#!/bin/bash
################################################################################
# Multi-Parameter Sweep for Data Augmentation (Surface-Area-Adjusted Forces)
# 
# Runs comprehensive parameter sweep for muscle prestretch simulations
# with surface-area-adjusted forces to ensure consistent stress levels.
#
# Parameters varied:
# FORCE_TARGETS=(0 3 6 9 12 15 18 21 24 27 30 33 36 39 42 45)  # [N] referenced to min area
# ASPECT_RATIOS=(6.88 7.95 9.03 10.1)                          # a/b ratios
# VOLUMES=(421.6 455.9 573.5 691.2 738.0)                      # [cm³]
# AM/RHO: 4 random combinations from available values
# 
# Key Changes from Previous Version:
# - Forces adjusted for surface area (0-45N range instead of 0-31N)
# - Aspect ratios instead of fixed muscle_y values
# - Reduced volume set (5 instead of 7 values)
# - Random sampling of Am/Rho (4 instead of 12 combinations)
# 
# Total Simulations: 4 × 5 × 16 × 4 = 1,280 (vs. 2,940 previously)
#
# Features:
# - Resume capability: Skips completed simulations in archived_results
# - Parallel execution: Runs multiple simulations simultaneously
# - Progress tracking: Maintains master log and summary CSV
# - Force adjustment: Calculates actual force based on geometry's surface area
#
# Usage:
#   1. Upload to server: scp run_parameter_sweep_new.sh cmcs-fa01@cmcs09:~/
#   2. SSH to server: ssh cmcs-fa01@cmcs09.mathematik.uni-stuttgart.de
#   3. Run: bash run_parameter_sweep_new.sh [existing_results_dir] [max_parallel]
#
# Examples:
#   bash run_parameter_sweep_new.sh  # Start new sweep
#   bash run_parameter_sweep_new.sh parameter_sweep_DA_20260129_120000  # Resume existing
#   bash run_parameter_sweep_new.sh parameter_sweep_DA_20260129_120000 4  # Resume with 4 parallel jobs
#
# See calculate_new_parameters.ipynb for parameter calculations and documentation
#
# Author: Generated for data augmentation study
# Date: 2026-01-29
################################################################################

set -e  # Exit on error

# Configuration
SERVER_USER="cmcs-fa01"
SERVER_HOST="cmcs09.mathematik.uni-stuttgart.de"
BASE_DIR="/usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular"
TEMPLATE_DIR="${BASE_DIR}/cuboid_4x4_prestretch_for_DA"

# Command-line arguments
EXISTING_RESULTS_DIR="${1:-}"  # Optional: path to existing results directory to resume
MAX_PARALLEL="${2:-4}"          # Optional: max parallel simulations (default: 4)

# Determine results directory
if [[ -n "${EXISTING_RESULTS_DIR}" ]]; then
    # Resume existing sweep
    if [[ "${EXISTING_RESULTS_DIR}" == /* ]]; then
        # Absolute path provided
        RESULTS_BASE="${EXISTING_RESULTS_DIR}"
    else
        # Relative path - assume it's in BASE_DIR
        RESULTS_BASE="${BASE_DIR}/${EXISTING_RESULTS_DIR}"
    fi
    
    if [[ ! -d "${RESULTS_BASE}" ]]; then
        echo "ERROR: Results directory not found: ${RESULTS_BASE}"
        exit 1
    fi
    
    RESUME_MODE=true
    echo "RESUME MODE: Using existing results directory: ${RESULTS_BASE}"
else
    # Start new sweep
    RESULTS_BASE="${BASE_DIR}/parameter_sweep_DA_$(date +%Y%m%d_%H%M%S)"
    RESUME_MODE=false
    echo "NEW SWEEP: Creating results directory: ${RESULTS_BASE}"
fi

# Parameter ranges
# ----------------
# NOTE: This configuration uses surface-area-adjusted forces and aspect ratios
# See calculate_new_parameters.ipynb for detailed calculations

# 1. Aspect ratios (a/b) - 4 equally-spaced values from 6.88 to 10.1
ASPECT_RATIOS=(6.8800 7.9533 9.0267 10.1000)

# 2. Volume values (cm³) - reduced set
VOLUMES=(421.6 455.9 573.5 691.2 738.0)

# 3. Force target values (N) - referenced to minimum surface area
# These are the TARGET forces; actual forces will be calculated based on geometry
FORCE_TARGETS=(0 3 6 9 12 15 18 21 24 27 30 33 36 39 42 45)

# 4. Reference surface area (cm²) - minimum area for force scaling
REFERENCE_AREA=203.3883

# 5. Random Am/Rho combinations (4 samples instead of all 12)
# Generated with random seed 42 for reproducibility
AM_VALUES=(550 450 500)
RHO_VALUES=(10.493 10.534 10.575 10.616)

# Simulation parameters
ENDTIME_MS=100  # 100 ms simulation time
N_RANKS=1       # Number of MPI ranks

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

################################################################################
# Functions
################################################################################

print_header() {
    echo -e "${BLUE}================================================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================================================================${NC}"
}

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

is_simulation_completed() {
    local force_target=$1
    local aspect_ratio=$2
    local volume=$3
    local am=$4
    local rho=$5
    
    # Format parameters for directory name (same logic as create_experiment_dir)
    local force_int=${force_target%.*}
    local force_formatted=$(printf "%02d" "${force_int}")
    local ratio_formatted="${aspect_ratio}"
    local volume_formatted="${volume}"
    local am_int=${am%.*}
    local rho_formatted="${rho}"
    
    local exp_name="F${force_formatted}_ratio${ratio_formatted}_Vol${volume_formatted}_Am${am_int}_rho${rho_formatted}"
    
    # Check if result exists in archived_results
    local archive_dir="${RESULTS_BASE}/archived_results/${exp_name}"
    
    if [[ -d "${archive_dir}" ]] && [[ -f "${archive_dir}/muscle_length_prestretch.csv" ]]; then
        return 0  # Completed
    else
        return 1  # Not completed
    fi
}

cleanup_incomplete_simulations() {
    # Clean up any incomplete simulation directories (not in archived_results)
    print_info "Cleaning up incomplete simulations..."
    
    local cleaned=0
    for dir in "${RESULTS_BASE}"/F*; do
        if [[ -d "${dir}" ]]; then
            local dirname=$(basename "${dir}")
            # Check if this simulation is in archived_results
            if [[ ! -d "${RESULTS_BASE}/archived_results/${dirname}" ]]; then
                print_warning "Removing incomplete simulation: ${dirname}"
                rm -rf "${dir}"
                cleaned=$((cleaned + 1))
            fi
        fi
    done
    
    if [[ ${cleaned} -gt 0 ]]; then
        print_info "Cleaned ${cleaned} incomplete simulation(s)"
    else
        print_info "No incomplete simulations found"
    fi
}

wait_for_slot() {
    # Wait until there's a free slot (fewer than MAX_PARALLEL jobs running)
    while true; do
        local running_jobs=$(jobs -r | wc -l)
        if [[ ${running_jobs} -lt ${MAX_PARALLEL} ]]; then
            break
        fi
        sleep 2
    done
}

check_background_jobs() {
    # Check for any failed background jobs
    local failed=0
    for job in $(jobs -p); do
        wait ${job} || failed=$((failed + 1))
    done
    return ${failed}
}

check_prerequisites() {
    print_header "Checking Prerequisites"
    
    # Check if we're on the server
    if [[ ! -d "${BASE_DIR}" ]]; then
        print_error "Base directory not found: ${BASE_DIR}"
        print_error "Are you running this on the server?"
        exit 1
    fi
    
    # Check if template exists
    if [[ ! -d "${TEMPLATE_DIR}" ]]; then
        print_error "Template directory not found: ${TEMPLATE_DIR}"
        exit 1
    fi
    
    # Check if executable exists
    if [[ ! -f "${TEMPLATE_DIR}/build_release/muscle_with_prestretch" ]]; then
        print_error "Executable not found: ${TEMPLATE_DIR}/build_release/muscle_with_prestretch"
        print_error ""
        print_error "Please compile first (in a separate terminal):"
        print_error "  cd ${TEMPLATE_DIR}"
        print_error "  mkorn && sr"
        print_error ""
        print_error "Then re-run this script."
        exit 1
    fi
    
    print_info "Executable found: ${TEMPLATE_DIR}/build_release/muscle_with_prestretch"
    print_info "All prerequisites OK"
}

create_experiment_dir() {
    local force_target=$1
    local aspect_ratio=$2
    local volume=$3
    local am=$4
    local rho=$5
    
    # Calculate muscle dimensions from volume and aspect ratio
    # For cuboid [b, a, a]: Volume = b * a²
    # Aspect ratio r = a/b, so a = r * b
    # Volume = b * (r*b)² = b³ * r²
    # Therefore: b = (Volume / r²)^(1/3) and a = r * b
    
    local muscle_b=$(echo "scale=6; e((l(${volume} / (${aspect_ratio} * ${aspect_ratio})) / 3) * l(10) / l(10))" | bc -l)
    local muscle_a=$(echo "scale=6; ${aspect_ratio} * ${muscle_b}" | bc -l)
    
    # Calculate surface area for force adjustment
    local surface_area=$(echo "scale=6; ${muscle_a} * ${muscle_a}" | bc -l)
    
    # Calculate actual force to apply (adjust for surface area)
    # F_actual = F_target × (A_geometry / A_reference)
    # This ensures same stress across all geometries
    local force_actual=$(echo "scale=6; ${force_target} * ${surface_area} / ${REFERENCE_AREA}" | bc -l)
    
    # Format parameters for directory name
    local force_int=${force_target%.*}
    local force_formatted=$(printf "%02d" "${force_int}")
    local ratio_formatted="${aspect_ratio}"
    local volume_formatted="${volume}"
    local am_int=${am%.*}
    local rho_formatted="${rho}"
    
    # Create experiment name with new parameters
    local exp_name="F${force_formatted}_ratio${ratio_formatted}_Vol${volume_formatted}_Am${am_int}_rho${rho_formatted}"
    local exp_dir="${RESULTS_BASE}/${exp_name}"
    
    # Create directory structure
    mkdir -p "${exp_dir}/build_release"
    
    # Copy necessary files
    cp "${TEMPLATE_DIR}/settings_muscle_with_prestretch.py" "${exp_dir}/" 2>/dev/null || true
    cp "${TEMPLATE_DIR}/helper.py" "${exp_dir}/" 2>/dev/null || true
    cp -r "${TEMPLATE_DIR}/variables" "${exp_dir}/" 2>/dev/null || true
    cp -r "${TEMPLATE_DIR}/src" "${exp_dir}/" 2>/dev/null || true
    
    # Modify variables.py with the specific parameter values
    local variables_file="${exp_dir}/variables/variables.py"
    if [[ -f "${variables_file}" ]]; then
        # Update muscle_extent with calculated a and b
        sed -i.bak "s/^muscle_extent = .*/muscle_extent = [${muscle_a}, ${muscle_a}, ${muscle_b}]  # [cm, cm, cm] - Vol=${volume} cm^3, ratio=${aspect_ratio}/" "${variables_file}"
        
        # Update end_time to 100 ms
        sed -i.bak "s/^end_time = .*/end_time = ${ENDTIME_MS}/" "${variables_file}"
        
        # Update rho value
        sed -i.bak "s/^rho = 10   .*/rho = ${rho}   ## [1e-4 kg\/cm^3] density/" "${variables_file}"
        sed -i.bak "s/^rho = 10  .*/rho = ${rho}                    # [1e-4 kg\/cm^3] density of the muscle/" "${variables_file}"
        
        # Update Am value
        sed -i.bak "s/^Am = .*/Am = ${am}                          # surface area to volume ratio [cm^-1]/" "${variables_file}"
        
        # Update diffusion_prefactor to match new Am value
        sed -i.bak "s/^diffusion_prefactor = .*/diffusion_prefactor = 3.828 \/ (${am} * 0.58)  # Conductivity \/ (Am * Cm)/" "${variables_file}"
        
        # Remove backup files
        rm -f "${variables_file}.bak"
    fi
    
    # Symlink to compiled executable
    ln -sf "${TEMPLATE_DIR}/build_release/muscle_with_prestretch" "${exp_dir}/build_release/"
    
    # Copy lib directory
    if [[ -d "${TEMPLATE_DIR}/build_release/lib" ]]; then
        cp -r "${TEMPLATE_DIR}/build_release/lib" "${exp_dir}/build_release/" 2>/dev/null || true
    else
        mkdir -p "${exp_dir}/build_release/lib"
    fi
    
    # Create documentation
    cat > "${exp_dir}/README.md" << EOF
# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): ${force_target} N
- Force Actual (at this geometry): ${force_actual} N
- Aspect Ratio (a/b): ${aspect_ratio}
- muscle_extent: [${muscle_a}, ${muscle_a}, ${muscle_b}] cm
- Volume: ${volume} cm³
- Surface Area: ${surface_area} cm²
- Am: ${am} cm⁻¹
- Rho: ${rho} [1e-4 kg/cm³]
- Simulation Time: ${ENDTIME_MS} ms

## Force Adjustment
- Reference Area: ${REFERENCE_AREA} cm²
- Geometry Area: ${surface_area} cm²
- Area Ratio: $(echo "scale=4; ${surface_area} / ${REFERENCE_AREA}" | bc -l)
- Applied Stress: $(echo "scale=8; ${force_actual} / ${surface_area}" | bc -l) N/cm²
- Reference Stress: $(echo "scale=8; ${force_target} / ${REFERENCE_AREA}" | bc -l) N/cm²

## Created
- Date: $(date)
- Template: ${TEMPLATE_DIR}

## Calculated Values
- muscle_b = (Vol/r²)^(1/3) = (${volume}/${aspect_ratio}²)^(1/3) = ${muscle_b} cm
- muscle_a = r × b = ${aspect_ratio} × ${muscle_b} = ${muscle_a} cm
- F_actual = F_target × (A/A_ref) = ${force_target} × (${surface_area}/${REFERENCE_AREA}) = ${force_actual} N

## Run Command
\`\`\`bash
cd ${exp_dir}/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py ${force_actual} 0 ${N_RANKS}
\`\`\`
EOF
    
    # Store actual force for simulation run
    echo "${force_actual}" > "${exp_dir}/force_actual.txt"
    
    echo "${exp_dir}"
}

run_simulation() {
    local force_actual=$1
    local exp_dir=$2
    local force_target=$3
    local aspect_ratio=$4
    local volume=$5
    local am=$6
    local rho=$7
    
    # Change to build directory
    cd "${exp_dir}/build_release" || return 1
    
    # Execute simulation (suppress most output to avoid log overflow)
    ./muscle_with_prestretch ../settings_muscle_with_prestretch.py ${force_actual} 0 ${N_RANKS} > sim.log 2>&1
    
    local exit_code=$?
    
    if [ ${exit_code} -ne 0 ]; then
        print_error "Simulation failed with exit code ${exit_code}"
        return ${exit_code}
    fi
    
    return 0
}

run_simulation_wrapper() {
    # Wrapper function to run simulation and handle results in background
    local force_target=$1
    local aspect_ratio=$2
    local volume=$3
    local am=$4
    local rho=$5
    local sim_number=$6
    local total_sims=$7
    
    # Create experiment directory (also calculates force_actual and muscle dimensions)
    local exp_dir=$(create_experiment_dir "${force_target}" "${aspect_ratio}" "${volume}" "${am}" "${rho}")
    
    # Read the actual force from the created file
    local force_actual=$(cat "${exp_dir}/force_actual.txt")
    
    # Calculate muscle dimensions for logging
    local muscle_b=$(echo "scale=6; e((l(${volume} / (${aspect_ratio} * ${aspect_ratio})) / 3) * l(10) / l(10))" | bc -l)
    local muscle_a=$(echo "scale=6; ${aspect_ratio} * ${muscle_b}" | bc -l)
    
    # Log to master
    {
        echo "=== Simulation ${sim_number}/${total_sims} ===" 
        echo "F_target=${force_target}N, F_actual=${force_actual}N, ratio=${aspect_ratio}, Vol=${volume}, Am=${am}, rho=${rho}"
        echo "Dimensions: [${muscle_a}, ${muscle_a}, ${muscle_b}] cm"
        echo "Directory: $(basename ${exp_dir})"
        echo "Started: $(date)"
    } >> "${MASTER_LOG}"
    
    # Run simulation with actual force
    if run_simulation "${force_actual}" "${exp_dir}" "${force_target}" "${aspect_ratio}" "${volume}" "${am}" "${rho}"; then
        # Save results
        save_results "${force_target}" "${force_actual}" "${exp_dir}" "${aspect_ratio}" "${volume}" "${am}" "${rho}"
        
        # Extract metrics for summary
        local prestretch_file="${exp_dir}/build_release/muscle_length_prestretch.csv"
        if [[ -f "${prestretch_file}" ]]; then
            local final_length=$(tail -1 "${prestretch_file}" | cut -d',' -f2)
            local elongation=$(echo "${final_length} - ${muscle_b}" | bc -l)
            local strain=$(echo "scale=6; ${elongation} / ${muscle_b}" | bc -l)
            echo "${force_target},${force_actual},${aspect_ratio},${muscle_b},${muscle_a},${volume},${am},${rho},${muscle_b},${final_length},${elongation},${strain},$(date)" >> "${SUMMARY_FILE}"
        fi
        
        echo "Status: SUCCESS" >> "${MASTER_LOG}"
        echo "Completed: $(date)" >> "${MASTER_LOG}"
        echo "" >> "${MASTER_LOG}"
        
        # Clean up experiment directory to save disk space
        rm -rf "${exp_dir}"
        
        return 0
    else
        echo "Status: FAILED" >> "${MASTER_LOG}"
        echo "Completed: $(date)" >> "${MASTER_LOG}"
        echo "" >> "${MASTER_LOG}"
        return 1
    fi
}

save_results() {
    local force_target=$1
    local force_actual=$2
    local exp_dir=$3
    local aspect_ratio=$4
    local volume=$5
    local am=$6
    local rho=$7
    
    # Calculate muscle dimensions
    local muscle_b=$(echo "scale=6; e((l(${volume} / (${aspect_ratio} * ${aspect_ratio})) / 3) * l(10) / l(10))" | bc -l)
    local muscle_a=$(echo "scale=6; ${aspect_ratio} * ${muscle_b}" | bc -l)
    local surface_area=$(echo "scale=6; ${muscle_a} * ${muscle_a}" | bc -l)
    
    # Format for archive directory
    local force_int=${force_target%.*}
    local force_formatted=$(printf "%02d" "${force_int}")
    local ratio_formatted="${aspect_ratio}"
    local volume_formatted="${volume}"
    local am_int=${am%.*}
    local rho_formatted="${rho}"
    
    local archive_name="F${force_formatted}_ratio${ratio_formatted}_Vol${volume_formatted}_Am${am_int}_rho${rho_formatted}"
    local archive_dir="${RESULTS_BASE}/archived_results/${archive_name}"
    mkdir -p "${archive_dir}"
    
    # Copy only essential result files (not entire build_release to save space)
    cp "${exp_dir}/build_release/muscle_length_prestretch.csv" "${archive_dir}/" 2>/dev/null || true
    cp "${exp_dir}/build_release/muscle_length_contraction.csv" "${archive_dir}/" 2>/dev/null || true
    cp "${exp_dir}/build_release/sim.log" "${archive_dir}/" 2>/dev/null || true
    cp "${exp_dir}/settings_muscle_with_prestretch.py" "${archive_dir}/" 2>/dev/null || true
    cp "${exp_dir}/README.md" "${archive_dir}/" 2>/dev/null || true
    cp -r "${exp_dir}/variables" "${archive_dir}/" 2>/dev/null || true
    
    # Extract metrics
    local prestretch_file="${exp_dir}/build_release/muscle_length_prestretch.csv"
    if [[ -f "${prestretch_file}" ]]; then
        local final_length=$(tail -1 "${prestretch_file}" | cut -d',' -f2)
        local elongation=$(echo "${final_length} - ${muscle_b}" | bc -l)
        local strain=$(echo "scale=6; ${elongation} / ${muscle_b}" | bc -l)
        
        # Save summary
        cat > "${archive_dir}/summary.txt" << EOF
Parameters:
-----------
Force Target (at reference): ${force_target} N
Force Actual (at geometry): ${force_actual} N
Aspect Ratio (a/b): ${aspect_ratio}
muscle_extent: [${muscle_a}, ${muscle_a}, ${muscle_b}] cm
Volume: ${volume} cm³
Surface Area: ${surface_area} cm²
Am: ${am} cm⁻¹
Rho: ${rho} [1e-4 kg/cm³]

Force Adjustment:
----------------
Reference Area: ${REFERENCE_AREA} cm²
Geometry Area: ${surface_area} cm²
Area Ratio: $(echo "scale=4; ${surface_area} / ${REFERENCE_AREA}" | bc -l)

Results:
--------
Initial Length: ${muscle_b} cm
Final Length: ${final_length} cm
Elongation: ${elongation} cm
Strain: ${strain}

Completed: $(date)
EOF
    fi
    
    return 0
}

################################################################################
# Main Script
################################################################################

main() {
    print_header "Multi-Parameter Sweep for Data Augmentation (Surface-Area-Adjusted)"
    
    # Calculate total simulations
    local total_sims=$((${#ASPECT_RATIOS[@]} * ${#VOLUMES[@]} * ${#FORCE_TARGETS[@]} * ${#AM_VALUES[@]}))
    
    echo ""
    print_info "Configuration:"
    print_info "  Template:     ${TEMPLATE_DIR}"
    print_info "  Results:      ${RESULTS_BASE}"
    if [[ "${RESUME_MODE}" == "true" ]]; then
        print_info "  Mode:         RESUME (skip completed simulations)"
    else
        print_info "  Mode:         NEW"
    fi
    print_info "  Parallel:     ${MAX_PARALLEL} simultaneous jobs"
    print_info "  Aspect Ratios: ${#ASPECT_RATIOS[@]} values (6.88-10.1)"
    print_info "  Volumes:      ${#VOLUMES[@]} values (421.6-738 cm³)"
    print_info "  Forces:       ${#FORCE_TARGETS[@]} values (0-45 N, surface-area-adjusted)"
    print_info "  Am/Rho:       ${#AM_VALUES[@]} random combinations"
    print_info "  Reference Area: ${REFERENCE_AREA} cm²"
    print_info "  EndTime:      ${ENDTIME_MS} ms"
    print_info "  Ranks:        ${N_RANKS}"
    print_info "  Total:        ${total_sims} simulations"
    echo ""
    
    # Check prerequisites
    check_prerequisites
    
    # Create or verify results directory structure
    if [[ "${RESUME_MODE}" == "true" ]]; then
        print_info "Resuming existing sweep..."
        
        # Clean up incomplete simulations
        cleanup_incomplete_simulations
        
        # Count completed simulations
        local completed_count=$(find "${RESULTS_BASE}/archived_results" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
        local remaining=$((total_sims - completed_count))
        
        print_info "Progress: ${completed_count}/${total_sims} completed, ${remaining} remaining"
        
        if [[ ${remaining} -eq 0 ]]; then
            print_info "All simulations already completed!"
            exit 0
        fi
        
        echo ""
        print_warning "Will run ${remaining} remaining simulations with ${MAX_PARALLEL} parallel jobs"
        echo ""
        read -p "Continue? (yes/no): " -r
        if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
            print_info "Aborted by user"
            exit 0
        fi
    else
        print_warning "WARNING: This will run ${total_sims} simulations!"
        print_warning "Estimated time: ~$(echo "scale=2; ${total_sims} * 5 / 60 / ${MAX_PARALLEL}" | bc -l) hours (assuming 5 min per sim, ${MAX_PARALLEL} parallel)"
        echo ""
        read -p "Continue? (yes/no): " -r
        if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
            print_info "Aborted by user"
            exit 0
        fi
        
        # Create results base directory
        print_info "Creating results directory: ${RESULTS_BASE}"
        mkdir -p "${RESULTS_BASE}"
        mkdir -p "${RESULTS_BASE}/archived_results"
    fi
    
    # Initialize or append to logs
    MASTER_LOG="${RESULTS_BASE}/parameter_sweep_log.txt"
    SUMMARY_FILE="${RESULTS_BASE}/all_results_summary.csv"
    
    if [[ "${RESUME_MODE}" != "true" ]]; then
        # Create new logs
        echo "Parameter Sweep Started: $(date)" > "${MASTER_LOG}"
        print_info "Total Simulations: ${total_sims}" >> "${MASTER_LOG}"
        print_info "Parallel Jobs: ${MAX_PARALLEL}" >> "${MASTER_LOG}"
        echo "" >> "${MASTER_LOG}"
        
        echo "Force_Target_N,Force_Actual_N,Aspect_Ratio_a_b,muscle_b_cm,muscle_a_cm,Volume_cm3,Am,Rho,Initial_Length_cm,Final_Length_cm,Elongation_cm,Strain,Completed_Date" > "${SUMMARY_FILE}"
    else
        # Append to existing logs
        {
            echo ""
            echo "======================================================================"
            echo "Resumed: $(date)"
            echo "Parallel Jobs: ${MAX_PARALLEL}"
            echo "======================================================================"
            echo ""
        } >> "${MASTER_LOG}"
    fi
    
    # Run simulations with 4-nested loop and parallelization
    print_header "Running Simulations (${MAX_PARALLEL} parallel jobs)"
    
    local success_count=0
    local failure_count=0
    local skipped_count=0
    local sim_number=0
    
    # 4-nested loop: Am/Rho combinations -> Volume -> Aspect Ratio -> Force Target
    for i in "${!AM_VALUES[@]}"; do
        local am="${AM_VALUES[$i]}"
        local rho="${RHO_VALUES[$i]}"
        
        for volume in "${VOLUMES[@]}"; do
            for aspect_ratio in "${ASPECT_RATIOS[@]}"; do
                for force_target in "${FORCE_TARGETS[@]}"; do
                    sim_number=$((sim_number + 1))
                    
                    # Check if simulation already completed
                    if is_simulation_completed "${force_target}" "${aspect_ratio}" "${volume}" "${am}" "${rho}"; then
                        skipped_count=$((skipped_count + 1))
                        
                        # Print progress every 50 skips
                        if [ $((skipped_count % 50)) -eq 0 ]; then
                            print_info "Skipped ${skipped_count} completed simulations..."
                        fi
                        continue
                    fi
                    
                    # Wait for available slot
                    wait_for_slot
                    
                    # Print progress
                    local running=$((sim_number - skipped_count - success_count - failure_count))
                    print_info "Starting ${sim_number}/${total_sims}: F_target=${force_target}N, ratio=${aspect_ratio}, Vol=${volume}, Am=${am}, ρ=${rho} (${running} running)"
                    
                    # Launch simulation in background
                    run_simulation_wrapper "${force_target}" "${aspect_ratio}" "${volume}" "${am}" "${rho}" "${sim_number}" "${total_sims}" &
                    
                    # Small delay to avoid race conditions
                    sleep 0.5
                    
                    # Progress update every 10 simulations
                    if [ $(((sim_number - skipped_count) % 10)) -eq 0 ]; then
                        local completed=$((success_count + failure_count))
                        print_info "Progress: ${completed} completed, ${skipped_count} skipped, $((sim_number - skipped_count - completed)) running/queued"
                    fi
                done
            done
        done
    done
    
    # Wait for all background jobs to complete
    print_info "Waiting for all remaining simulations to complete..."
    wait
    
    # Count actual results
    local final_completed=$(find "${RESULTS_BASE}/archived_results" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
    success_count=$((final_completed - skipped_count))
    
    # Final summary
    print_header "Sweep Complete"
    
    echo ""
    print_info "Results:"
    print_info "  Total:        ${total_sims}"
    print_info "  Completed:    ${final_completed}/${total_sims}"
    if [[ ${skipped_count} -gt 0 ]]; then
        print_info "  Previously:   ${skipped_count}"
        print_info "  New:          ${success_count}"
    fi
    echo ""
    print_info "Results directory: ${RESULTS_BASE}"
    print_info "Master log:        ${MASTER_LOG}"
    print_info "Summary CSV:       ${SUMMARY_FILE}"
    echo ""
    
    print_header "Download Results"
    echo ""
    echo "  Summary CSV:"
    echo "    scp ${SERVER_USER}@${SERVER_HOST}:${SUMMARY_FILE} ."
    echo ""
    echo "  Full archive:"
    echo "    scp -r ${SERVER_USER}@${SERVER_HOST}:${RESULTS_BASE}/archived_results ."
    echo ""
    
    print_header "DONE - Parameter Sweep Complete"
}

# Run main function
main "$@"
