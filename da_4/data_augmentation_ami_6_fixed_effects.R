#remove.packages("rgl") 
#install.packages("matlib", dependencies = FALSE) 
#install.packages('matlib', repos = c('https://friendly.r-universe.dev', 'https://cloud.r-project.org')) 
#remove.packages("rgl") 
# falls ein kaputter Rest existiert 
#install.packages("rgl", type = "source") 
#options(rgl.useNULL = TRUE) # oder dauerhaft in ~/.Rprofile: 
# options(rgl.useNULL = TRUE)
#install.packages("matlib")
library(matlib)
library(ggplot2)
library(ggridges)
#install.packages("here") 
library(here) 
source(here("data_augmentation_general.R")) 

# load dat in 
dat <- read.csv( "data/dat.csv", header = TRUE ) 
dat_loaded <- read.csv( "data/all_results_summary_updated.csv", header = TRUE ) 
# load and rename cols
dat <- dat_loaded[, c('Aspect_Ratio_b_a', 'Force_Actual_N', 'Initial_Length_cm', 'ROM_cm', 'Am', 'Rho')]

# Data visualisation
ggplot(dat[dat$Aspect_Ratio_b_a==9.0267,], aes(x = ROM_cm, y = Force_Actual_N, color = Initial_Length_cm)) +
  # Scatter points with color mapped inside aes()
  geom_point(
    size = 1.5
  )

# visualise entire data set
  # uncleaned
ggplot(dat, aes(x = ROM_cm, y = Force_Actual_N)) +
  # Scatter points with color mapped inside aes()
  geom_point(
    size = 1.5
  )
ggplot(dat[dat$ROM_cm<25,], aes(x = ROM_cm, y = Force_Actual_N)) +
  # Scatter points with color mapped inside aes()
  geom_point(
    size = 1.5
  )

dat = dat[dat$ROM_cm<25,]

aim_muscle_length <- 34.97 #[cm] the muscle length for which predictions should be made
aim_ratio <- 34.97/3.87 #[] the ratio of width to length for which predictions should be made
aim_volume <- aim_muscle_length^3 * aim_ratio^(-2) # [cm^3] the muscle volume for which predictions should be made

# Normalise data to [0,1]
minmax <- function(x) (x - min(x)) / (max(x) - min(x)) 
fn_minmax_single <- function(dat)( function(x) (x - min(dat)) / (max(dat) - min(dat)))
fn_minmax_inv <- function(dat)( function(x) x * (max(dat) - min(dat)) + min(dat))
minmax_inv_prestretch <- fn_minmax_inv(dat$Force_Actual_N)
minmax_inv_prestretch_quad <- fn_minmax_inv(dat$Force_Actual_N_quad)
minmax_inv_rom <- fn_minmax_inv(dat$ROM_cm)
minmax_single_muscle_length <- fn_minmax_single(dat$Initial_Length_cm)
minmax_single_ratio <- fn_minmax_single(dat$Aspect_Ratio_b_a)
minmax_single_prestretch <- fn_minmax_single(dat$Force_Actual_N)



# prestretch, muscle length, aspect ratio, prestretch^2, ratio*prestretch, ratio*prestretch^2, y axis intercept Fixed effects (m rows, p columns) 
X <- as.matrix(dat[c('Force_Actual_N', 'Initial_Length_cm', 'Aspect_Ratio_b_a')]) 
X <- apply(X, 2, minmax) # normalise before adding scaled data
X <- cbind(X, Force_Actual_N_quad = X[, 'Force_Actual_N']^2) # add quadratic term after [0,1] normalisation
X <- cbind(X, cross = X[, 'Aspect_Ratio_b_a'] * X[, 'Force_Actual_N']) # add cross term
X <- cbind(X, cross_quad = X[, 'Aspect_Ratio_b_a'] * X[, 'Force_Actual_N']^2) # add cross term with F^2
X <- cbind(X, intercept = 1) # add intercept
#, rho, Am # Random Effects (m rows, q columns) 
Z <- as.matrix(dat[c('Rho', 'Am')]) 
Z <- apply(Z, 2, minmax) 
#, predictor: rom
Y <- as.matrix(dat$ROM_cm) 
# normalise
Y <- apply(Y, 2, minmax)

# only work on subset of data
subsample_size <- 500
subsample_bool <- FALSE#
if(subsample_bool){
  subset <- sample(nrow(Y),size=subsample_size,replace=FALSE)
  X <- X[subset,]
  Z <- Z[subset,]
  Y <- Y[subset,, drop = FALSE]
} else {
  subset <- 1:nrow(dat)
}

# fix seed for reproducibility
set.seed(123)

n_iterations <- 50

# conduct EM algorithm
results <- run_EM_algorithm(X=X, Y=Y, Z=Z, n_iterations=n_iterations, early_stopping=TRUE)
sigma_quad <- results$sigma_quad
beta <- results$beta
xi_tild <- results$xi_tild
Z_tild <- results$Z_tild
Upsilon <- results$Upsilon
l <- results$l
q <- results$q
b <- results$b
n <- results$n
big_T <- results$big_T
xi <- results$xi
fails <- results$fail
converges_at <- results$i


### uniform evaluation of prestretch vs ROM
m = 100
r <- 10

X_test <- t(matrix(c(rep(0.5, 1), rep((minmax_single_muscle_length(aim_muscle_length)), 1), rep((minmax_single_ratio(aim_ratio)),1), rep(0.5^2, 1), rep((minmax_single_ratio(aim_ratio) * minmax_single_prestretch(0.5)), 1), rep((minmax_single_ratio(aim_ratio) * 0.5^2), 1), rep(1, 1)), nrow = 7, byrow = TRUE)) 
Z_test <- cbind(1, rep(0.5, r)) 
b <- mvrnorm(n = m, mu = rep(0, q), Sigma = big_T) 

Y_pred_vec <- array(0, dim = c(m, r, r, r))
for(l in 1:m){
  for(i in 1:r){ #prestretch
    X_test <- t(matrix(c(rep(i/r, r), rep((minmax_single_muscle_length(aim_muscle_length)), r), rep((minmax_single_ratio(aim_ratio)), r), rep((i/r)^2, r), rep((minmax_single_ratio(aim_ratio) * (i/r)), r), rep((minmax_single_ratio(aim_ratio) * (i/r)^2), r), rep(1, r)), nrow = 7, byrow = TRUE)) 
    for(j in 1:r){ #rho
      e <- mvrnorm(n=r, mu=0, Sigma = sigma_quad) # sample white noise
      
      Z_test[,1] <- j/r
      Z_test[,2] <- (1:r)/r
            Y_pred_vec[l, i, j, ] <- (X_test %*% beta +
                                         Z_test %*% xi +
                                         Z_test %*% b[l,] +
                                        e) # add white noise
      }
    }
  }


for(i in 1:r){
  for(j in 1:r){
    for(k in 1:r){
      Y_pred_vec[,i,j,k] <- Y_pred_vec[, i, j, k] * dnorm(j/r, mean=0.5, sd = 0.15) *dnorm(k/r, mean=0.5, sd = 0.15)
        
    }
  }
}

# take mean to integrate out random effects
marginalized_y_pred_vec <- apply(Y_pred_vec, MARGIN = c(1, 2), FUN = mean)


### make plot to compare marginalised pred for multiple prestretches
prestretches <- minmax_inv_prestretch(rep((1:r)/r, each = m))
rom <- as.vector(lapply(marginalized_y_pred_vec, minmax_inv_rom))

# Create data frame
df_long <- data.frame(
  prestretch = factor(round(prestretches, 1)),
  rom = as.numeric(rom)
)

# export dataframe with result to csv
num_samples <- ifelse(subsample_bool, subsample_size, nrow(X))
write.csv(df_long, sprintf("data/output/uniform_prestretches_%s", num_samples), row.names = TRUE)



ggplot(df_long, aes(x = rom, y = prestretch)) +
  # Ridges with fill mapped inside aes()
  geom_density_ridges(
    aes(fill = "DA pred"),  # Map fill to a constant string
    alpha = 0.8,
    color = "black"
  )

ggplot(df_long, aes(x = rom, y = prestretch)) +
  # Scatter points with color mapped inside aes()
  geom_point(
    data = dat[subset,],
    aes(x = ROM_cm, y = Force_Actual_N, color = "Input data"),  # Map color to a constant string
    #alpha = 0.3,
    size = 1.5
  )


# Sanity check
ggplot(df_long, aes(x = rom, y = prestretch)) +
  # Scatter points with color mapped inside aes()
  geom_point(
    data = dat[subset,],
    aes(x = ROM_cm, y = Force_Actual_N, color = Aspect_Ratio_b_a),  # Map color to a constant string
    #alpha = 0.3,
    size = 1.5
  )


# somehow the combined plot does not work anymore as the y axis is categoric for geom_density_ridges and 
ggplot(df_long, aes(x = rom, y = prestretch)) +
  # Ridges with fill mapped inside aes()
  geom_density_ridges(
    aes(fill = "DA pred"),  # Map fill to a constant string
    alpha = 0.8,
    color = "black"
  ) +
  # Scatter points with color mapped inside aes()
  geom_point(
    data = dat[subset,],
    aes(x = ROM_cm, y = Force_Actual_N, color = "Input data"),  # Map color to a constant string
    #alpha = 0.3,
    size = 1.5
  ) +
  # Customize fill and color scales for the legend
  scale_fill_manual(
    name = "Plot Type",
    values = c("DA pred" = "#1f77b4")
  ) +
  scale_color_manual(
    name = "Plot Type",
    values = c("Input data" = "#ff7f0e")
  ) +
  labs(
    title = "Density Ridges of ROM by Prestretch",
    x = "Range of Motion (ROM)",
    y = "Prestretch Level"
  ) +
  theme_light(base_family = "sans") +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
    axis.title = element_text(size = 12, face = "bold"),
    axis.text = element_text(size = 10),
    legend.position = "right"
  )




## BO data prediction with uncertainties
# load BO runs in 
bo_samples <- read.csv( "data/bo_cuboid_updated.csv", header = TRUE)
bo_prestretches <- minmax_single_prestretch(bo_samples$prestretch_force)
# define geometry of BO run
bo_ratio <- 34.97 / 3.87
bo_muscle_length <- 34.97

m = 100
r <- length(bo_prestretches)

X_test <- t(matrix(c(rep(0.5, 1),rep((minmax_single_muscle_length(bo_muscle_length)), 1), rep((minmax_single_ratio(bo_ratio)), 1), rep(0.5^2, 1), rep(minmax_single_ratio(bo_ratio) * (0.5), 1), rep(minmax_single_ratio(bo_ratio) * (0.5^2), 1), rep(1, 1)), nrow = 7, byrow = TRUE)) 
Z_test <- cbind(1, rep(0.5, r)) 
b <- mvrnorm(n = m, mu = rep(0, q), Sigma = big_T) 

Y_pred_vec <- array(0, dim = c(m, r, r, r))
for(l in 1:m){
  for(i in 1:r){ #prestretch
    X_test <- t(matrix(c(rep(bo_prestretches[i], r), rep((minmax_single_muscle_length(bo_muscle_length)), r), rep((minmax_single_ratio(bo_ratio)), r), rep(bo_prestretches[i]^2, r), rep((minmax_single_ratio(bo_ratio) * (bo_prestretches[i])), r), rep((minmax_single_ratio(bo_ratio) * (bo_prestretches[i]^2)), r) , rep(1, r)), nrow = 7, byrow = TRUE)) 
    for(j in 1:r){ #rho
      e <- mvrnorm(n=r, mu=0, Sigma = sigma_quad) # sample white noise
      
      Z_test[,1] <- j/r
      Z_test[,2] <- (1:r)/r
      Y_pred_vec[l, i, j, ] <- (X_test %*% beta +
                                  Z_test %*% xi +
                                  Z_test %*% b[l,] +
                                  e) # add white noise
    }
  }
}


for(i in 1:r){
  for(j in 1:r){
    for(k in 1:r){
      Y_pred_vec[,i,j,k] <- Y_pred_vec[, i, j, k] * dnorm(j/r, mean=0.5, sd = 0.15) *dnorm(k/r, mean=0.5, sd = 0.15)
      
    }
  }
}


marginalized_y_pred_vec <- apply(Y_pred_vec, MARGIN = c(1, 2), FUN = mean)



### make plot to compare marginalised pred for multiple prestretches
prestretches <- minmax_inv_prestretch(rep(bo_prestretches, each = m))
rom <- as.vector(lapply(marginalized_y_pred_vec, minmax_inv_rom))

# Create data frame
df_long <- data.frame(
  prestretch = factor(round(prestretches, 1)),
  rom = as.numeric(rom)
)

# export dataframe with result to csv
num_samples <- ifelse(subsample_bool, subsample_size, nrow(X))
write.csv(df_long, sprintf("data/output/bo_prestretches_%s", num_samples), row.names = TRUE)



ggplot(df_long, aes(x = rom, y = prestretch)) +
  # Ridges with fill mapped inside aes()
  geom_density_ridges(
    aes(fill = "DA pred"),  # Map fill to a constant string
    alpha = 0.8,
    color = "black"
  )

# data reference
ggplot(dat[(abs(dat$Aspect_Ratio_b_a-bo_ratio)<0.2) & abs(dat$Initial_Length_cm-bo_muscle_length)<2,], aes(x = ROM_cm, y = Force_Actual_N, color = Aspect_Ratio_b_a)) +
  # Scatter points with color mapped inside aes()
  geom_point(
    size = 1.5
  )

ggplot(bo_samples, aes(x = range_of_motion, y = prestretch_force)) +
  # Scatter points with color mapped inside aes()
  geom_point(
    #aes(x = rom, y = pretr, color = "Input data"),  # Map color to a constant string
    #alpha = 0.3,
    size = 1.5
  )

