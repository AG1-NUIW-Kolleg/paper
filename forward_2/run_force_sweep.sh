#!/bin/bash
################################################################################
# Force Sweep for Forward Model Analysis
# 
# Runs systematic force sweep to analyze prestretch-ROM relationship
# Parameters varied:
# - FORCES: Range of prestretch forces (N)
# - MESH_SIZES: 4x4 and 8x8
# 
# Features:
# - Resume capability: Skips completed simulations
# - Parallel execution: Runs multiple simulations simultaneously
# - Progress tracking: Maintains logs and summary CSV
#
# Usage:
#   1. Upload to server: scp run_force_sweep.sh cmcs-fa01@cmcs09:~/
#   2. SSH to server: ssh cmcs-fa01@cmcs09.mathematik.uni-stuttgart.de
#   3. Run: bash run_force_sweep.sh [existing_results_dir] [max_parallel]
#
# Examples:
#   bash run_force_sweep.sh                          # Start new sweep
#   bash run_force_sweep.sh force_sweep_20251220 4   # Resume with 4 parallel jobs
#
# Author: Generated for forward model force analysis
# Date: 2025-12-20
################################################################################

set -e  # Exit on error

# Configuration
SERVER_USER="cmcs-fa01"
SERVER_HOST="cmcs09.mathematik.uni-stuttgart.de"
BASE_DIR="/usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular"
TEMPLATE_DIR="${BASE_DIR}/cuboid_prestretch_forforward/4x4"

# Command-line arguments
EXISTING_RESULTS_DIR="${1:-}"  # Optional: path to existing results directory to resume
MAX_PARALLEL="${2:-18}"          # Optional: max parallel simulations (default: 18)
TIMEOUT_MINUTES="${3:-15}"      # Optional: timeout per simulation in minutes (default: 15)

# Determine results directory
if [[ -n "${EXISTING_RESULTS_DIR}" ]]; then
    # Resume existing sweep
    if [[ "${EXISTING_RESULTS_DIR}" == /* ]]; then
        RESULTS_BASE="${EXISTING_RESULTS_DIR}"
    else
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
    RESULTS_BASE="${BASE_DIR}/force_sweep_$(date +%Y%m%d_%H%M%S)"
    RESUME_MODE=false
    echo "NEW SWEEP: Creating results directory: ${RESULTS_BASE}"
fi

# Parameter ranges
# ----------------

# Force values (Newtons) - comprehensive sweep from 0 to 35N
FORCES=(0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35)

# Mesh sizes: 4x4 and 8x8
MESH_SIZES=("4x4" "8x8")

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
    local mesh=$1
    local force=$2
    
    # Format force for directory name
    local force_int=${force%.*}
    local force_formatted=$(printf "%02d" "${force_int}")
    
    local exp_name="${mesh}_F${force_formatted}N"
    local archive_dir="${RESULTS_BASE}/archived_results/${exp_name}"
    
    # Check if result exists in archived_results with muscle_length_contraction.csv
    if [[ -d "${archive_dir}" ]] && [[ -f "${archive_dir}/muscle_length_contraction.csv" ]]; then
        return 0  # Completed
    else
        return 1  # Not completed
    fi
}

cleanup_incomplete_simulations() {
    print_info "Cleaning up incomplete simulations..."
    
    local cleaned=0
    for dir in "${RESULTS_BASE}"/{4x4,8x8}_F*; do
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
    local last_status_time=$(date +%s)
    while true; do
        local running_jobs=$(jobs -r | wc -l)
        if [[ ${running_jobs} -lt ${MAX_PARALLEL} ]]; then
            break
        fi
        
        # Print status every 30 seconds
        local current_time=$(date +%s)
        if [[ $((current_time - last_status_time)) -ge 30 ]]; then
            print_info "⏳ Waiting for slot... (${running_jobs}/${MAX_PARALLEL} jobs running)"
            check_for_timeouts
            last_status_time=${current_time}
        fi
        
        sleep 2
    done
}

check_for_timeouts() {
    # Check if any simulations have timed out
    local timeout_file="${RESULTS_BASE}/.timeouts"
    if [[ -f "${timeout_file}" ]]; then
        while read -r line; do
            [[ -z "${line}" ]] && continue
            local job_id=$(echo "${line}" | cut -d'|' -f1)
            local start_time=$(echo "${line}" | cut -d'|' -f2)
            
            local current_time=$(date +%s)
            local elapsed=$((current_time - start_time))
            local timeout_seconds=$((TIMEOUT_MINUTES * 60))
            
            if [[ ${elapsed} -gt ${timeout_seconds} ]]; then
                local elapsed_min=$((elapsed / 60))
                print_warning "⏱️  TIMEOUT WARNING: ${job_id} running for ${elapsed_min} min (limit: ${TIMEOUT_MINUTES} min)"
            fi
        done < "${timeout_file}"
    fi
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
    local mesh=$1
    local force=$2
    
    # Format force for directory name
    local force_int=${force%.*}
    local force_formatted=$(printf "%02d" "${force_int}")
    
    # Create experiment name
    local exp_name="${mesh}_F${force_formatted}N"
    local exp_dir="${RESULTS_BASE}/${exp_name}"
    
    # Create directory structure
    mkdir -p "${exp_dir}/build_release"
    
    # Copy necessary files from template
    cp "${TEMPLATE_DIR}/settings_muscle_with_prestretch.py" "${exp_dir}/" 2>/dev/null || true
    cp "${TEMPLATE_DIR}/helper.py" "${exp_dir}/" 2>/dev/null || true
    cp -r "${TEMPLATE_DIR}/variables" "${exp_dir}/" 2>/dev/null || true
    
    # Modify variables.py based on mesh size
    local variables_file="${exp_dir}/variables/variables.py"
    if [[ -f "${variables_file}" ]]; then
        # Update end_time to 100 ms
        sed -i.bak "s/^end_time = .*/end_time = ${ENDTIME_MS}/" "${variables_file}"
        
        # Set mesh-specific parameters
        if [[ "${mesh}" == "4x4" ]]; then
            # 4x4 mesh configuration (reduced model)
            sed -i.bak "s/^n_elements_muscle = .*/n_elements_muscle = [4, 4, 10]/" "${variables_file}"
            sed -i.bak "s/^n_points_whole_fiber = .*/n_points_whole_fiber = 30/" "${variables_file}"
            sed -i.bak "s/^n_fibers_x = .*/n_fibers_x = 3/" "${variables_file}"
            sed -i.bak "s/^n_fibers_y = .*/n_fibers_y = 3/" "${variables_file}"
        else
            # 8x8 mesh configuration (full resolution)
            sed -i.bak "s/^n_elements_muscle = .*/n_elements_muscle = [8, 8, 20]/" "${variables_file}"
            sed -i.bak "s/^n_points_whole_fiber = .*/n_points_whole_fiber = 60/" "${variables_file}"
            sed -i.bak "s/^n_fibers_x = .*/n_fibers_x = 6/" "${variables_file}"
            sed -i.bak "s/^n_fibers_y = .*/n_fibers_y = 6/" "${variables_file}"
        fi
        
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
# Force Sweep Simulation

## Parameters
- Mesh Size: ${mesh}
- Force: ${force} N
- Simulation Time: ${ENDTIME_MS} ms

## Created
- Date: $(date)
- Template: ${TEMPLATE_DIR}

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
    local mesh=$3
    
    # Change to build directory
    cd "${exp_dir}/build_release" || return 1
    
    local start_time=$(date +%s)
    echo "[$(date '+%H:%M:%S')] Starting simulation: ${mesh}_F${force}N" >> sim.log
    
    # Execute simulation - only show critical errors, save full log
    ./muscle_with_prestretch ../settings_muscle_with_prestretch.py ${force} 0 ${N_RANKS} > sim.log 2>&1
    
    local exit_code=$?
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    echo "[$(date '+%H:%M:%S')] Finished in ${duration}s (exit: ${exit_code})" >> sim.log
    
    if [ ${exit_code} -ne 0 ]; then
        print_error "Simulation failed with exit code ${exit_code} (after ${duration}s)"
        return ${exit_code}
    fi
    
    return 0
}

calculate_rom() {
    local csv_file=$1
    
    if [[ ! -f "${csv_file}" ]]; then
        echo "0,0,0"
        return
    fi
    
    # Read all values from CSV (comma-separated)
    local content=$(cat "${csv_file}")
    local values=(${content//,/ })
    
    # Find min and max
    local min=${values[0]}
    local max=${values[0]}
    
    for val in "${values[@]}"; do
        if (( $(echo "$val < $min" | bc -l) )); then
            min=$val
        fi
        if (( $(echo "$val > $max" | bc -l) )); then
            max=$val
        fi
    done
    
    # Calculate ROM
    local rom=$(echo "$max - $min" | bc -l)
    
    echo "$max,$min,$rom"
}

run_simulation_wrapper() {
    # Wrapper function to run simulation and handle results in background
    local mesh=$1
    local force=$2
    local sim_number=$3
    local total_sims=$4
    
    local start_time=$(date +%s)
    local job_id="${mesh}_F${force}N"
    
    # Create experiment directory
    local exp_dir=$(create_experiment_dir "${mesh}" "${force}")
    
    # Track this simulation for timeout monitoring (using job_id instead of PID)
    echo "${job_id}|${start_time}|${mesh}|${force}" >> "${RESULTS_BASE}/.timeouts"
    
    # Log to master
    {
        echo "=== Simulation ${sim_number}/${total_sims} ==="
        echo "Mesh=${mesh}, Force=${force}N"
        echo "Directory: $(basename ${exp_dir})"
        echo "Started: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "Job ID: ${job_id}"
    } >> "${MASTER_LOG}"
    
    # Print live status
    print_info "🚀 [${sim_number}/${total_sims}] Running: ${job_id}"
    
    # Run simulation
    if run_simulation "${force}" "${exp_dir}" "${mesh}"; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        # Save results
        save_results "${mesh}" "${force}" "${exp_dir}"
        
        # Extract ROM metrics for summary
        local contraction_file="${exp_dir}/build_release/muscle_length_contraction.csv"
        local prestretch_file="${exp_dir}/build_release/muscle_length_prestretch.csv"
        
        if [[ -f "${contraction_file}" ]]; then
            # Calculate ROM from contraction phase
            local rom_data=$(calculate_rom "${contraction_file}")
            local z_max=$(echo "${rom_data}" | cut -d',' -f1)
            local z_min=$(echo "${rom_data}" | cut -d',' -f2)
            local rom=$(echo "${rom_data}" | cut -d',' -f3)
            
            # Get initial and final prestretch length
            local initial_length="0"
            local final_length="0"
            if [[ -f "${prestretch_file}" ]]; then
                initial_length=$(head -1 "${prestretch_file}" | cut -d',' -f2)
                final_length=$(tail -1 "${prestretch_file}" | cut -d',' -f2)
            fi
            
            echo "${mesh},${force},${initial_length},${final_length},${z_max},${z_min},${rom},$(date)" >> "${SUMMARY_FILE}"
        fi
        
        echo "Status: SUCCESS" >> "${MASTER_LOG}"
        echo "Duration: ${duration}s" >> "${MASTER_LOG}"
        echo "Completed: $(date '+%Y-%m-%d %H:%M:%S')" >> "${MASTER_LOG}"
        echo "" >> "${MASTER_LOG}"
        
        # Remove from timeout tracking
        sed -i.bak "/^${job_id}|/d" "${RESULTS_BASE}/.timeouts" 2>/dev/null || true
        
        # Print completion status
        print_info "✅ [${sim_number}/${total_sims}] Completed: ${job_id} in ${duration}s"
        
        # Clean up experiment directory to save disk space
        rm -rf "${exp_dir}"
        
        return 0
    else
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        
        echo "Status: FAILED" >> "${MASTER_LOG}"
        echo "Duration: ${duration}s" >> "${MASTER_LOG}"
        echo "Completed: $(date '+%Y-%m-%d %H:%M:%S')" >> "${MASTER_LOG}"
        echo "" >> "${MASTER_LOG}"
        
        # Remove from timeout tracking
        sed -i.bak "/^${job_id}|/d" "${RESULTS_BASE}/.timeouts" 2>/dev/null || true
        
        # Print failure status
        print_error "❌ [${sim_number}/${total_sims}] Failed: ${job_id} after ${duration}s"
        
        return 1
    fi
}

save_results() {
    local mesh=$1
    local force=$2
    local exp_dir=$3
    
    # Format for archive directory
    local force_int=${force%.*}
    local force_formatted=$(printf "%02d" "${force_int}")
    
    local archive_name="${mesh}_F${force_formatted}N"
    local archive_dir="${RESULTS_BASE}/archived_results/${archive_name}"
    mkdir -p "${archive_dir}"
    
    # Copy essential result files
    cp "${exp_dir}/build_release/muscle_length_prestretch.csv" "${archive_dir}/" 2>/dev/null || true
    cp "${exp_dir}/build_release/muscle_length_contraction.csv" "${archive_dir}/" 2>/dev/null || true
    cp "${exp_dir}/build_release/sim.log" "${archive_dir}/" 2>/dev/null || true
    cp "${exp_dir}/settings_muscle_with_prestretch.py" "${archive_dir}/" 2>/dev/null || true
    cp "${exp_dir}/README.md" "${archive_dir}/" 2>/dev/null || true
    cp -r "${exp_dir}/variables" "${archive_dir}/" 2>/dev/null || true
    
    # Calculate ROM from contraction phase
    local contraction_file="${exp_dir}/build_release/muscle_length_contraction.csv"
    if [[ -f "${contraction_file}" ]]; then
        local rom_data=$(calculate_rom "${contraction_file}")
        local z_max=$(echo "${rom_data}" | cut -d',' -f1)
        local z_min=$(echo "${rom_data}" | cut -d',' -f2)
        local rom=$(echo "${rom_data}" | cut -d',' -f3)
        
        # Get prestretch info
        local prestretch_file="${exp_dir}/build_release/muscle_length_prestretch.csv"
        local initial_length="N/A"
        local final_length="N/A"
        if [[ -f "${prestretch_file}" ]]; then
            initial_length=$(head -1 "${prestretch_file}" | cut -d',' -f2)
            final_length=$(tail -1 "${prestretch_file}" | cut -d',' -f2)
        fi
        
        # Save ROM to file
        cat > "${archive_dir}/range_of_motion.txt" << EOF
z_max: ${z_max}
z_min: ${z_min}
ROM: ${rom}
num_timesteps: $(wc -w < "${contraction_file}" | tr -d ' ')
EOF
        
        # Save summary
        cat > "${archive_dir}/summary.txt" << EOF
Parameters:
-----------
Mesh Size: ${mesh}
Force: ${force} N
Simulation Time: ${ENDTIME_MS} ms

Prestretch Results:
------------------
Initial Length: ${initial_length} cm
Final Length (after prestretch): ${final_length} cm

Contraction Results:
-------------------
Maximum Muscle Length (z_max): ${z_max} cm
Minimum Muscle Length (z_min): ${z_min} cm
Range of Motion (ROM): ${rom} cm

Completed: $(date)
EOF
    fi
    
    return 0
}

################################################################################
# Main Script
################################################################################

main() {
    print_header "Force Sweep for Forward Model Analysis"
    
    # Calculate total simulations
    local total_sims=$((${#FORCES[@]} * ${#MESH_SIZES[@]}))
    
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
    print_info "  Timeout:      ${TIMEOUT_MINUTES} minutes per simulation"
    print_info "  Forces:       ${#FORCES[@]} values (0-35 N)"
    print_info "  Mesh Sizes:   ${#MESH_SIZES[@]} (4x4, 8x8)"
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
    MASTER_LOG="${RESULTS_BASE}/force_sweep_log.txt"
    SUMMARY_FILE="${RESULTS_BASE}/force_sweep_summary.csv"
    
    # Initialize timeout tracking file
    echo "" > "${RESULTS_BASE}/.timeouts"
    
    if [[ "${RESUME_MODE}" != "true" ]]; then
        # Create new logs
        echo "Force Sweep Started: $(date)" > "${MASTER_LOG}"
        echo "Total Simulations: ${total_sims}" >> "${MASTER_LOG}"
        echo "Parallel Jobs: ${MAX_PARALLEL}" >> "${MASTER_LOG}"
        echo "Timeout: ${TIMEOUT_MINUTES} minutes per simulation" >> "${MASTER_LOG}"
        echo "" >> "${MASTER_LOG}"
        
        echo "Mesh,Force_N,Initial_Length_cm,Final_Prestretch_Length_cm,z_max_cm,z_min_cm,ROM_cm,Completed_Date" > "${SUMMARY_FILE}"
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
    
    # Run simulations with parallelization
    print_header "Running Simulations (${MAX_PARALLEL} parallel jobs)"
    
    local skipped_count=0
    local sim_number=0
    
    # Nested loop: mesh -> force
    for mesh in "${MESH_SIZES[@]}"; do
        for force in "${FORCES[@]}"; do
            sim_number=$((sim_number + 1))
            
            # Check if simulation already completed
            if is_simulation_completed "${mesh}" "${force}"; then
                skipped_count=$((skipped_count + 1))
                print_info "Skipped ${sim_number}/${total_sims}: ${mesh} F=${force}N (already completed)"
                continue
            fi
            
            # Wait for available slot
            wait_for_slot
            
            # Print progress
            local running=$((sim_number - skipped_count))
            print_info "Starting ${sim_number}/${total_sims}: ${mesh} mesh, F=${force}N"
            
            # Launch simulation in background
            run_simulation_wrapper "${mesh}" "${force}" "${sim_number}" "${total_sims}" &
            
            # Small delay to avoid race conditions
            sleep 0.5
        done
    done
    
    # Wait for all background jobs to complete
    print_info "Waiting for all remaining simulations to complete..."
    wait
    
    # Count actual results
    local final_completed=$(find "${RESULTS_BASE}/archived_results" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
    
    # Final summary
    print_header "Sweep Complete"
    
    echo ""
    print_info "Results:"
    print_info "  Total:        ${total_sims}"
    print_info "  Completed:    ${final_completed}/${total_sims}"
    if [[ ${skipped_count} -gt 0 ]]; then
        print_info "  Previously:   ${skipped_count}"
        print_info "  New:          $((final_completed - skipped_count))"
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
    
    print_header "DONE - Force Sweep Complete"
}

# Run main function
main "$@"
