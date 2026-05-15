#import libraries: install.packages("matlib")
library(matlib)
#install.packages("arrayhelpers")
library(arrayhelpers)
#install.packages("MASS")
library(MASS)
#install.packages("tibble")
library(tibble)
# install.packages("distributions3")
library(distributions3)

# Auxiliary functions
get_W <- function(i, beta, xi, sigma_quad, big_T, n_i, Z) {
  # Construct the matrix inside the inverse following the paper
  answer <- (sigma_quad * diag(n_i) + Z[i, , drop = FALSE] %*% big_T %*% t(Z[i, , drop = FALSE]))
  if (n_i == 1) {
    answer <- answer^-1
  }
  else{
    answer <- inv(answer)
  }
  
  return(answer)
}

get_b_hat <- function(i, big_T, Z, W_i, y, X, beta, xi) {
  return ((big_T %*% t(Z[i, , drop = FALSE]) %*% W_i) %*%
            (Y[i, , drop = FALSE] - X[i, , drop = FALSE] %*% beta - Z[i, , drop = FALSE] %*% xi))
}

# notation according to paper definition under 8.3; assume Upsilon as full matrix
get_Z_tild_i <- function(Z_i, d_i, n_i, q) {
  Z_tild_i <- matrix(c(0), nrow = 1, ncol = q^2)
  for (k in 1:q) {
    for (l in 1:q) {
      Z_tild_i[1, (k - 1) * q + l] = (Z_i[k] %*% t(d_i))[1, l]
    }
  }
  return(Z_tild_i)
}

get_y_pred <- function(n, sigma_quad, X, beta, Z, xi_tild, Z_tild, Upsilon, q, white_noise = TRUE) {
  # Prediction (8.3)
  e <- mvrnorm(1, rep(c(0), n), sigma_quad[1, 1] * diag(n))
  Y_pred <- X %*% beta + Z %*% xi_tild + Z_tild %*% matrix(Upsilon, nrow = q^2, ncol = 1) 
  if(white_noise){
    Y_pred <- Y_pred + e
  }
  return (Y_pred)
}


# sample b as described in Van Dyk and Meng step 1 p.28
step1 <- function(beta, xi, sigma_quad, big_T, n_i, Z, m, q, b) {
  for (i in 1:m) {
    W_i <- get_W(i, beta, xi, sigma_quad, big_T, n_i, Z)
    b_hat_i <- get_b_hat(i, big_T, Z, W_i, y, X, beta, xi)
    stand_err <- (big_T - (big_T %*% t(Z[i, , drop = FALSE])
                           %*% W_i %*% Z[i, , drop = FALSE] %*% big_T)) # Formel 8.4
    
    for (j in 1:q) {
      b[j, i] <- rnorm(1, b_hat_i, stand_err)
    }
  }
  return(b)
}

# now step 2
step2 <- function(m, Ups_Inv, b, gamma, beta, xi_tild, Z, n_i, q, Y, X, n, p) {
  X_tild <- matrix(c(0), nrow = m, ncol = p + q + q^2) # here Upsilon is assumed to be a full matrix
  Z_tild <- matrix(c(0), nrow = m, ncol = q^2) # same assumption as above
  for (i in 1:m) {
    d_i <- Ups_Inv %*% b[, i, drop = FALSE] + gamma #Formel 8.2
    Z_tild_i <- get_Z_tild_i(Z[i, , drop = FALSE], d_i, n_i, q)
    Z_tild[i, ] <- Z_tild_i
    X_tild[i, ] <- c(as.numeric(X[i, ]), as.numeric(Z[i, ]), as.numeric(Z_tild_i))
    #X_tild[i, ] <- c(X[i, , drop = FALSE], Z[i, , drop = FALSE], Z_tild_i)
  }
  normalizing_factor <- rchisq(1, n - p - q - q^2)
  sigma_quad <- (t(Y) %*% (diag(n) - X_tild %*% inv(t(X_tild) %*% X_tild) %*% t(X_tild)) %*%
                   Y) / normalizing_factor
  
  # Equation 8.7
  mean <- inv(t(X_tild) %*% X_tild) %*% t(X_tild) %*% Y
  var <- sigma_quad[1, 1] * inv(t(X_tild) %*% X_tild) # If n_i = 1, sigma_quad is scalar
  
  RHS <- mvrnorm(1, mean, var)
  
  beta[, 1] <- RHS[1:p]
  xi_tild[, 1] <- RHS[(p + 1):(p + q)]
  Upsilon <- matrix(RHS[(p + q + 1):(p + q + q^2)], nrow = q, ncol = q)
  
  mu_gamma <- matrix(rowSums(b) / m, nrow = q, ncol = 1)
  
  var_wish <- matrix(c(0), nrow = q, ncol = q)
  for (i in 1:m) {
    var_wish <- var_wish + (b[, i] - mu_gamma) %*% t(b[, i] - mu_gamma)
  }
  
  if (dim(var_wish)[1] == 1){
    var_wish = 1/var_wish
  } else{
    var_wish <- inv(var_wish)
  }
  
  t_tild_inv <- rWishart(1, m - q - 1, var_wish)
  t_tild_inv <- t_tild_inv[, , 1]
  
  if (dim(var_wish)[1] == 1){
    t_tild = 1/t_tild_inv
  } else{
    t_tild <- inv(t_tild_inv)
  }
  
  gamma <- matrix(mvrnorm(1, mu_gamma, 1 / m * t_tild),
                  nrow = q,
                  ncol = 1)
  
  xi <- xi_tild + Upsilon %*% gamma
  big_T <- Upsilon %*% t_tild %*% t(Upsilon)
  
  return(
    list(
      beta = beta,
      xi = xi,
      sigma_quad = sigma_quad,
      big_T = big_T,
      Z_tild = Z_tild,
      Upsilon = Upsilon,
      Ups_Inv = Ups_Inv
    )
  )
}

run_EM_algorithm <- function(X, Y, Z, n_iterations=100, early_stopping=TRUE) {
  # create arbitrary data for X, Z, Y
  # here with two observations, notation following "Art of data augmentation" from van Dyk and Weng
  p <- dim(X)[2] # number of columns in X (fixed effects)
  q <- dim(Z)[2] # number of columns in Z (random effects)
  # Ensure, that m > p + q + q^2, otherwise (1) formula does not work or (2) X_tild could be invertable
  m <- dim(X)[1] # number of observation (e.g. subjects)
  n_i <- 1 # n_i here constant (Dependent variables)
  n <- m * n_i # Sum of observations
  l <- list()
  fail <- 0
  gamma <- matrix(rep(0, q), nrow = q, ncol = 1) # as in Liu, Rubin and Wu 1998
  Upsilon <- diag(q)
  sigma_quad <- 1
  big_T <- diag(q) # variance of random effects
  xi_tild <- matrix(c(0), nrow = q, ncol = 1)
  b <- matrix(rep(0, q), nrow = q, ncol = m)
  beta <- matrix(rep(1, p), nrow = p, ncol = 1)
  xi <- matrix(rep(1, q), nrow = q, ncol = 1)
  
  if (dim(Upsilon)[1] == 1){
    Ups_Inv = 1/Upsilon
  } else{
    Ups_Inv <- inv(Upsilon)
  }
  
  for (i in 1:n_iterations) {
    b <- step1(beta, xi, sigma_quad, big_T, n_i, Z, m, q, b=b)
    results_step2 <- try({
      step2(m, Ups_Inv, b, gamma, beta, xi_tild, Z, n_i, q, Y, X, n, p)
    }, silent = FALSE)
    
    if (inherits(results_step2, "try-error")) {
      #print(c("Cov matrix not positive definite at iteration ", i))
      fail <- 1
      return(list(fail=fail))
      break
      
    }
    else{
      # update values gathered in step 2
      sigma_quad <- results_step2$sigma_quad
      beta <- results_step2$beta
      xi <- results_step2$xi
      big_T <- results_step2$big_T
      Z_tild <- results_step2$Z_tild
      Upsilon <- results_step2$Upsilon
      Ups_Inv <- results_step2$Ups_Inv
      
      Y_pred <- get_y_pred(n, sigma_quad, X, beta, Z, xi_tild, Z_tild, Upsilon, q)
      mse <- get_mse(Y_pred, Y)
      l[[i]] <- mse
      if (mse < 0.01 & early_stopping) {
        #print(paste("Early stopped after", i,"iterations with MSE of", mse))
        return(list(beta=beta, xi_tild=xi_tild, Z_tild=Z_tild, Upsilon=Upsilon, sigma_quad=sigma_quad,
                    q=q, b=b, n=n, l=l, i = i, fail=fail, xi = xi, big_T = big_T))
      }
    }
  }
}

get_mse <- function(Y, Y_pred) {
  # compare iterated results to ground truth
  return(mean((Y - Y_pred)^2))
}
get_mae <- function(Y, Y_pred) {
  # compare iterated results to ground truth
  return(mean(abs(Y - Y_pred)))
}

plot_mse_over_iterations <- function(l, n_iterations) {
  # Create a sequence for x-axis (e.g., time or index)
  time <- seq_along(l)
  
  # Plot the values over time
  plot(
    time,
    l,
    ylim = c(0,1),
    type = "o",
    col = "blue",
    pch = 16,
    lwd = 2,
    xlab = "Iteration",
    ylab = "MSE Values",
    main = paste("MSE Values for", n_iterations, "iterations")
  )
  
  # Add a grid for better visibility
  grid()
}