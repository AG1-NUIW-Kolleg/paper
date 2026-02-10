#!/bin/bash
################################################################################
# Multi-Parameter Sweep for Data Augmentation
# 
# Runs comprehensive parameter sweep for muscle prestretch simulations
# Parameters varied:
# FORCES=(0 3 6 9 12 15 18 21 24 27 30 31)
# MUSCLE_Y_VALUES=(32.69 33.19 33.69 34.19 34.97)
# VOLUME_VALUES=(421.6 455.9 514.7 573.5 632.3 691.2 738.0)
# AM_VALUES=(450 500 550)
# RHO_VALUES=(10.493 10.534 10.575 10.616)
# 
# Features:
# - Resume capability: Skips completed simulations in archived_results
# - Parallel execution: Runs multiple simulations simultaneously
# - Progress tracking: Maintains master log and summary CSV
#
# Usage:
#   1. Upload to server: scp run_parameter_sweep.sh cmcs-fa01@cmcs09:~/
#   2. SSH to server: ssh cmcs-fa01@cmcs09.mathematik.uni-stusttgart.de
#   3. Run: bash run_parameter_sweep.sh [existing_results_dir] [max_parallel]
#
# Examples:
#   bash run_parameter_sweep.sh  # Start new sweep
#   bash run_parameter_sweep.sh parameter_sweep_DA_20251202_130337  # Resume existing
#   bash run_parameter_sweep.sh parameter_sweep_DA_20251202_130337 4  # Resume with 4 parallel jobs
#
# Author: Generated for data augmentation study
# Date: 2025-12-02
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

# 1. Force values (Newtons) -
FORCES=(0 3 6 9 12 15 18 21 24 27 30 31)

# 2. muscle_extent_y values (cm)
MUSCLE_Y_VALUES=(32.69 33.19 33.69 34.19 34.97)

# 3. Volume values (cm³)
VOLUME_VALUES=(421.6 455.9 514.7 573.5 632.3 691.2 738.0)

# 4. Am values (surface area to volume ratio) - [cm⁻¹]
AM_VALUES=(450 500 550)

# 5. Rho values (density) - [1e-4 kg/cm³]
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
    local force=$1
    local muscle_y=$2
    local volume=$3
    local am=$4
    local rho=$5
    
    # Format parameters for directory name (same logic as create_experiment_dir)
    local force_int=${force%.*}
    local force_formatted=$(printf "%02d" "${force_int}")
    local muscle_y_formatted="${muscle_y}"
    local volume_formatted="${volume}"
    local am_int=${am%.*}
    local rho_formatted="${rho}"
    
    local exp_name="F${force_formatted}_y${muscle_y_formatted}_Vol${volume_formatted}_Am${am_int}_rho${rho_formatted}"
    
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
    local force=$1
    local muscle_y=$2
    local volume=$3
    local am=$4
    local rho=$5
    
    # Calculate muscle_x from volume and y: x = sqrt(Vol/y)
    local muscle_x=$(echo "scale=6; sqrt(${volume} / ${muscle_y})" | bc -l)
    
    # Format parameters for directory name
    local force_int=${force%.*}
    local force_formatted=$(printf "%02d" "${force_int}")
    # Use string substitution for floats (printf doesn't support floats in bash)
    local muscle_y_formatted="${muscle_y}"
    local volume_formatted="${volume}"
    local muscle_x_formatted="${muscle_x}"
    local am_int=${am%.*}
    local rho_formatted="${rho}"
    
    # Create experiment name with all parameters
    local exp_name="F${force_formatted}_y${muscle_y_formatted}_Vol${volume_formatted}_Am${am_int}_rho${rho_formatted}"
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
        # Update muscle_extent with calculated x and given y
        sed -i.bak "s/^muscle_extent = .*/muscle_extent = [${muscle_x}, ${muscle_x}, ${muscle_y}]  # [cm, cm, cm] - Vol=${volume} cm^3/" "${variables_file}"
        
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
# Parameter Sweep Simulation

## Parameters
- Force: ${force} N
- muscle_extent: [${muscle_x}, ${muscle_x}, ${muscle_y}] cm
- Volume: ${volume} cm³
- Am: ${am} cm⁻¹
- Rho: ${rho} [1e-4 kg/cm³]
- Simulation Time: ${ENDTIME_MS} ms

## Created
- Date: $(date)
- Template: ${TEMPLATE_DIR}

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(${volume}/${muscle_y}) = ${muscle_x} cm

## Run Command
\`\`\`bash
cd ${exp_dir}/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py ${force} 0 ${N_RANKS}
\`\`\`
EOF
    
    echo "${exp_dir}"
}

run_simulation() {
    local force=$1
    local exp_dir=$2
    local muscle_y=$3
    local volume=$4
    local am=$5
    local rho=$6
    
    # Change to build directory
    cd "${exp_dir}/build_release" || return 1
    
    # Execute simulation (suppress most output to avoid log overflow)
    ./muscle_with_prestretch ../settings_muscle_with_prestretch.py ${force} 0 ${N_RANKS} > sim.log 2>&1
    
    local exit_code=$?
    
    if [ ${exit_code} -ne 0 ]; then
        print_error "Simulation failed with exit code ${exit_code}"
        return ${exit_code}
    fi
    
    return 0
}

run_simulation_wrapper() {
    # Wrapper function to run simulation and handle results in background
    local force=$1
    local muscle_y=$2
    local volume=$3
    local am=$4
    local rho=$5
    local sim_number=$6
    local total_sims=$7
    
    # Create experiment directory
    local exp_dir=$(create_experiment_dir "${force}" "${muscle_y}" "${volume}" "${am}" "${rho}")
    
    # Calculate muscle_x for logging
    local muscle_x=$(echo "scale=6; sqrt(${volume} / ${muscle_y})" | bc -l)
    
    # Log to master
    {
        echo "=== Simulation ${sim_number}/${total_sims} ===" 
        echo "F=${force}, y=${muscle_y}, x=${muscle_x}, Vol=${volume}, Am=${am}, rho=${rho}"
        echo "Directory: $(basename ${exp_dir})"
        echo "Started: $(date)"
    } >> "${MASTER_LOG}"
    
    # Run simulation
    if run_simulation "${force}" "${exp_dir}" "${muscle_y}" "${volume}" "${am}" "${rho}"; then
        # Save results
        save_results "${force}" "${exp_dir}" "${muscle_y}" "${volume}" "${am}" "${rho}"
        
        # Extract metrics for summary
        local prestretch_file="${exp_dir}/build_release/muscle_length_prestretch.csv"
        if [[ -f "${prestretch_file}" ]]; then
            local final_length=$(tail -1 "${prestretch_file}" | cut -d',' -f2)
            local elongation=$(echo "${final_length} - ${muscle_y}" | bc -l)
            local strain=$(echo "scale=6; ${elongation} / ${muscle_y}" | bc -l)
            echo "${force},${muscle_y},${muscle_x},${volume},${am},${rho},${muscle_y},${final_length},${elongation},${strain},$(date)" >> "${SUMMARY_FILE}"
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
    local force=$1
    local exp_dir=$2
    local muscle_y=$3
    local volume=$4
    local am=$5
    local rho=$6
    
    # Calculate muscle_x
    local muscle_x=$(echo "scale=6; sqrt(${volume} / ${muscle_y})" | bc -l)
    
    # Format for archive directory
    local force_int=${force%.*}
    local force_formatted=$(printf "%02d" "${force_int}")
    # Use string substitution for floats (printf doesn't support floats in bash)
    local muscle_y_formatted="${muscle_y}"
    local volume_formatted="${volume}"
    local am_int=${am%.*}
    local rho_formatted="${rho}"
    
    local archive_name="F${force_formatted}_y${muscle_y_formatted}_Vol${volume_formatted}_Am${am_int}_rho${rho_formatted}"
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
        local elongation=$(echo "${final_length} - ${muscle_y}" | bc -l)
        local strain=$(echo "scale=6; ${elongation} / ${muscle_y}" | bc -l)
        
        # Save summary
        cat > "${archive_dir}/summary.txt" << EOF
Parameters:
-----------
Force: ${force} N
muscle_extent: [${muscle_x}, ${muscle_x}, ${muscle_y}] cm
Volume: ${volume} cm³
Am: ${am} cm⁻¹
Rho: ${rho} [1e-4 kg/cm³]

Results:
--------
Initial Length: ${muscle_y} cm
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
    print_header "Multi-Parameter Sweep for Data Augmentation"
    
    # Calculate total simulations
    local total_sims=$((${#FORCES[@]} * ${#MUSCLE_Y_VALUES[@]} * ${#VOLUME_VALUES[@]} * ${#AM_VALUES[@]} * ${#RHO_VALUES[@]}))
    
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
    print_info "  Forces:       ${#FORCES[@]} values (0-31 N)"
    print_info "  muscle_y:     ${#MUSCLE_Y_VALUES[@]} values (32.69-34.97 cm)"
    print_info "  Volumes:      ${#VOLUME_VALUES[@]} values (421.6-738 cm³)"
    print_info "  Am:           ${#AM_VALUES[@]} values (450-550 cm⁻¹)"
    print_info "  Rho:          ${#RHO_VALUES[@]} values (10.493-10.616)"
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
        echo "Total Simulations: ${total_sims}" >> "${MASTER_LOG}"
        echo "Parallel Jobs: ${MAX_PARALLEL}" >> "${MASTER_LOG}"
        echo "" >> "${MASTER_LOG}"
        
        echo "Force_N,muscle_y_cm,muscle_x_cm,Volume_cm3,Am,Rho,Initial_Length_cm,Final_Length_cm,Elongation_cm,Strain,Completed_Date" > "${SUMMARY_FILE}"
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
    
    # Run simulations with 5-nested loop and parallelization
    print_header "Running Simulations (${MAX_PARALLEL} parallel jobs)"
    
    local success_count=0
    local failure_count=0
    local skipped_count=0
    local sim_number=0
    
    # 5-nested loop: rho -> Am -> Volume -> muscle_y -> force
    for rho in "${RHO_VALUES[@]}"; do
        for am in "${AM_VALUES[@]}"; do
            for volume in "${VOLUME_VALUES[@]}"; do
                for muscle_y in "${MUSCLE_Y_VALUES[@]}"; do
                    for force in "${FORCES[@]}"; do
                        sim_number=$((sim_number + 1))
                        
                        # Check if simulation already completed
                        if is_simulation_completed "${force}" "${muscle_y}" "${volume}" "${am}" "${rho}"; then
                            skipped_count=$((skipped_count + 1))
                            
                            # Print progress every 50 skips
                            if [ $((skipped_count % 50)) -eq 0 ]; then
                                print_info "Skipped ${skipped_count} completed simulations..."
                            fi
                            continue
                        fi
                        
                        # Wait for available slot
                        wait_for_slot
                        
                        # Calculate muscle_x for display
                        muscle_x=$(echo "scale=6; sqrt(${volume} / ${muscle_y})" | bc -l)
                        
                        # Print progress
                        local running=$((sim_number - skipped_count - success_count - failure_count))
                        print_info "Starting ${sim_number}/${total_sims}: F=${force}N, y=${muscle_y}, Vol=${volume}, Am=${am}, ρ=${rho} (${running} running)"
                        
                        # Launch simulation in background
                        run_simulation_wrapper "${force}" "${muscle_y}" "${volume}" "${am}" "${rho}" "${sim_number}" "${total_sims}" &
                        
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
