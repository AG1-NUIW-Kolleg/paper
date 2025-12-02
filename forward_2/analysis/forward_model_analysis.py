#!/usr/bin/env python3
"""
Analysis Script for Forward Model Chapter 2
============================================

This script analyzes the mesh resolution comparison for the forward model:
- 4x4 mesh vs 8x8 mesh
- Prestretch forces: 0N and 31N
- Computes ROM (Range of Motion) correlation
- Computes runtime reduction
- Generates all required plots and statistics

Author: Analysis for Data Package
Date: 2025-12-01
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import json

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# =============================================================================
# Configuration
# =============================================================================

BASE_DIR = "/Users/canis/Library/CloudStorage/OneDrive-Persönlich/work/SdV/natwissKolleg/results/final_results/results_for_paper/forward_2"

RESULTS_PATHS = {
    '4x4_0N': os.path.join(BASE_DIR, '4x4/4x4_0N/build_release'),
    '4x4_31N': os.path.join(BASE_DIR, '4x4/4x4_31N/build_release'),
    '8x8_0N': os.path.join(BASE_DIR, '8x8/8x8_0N/build_release'),
    '8x8_31N': os.path.join(BASE_DIR, '8x8/8x8_31N/build_release'),
}

AMI_PATH = os.path.join(BASE_DIR, 'ami/build_release')

OUTPUT_DIR = os.path.join(BASE_DIR, 'analysis')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =============================================================================
# Data Loading Functions
# =============================================================================

def load_muscle_length(path, experiment):
    """Load muscle length from prestretch CSV"""
    csv_file = os.path.join(path, 'muscle_length_prestretch.csv')
    if os.path.exists(csv_file):
        # Read CSV without headers
        with open(csv_file, 'r') as f:
            line = f.readline().strip()
            if line:
                values = line.rstrip(',').split(',')
                if len(values) >= 2:
                    initial_length = float(values[0])
                    final_length = float(values[1])
                    return {
                        'experiment': experiment,
                        'initial_length': initial_length,
                        'final_length': final_length,
                        'elongation': final_length - initial_length,
                        'strain': (final_length - initial_length) / initial_length
                    }
    return None

def load_runtime(path, experiment):
    """Load runtime from log.csv"""
    log_file = os.path.join(path, 'logs/log.csv')
    if os.path.exists(log_file):
        try:
            # Read all lines
            with open(log_file, 'r') as f:
                lines = f.readlines()
            
            # Find header and all data lines
            header_line = None
            data_lines = []
            for line in lines:
                if line.startswith('# timestamp'):
                    header_line = line[2:].strip()  # Remove '# ' prefix
                elif not line.startswith('#') and line.strip():
                    data_lines.append(line.strip())
            
            if header_line and data_lines:
                headers = header_line.split(';')
                
                # Try to find a line with "normal" exit (completed simulation)
                # Otherwise use the last line
                data_line = None
                if 'exit' in headers:
                    exit_idx = headers.index('exit')
                    for line in reversed(data_lines):
                        values = line.split(';')
                        if len(values) > exit_idx and values[exit_idx] == 'normal':
                            data_line = line
                            break
                
                # If no normal exit found, use last line
                if data_line is None:
                    data_line = data_lines[-1]
                
                # Parse the selected line
                values = data_line.split(';')
                
                # Find totalUsertime column
                if 'totalUsertime' in headers:
                    idx = headers.index('totalUsertime')
                    if len(values) > idx:
                        runtime = float(values[idx])
                        return {
                            'experiment': experiment,
                            'runtime_seconds': runtime,
                            'runtime_minutes': runtime / 60.0,
                            'runtime_hours': runtime / 3600.0
                        }
        except Exception as e:
            print(f"  Warning: Could not load runtime for {experiment}: {e}")
    return None

def load_all_data():
    """Load all experimental data"""
    results = []
    runtimes = []
    
    for exp_name, path in RESULTS_PATHS.items():
        # Load muscle length data
        muscle_data = load_muscle_length(path, exp_name)
        if muscle_data:
            results.append(muscle_data)
        
        # Load runtime data
        runtime_data = load_runtime(path, exp_name)
        if runtime_data:
            runtimes.append(runtime_data)
    
    return pd.DataFrame(results), pd.DataFrame(runtimes)

def load_tendon_positions(ami_path):
    """Load tendon positions from AMI simulation (up to 10 ms)"""
    tendon_file = os.path.join(ami_path, 'defaulttendon.txt')
    if os.path.exists(tendon_file):
        data = []
        with open(tendon_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split()
                    if len(parts) >= 3:
                        time = float(parts[0])
                        if time <= 10.0:  # Only analyze up to 10 ms
                            pos_left = float(parts[1])
                            pos_right = float(parts[2])
                            data.append({
                                'time_ms': time,
                                'pos_left': pos_left,
                                'pos_right': pos_right,
                                'tendon_length': pos_right - pos_left
                            })
        return pd.DataFrame(data)
    return None

# =============================================================================
# Analysis Functions
# =============================================================================

def compute_rom_correlation(df_results):
    """Compute ROM correlation between 4x4 and 8x8 meshes"""
    # Extract ROM values for each mesh resolution
    rom_4x4 = []
    rom_8x8 = []
    
    for force in ['0N', '31N']:
        rom_4x4.append(df_results[df_results['experiment'] == f'4x4_{force}']['final_length'].values[0])
        rom_8x8.append(df_results[df_results['experiment'] == f'8x8_{force}']['final_length'].values[0])
    
    # Compute correlation (R²)
    correlation = np.corrcoef(rom_4x4, rom_8x8)[0, 1]
    r_squared = correlation ** 2
    
    # Linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(rom_4x4, rom_8x8)
    
    return {
        'correlation': correlation,
        'r_squared': r_squared,
        'slope': slope,
        'intercept': intercept,
        'p_value': p_value,
        'rom_4x4': rom_4x4,
        'rom_8x8': rom_8x8
    }

def compute_runtime_reduction(df_runtimes):
    """Compute runtime reduction from 8x8 to 4x4"""
    # Average runtime for 4x4 and 8x8
    runtime_4x4_avg = df_runtimes[df_runtimes['experiment'].str.contains('4x4')]['runtime_seconds'].mean()
    runtime_8x8_avg = df_runtimes[df_runtimes['experiment'].str.contains('8x8')]['runtime_seconds'].mean()
    
    # Reduction percentage
    reduction_percent = ((runtime_8x8_avg - runtime_4x4_avg) / runtime_8x8_avg) * 100
    
    return {
        'runtime_4x4_avg_seconds': runtime_4x4_avg,
        'runtime_8x8_avg_seconds': runtime_8x8_avg,
        'runtime_4x4_avg_minutes': runtime_4x4_avg / 60.0,
        'runtime_8x8_avg_minutes': runtime_8x8_avg / 60.0,
        'reduction_percent': reduction_percent,
        'speedup_factor': runtime_8x8_avg / runtime_4x4_avg
    }

def compute_rom_values(df_results):
    """Compute ROM for each configuration"""
    rom_data = []
    
    for exp in df_results['experiment'].unique():
        row = df_results[df_results['experiment'] == exp].iloc[0]
        rom_data.append({
            'experiment': exp,
            'mesh': exp.split('_')[0],
            'force': exp.split('_')[1],
            'initial_length_cm': row['initial_length'],
            'final_length_cm': row['final_length'],
            'elongation_cm': row['elongation'],
            'strain': row['strain'],
            'ROM_cm': row['final_length']  # ROM is the final muscle length
        })
    
    return pd.DataFrame(rom_data)

def analyze_tendon_compliance(df_tendon):
    """Analyze tendon compliance from position data"""
    if df_tendon is None or len(df_tendon) == 0:
        return None
    
    initial_length = df_tendon['tendon_length'].iloc[0]
    max_deviation = (df_tendon['tendon_length'] - initial_length).abs().max()
    
    return {
        'initial_length': initial_length,
        'max_deviation': max_deviation,
        'max_deviation_percent': (max_deviation / initial_length) * 100
    }

# =============================================================================
# Visualization Functions
# =============================================================================

def plot_rom_correlation(rom_analysis, output_dir):
    """Plot ROM correlation between 4x4 and 8x8"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    rom_4x4 = rom_analysis['rom_4x4']
    rom_8x8 = rom_analysis['rom_8x8']
    r_squared = rom_analysis['r_squared']
    
    # Scatter plot
    ax.scatter(rom_4x4, rom_8x8, s=200, alpha=0.7, edgecolors='black', linewidth=2)
    
    # Add labels for each point
    labels = ['0N', '31N']
    for i, label in enumerate(labels):
        ax.annotate(label, (rom_4x4[i], rom_8x8[i]), 
                   fontsize=12, fontweight='bold',
                   xytext=(10, 10), textcoords='offset points')
    
    # Regression line
    x_line = np.array([min(rom_4x4) - 1, max(rom_4x4) + 1])
    y_line = rom_analysis['slope'] * x_line + rom_analysis['intercept']
    ax.plot(x_line, y_line, 'r--', linewidth=2, label=f'Linear Fit (R² = {r_squared:.4f})')
    
    # Perfect correlation line
    ax.plot(x_line, x_line, 'k:', linewidth=1, alpha=0.5, label='Perfect Correlation')
    
    ax.set_xlabel('ROM 4x4 Mesh [cm]', fontsize=14, fontweight='bold')
    ax.set_ylabel('ROM 8x8 Mesh [cm]', fontsize=14, fontweight='bold')
    ax.set_title('Range of Motion Correlation: 4x4 vs 8x8 Mesh', fontsize=16, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'rom_correlation_4x4_vs_8x8.png'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'rom_correlation_4x4_vs_8x8.pdf'), bbox_inches='tight')
    plt.close()

def plot_rom_comparison_bar(df_rom, output_dir):
    """Bar plot comparing ROM values"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Prepare data
    meshes = ['4x4', '8x8']
    forces = ['0N', '31N']
    x = np.arange(len(forces))
    width = 0.35
    
    rom_4x4 = [df_rom[(df_rom['mesh'] == '4x4') & (df_rom['force'] == f)]['ROM_cm'].values[0] for f in forces]
    rom_8x8 = [df_rom[(df_rom['mesh'] == '8x8') & (df_rom['force'] == f)]['ROM_cm'].values[0] for f in forces]
    
    bars1 = ax.bar(x - width/2, rom_4x4, width, label='4x4 Mesh', alpha=0.8, edgecolor='black')
    bars2 = ax.bar(x + width/2, rom_8x8, width, label='8x8 Mesh', alpha=0.8, edgecolor='black')
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_xlabel('Prestretch Force', fontsize=14, fontweight='bold')
    ax.set_ylabel('Range of Motion [cm]', fontsize=14, fontweight='bold')
    ax.set_title('ROM Comparison: 4x4 vs 8x8 Mesh Resolution', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(forces)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'rom_comparison_bar.png'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'rom_comparison_bar.pdf'), bbox_inches='tight')
    plt.close()

def plot_runtime_comparison(df_runtimes, runtime_stats, output_dir):
    """Plot runtime comparison"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot 1: Bar chart of individual runtimes
    experiments = df_runtimes['experiment'].values
    runtimes_min = df_runtimes['runtime_minutes'].values
    colors = ['#1f77b4' if '4x4' in exp else '#ff7f0e' for exp in experiments]
    
    bars = ax1.bar(range(len(experiments)), runtimes_min, color=colors, alpha=0.8, edgecolor='black')
    ax1.set_xlabel('Experiment', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Runtime [minutes]', fontsize=14, fontweight='bold')
    ax1.set_title('Runtime Comparison by Experiment', fontsize=16, fontweight='bold')
    ax1.set_xticks(range(len(experiments)))
    ax1.set_xticklabels(experiments, rotation=45, ha='right')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Plot 2: Average runtime comparison
    avg_4x4 = runtime_stats['runtime_4x4_avg_minutes']
    avg_8x8 = runtime_stats['runtime_8x8_avg_minutes']
    reduction = runtime_stats['reduction_percent']
    
    meshes = ['4x4', '8x8']
    avg_runtimes = [avg_4x4, avg_8x8]
    colors2 = ['#1f77b4', '#ff7f0e']
    
    bars2 = ax2.bar(meshes, avg_runtimes, color=colors2, alpha=0.8, edgecolor='black')
    ax2.set_xlabel('Mesh Resolution', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Average Runtime [minutes]', fontsize=14, fontweight='bold')
    ax2.set_title(f'Average Runtime Comparison\n(Reduction: {reduction:.1f}%)', fontsize=16, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add value labels and reduction arrow
    for i, bar in enumerate(bars2):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f} min',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Add reduction annotation
    ax2.annotate('', xy=(0.5, avg_4x4), xytext=(1.5, avg_8x8),
                arrowprops=dict(arrowstyle='<->', lw=2, color='red'))
    ax2.text(1.0, (avg_4x4 + avg_8x8) / 2, f'{reduction:.1f}%\nreduction',
            ha='center', va='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='red', linewidth=2))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'runtime_comparison.png'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'runtime_comparison.pdf'), bbox_inches='tight')
    plt.close()

def plot_elongation_comparison(df_rom, output_dir):
    """Plot elongation/strain comparison"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Prepare data
    forces = ['0N', '31N']
    x = np.arange(len(forces))
    width = 0.35
    
    elongation_4x4 = [df_rom[(df_rom['mesh'] == '4x4') & (df_rom['force'] == f)]['elongation_cm'].values[0] for f in forces]
    elongation_8x8 = [df_rom[(df_rom['mesh'] == '8x8') & (df_rom['force'] == f)]['elongation_cm'].values[0] for f in forces]
    
    strain_4x4 = [df_rom[(df_rom['mesh'] == '4x4') & (df_rom['force'] == f)]['strain'].values[0] for f in forces]
    strain_8x8 = [df_rom[(df_rom['mesh'] == '8x8') & (df_rom['force'] == f)]['strain'].values[0] for f in forces]
    
    # Plot 1: Elongation
    bars1 = ax1.bar(x - width/2, elongation_4x4, width, label='4x4 Mesh', alpha=0.8, edgecolor='black')
    bars2 = ax1.bar(x + width/2, elongation_8x8, width, label='8x8 Mesh', alpha=0.8, edgecolor='black')
    
    ax1.set_xlabel('Prestretch Force', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Elongation [cm]', fontsize=14, fontweight='bold')
    ax1.set_title('Muscle Elongation Comparison', fontsize=16, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(forces)
    ax1.legend(fontsize=12)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.3f}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Plot 2: Strain
    bars3 = ax2.bar(x - width/2, strain_4x4, width, label='4x4 Mesh', alpha=0.8, edgecolor='black')
    bars4 = ax2.bar(x + width/2, strain_8x8, width, label='8x8 Mesh', alpha=0.8, edgecolor='black')
    
    ax2.set_xlabel('Prestretch Force', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Strain', fontsize=14, fontweight='bold')
    ax2.set_title('Muscle Strain Comparison', fontsize=16, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(forces)
    ax2.legend(fontsize=12)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bars in [bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.5f}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'elongation_strain_comparison.png'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'elongation_strain_comparison.pdf'), bbox_inches='tight')
    plt.close()

def plot_tendon_compliance(df_tendon, tendon_stats, output_dir):
    """Plot tendon length over time"""
    if df_tendon is None or len(df_tendon) == 0:
        return
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.plot(df_tendon['time_ms'], df_tendon['tendon_length'], 'b-', linewidth=2, label='Tendon Length')
    ax.axhline(y=tendon_stats['initial_length'], color='r', linestyle='--', linewidth=2, 
               label=f"Initial Length = {tendon_stats['initial_length']:.3f} cm")
    
    # Set y-axis limits to show the full context (0 to initial_length + margin)
    y_min = max(0, tendon_stats['initial_length'] - 1.0)
    y_max = tendon_stats['initial_length'] + 1.0
    ax.set_ylim(y_min, y_max)
    
    ax.set_xlabel('Time [ms]', fontsize=14, fontweight='bold')
    ax.set_ylabel('Tendon Length [cm]', fontsize=14, fontweight='bold')
    ax.set_title('Tendon Compliance Analysis (AMI Model, 0-10 ms)', fontsize=16, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Add annotation for max deviation
    ax.text(0.98, 0.02, f"Max Deviation: {tendon_stats['max_deviation']:.4f} cm ({tendon_stats['max_deviation_percent']:.2f}%)",
            transform=ax.transAxes, fontsize=12, fontweight='bold',
            ha='right', va='bottom',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='black', linewidth=2))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'tendon_compliance_analysis.png'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'tendon_compliance_analysis.pdf'), bbox_inches='tight')
    plt.close()

# =============================================================================
# Report Generation
# =============================================================================

def generate_summary_report(df_results, df_runtimes, rom_analysis, runtime_stats, df_rom, tendon_stats, output_dir):
    """Generate comprehensive summary report"""
    
    report = []
    report.append("=" * 80)
    report.append("FORWARD MODEL ANALYSIS - MESH RESOLUTION COMPARISON")
    report.append("=" * 80)
    report.append("")
    report.append(f"Analysis Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # ROM Results
    report.append("-" * 80)
    report.append("1. RANGE OF MOTION (ROM) ANALYSIS")
    report.append("-" * 80)
    report.append("")
    report.append("ROM Values:")
    for _, row in df_rom.iterrows():
        report.append(f"  {row['experiment']:12s}: Initial={row['initial_length_cm']:.3f} cm, "
                     f"Final={row['final_length_cm']:.3f} cm, ROM={row['ROM_cm']:.3f} cm")
    report.append("")
    report.append("ROM Correlation (4x4 vs 8x8):")
    report.append(f"  Pearson Correlation: r = {rom_analysis['correlation']:.6f}")
    report.append(f"  R-squared:           R² = {rom_analysis['r_squared']:.6f}")
    report.append(f"  p-value:             p = {rom_analysis['p_value']:.6e}")
    report.append(f"  Linear Fit:          y = {rom_analysis['slope']:.6f}x + {rom_analysis['intercept']:.6f}")
    report.append("")
    
    # Elongation/Strain
    report.append("Elongation and Strain:")
    for _, row in df_rom.iterrows():
        report.append(f"  {row['experiment']:12s}: Elongation={row['elongation_cm']:.6f} cm, "
                     f"Strain={row['strain']:.8f}")
    report.append("")
    
    # Runtime Results
    report.append("-" * 80)
    report.append("2. RUNTIME ANALYSIS")
    report.append("-" * 80)
    report.append("")
    report.append("Individual Runtimes:")
    for _, row in df_runtimes.iterrows():
        report.append(f"  {row['experiment']:12s}: {row['runtime_seconds']:.2f} s "
                     f"({row['runtime_minutes']:.2f} min)")
    report.append("")
    report.append("Average Runtimes:")
    report.append(f"  4x4 Mesh: {runtime_stats['runtime_4x4_avg_seconds']:.2f} s "
                 f"({runtime_stats['runtime_4x4_avg_minutes']:.2f} min)")
    report.append(f"  8x8 Mesh: {runtime_stats['runtime_8x8_avg_seconds']:.2f} s "
                 f"({runtime_stats['runtime_8x8_avg_minutes']:.2f} min)")
    report.append("")
    report.append(f"Runtime Reduction: {runtime_stats['reduction_percent']:.2f}%")
    report.append(f"Speedup Factor:    {runtime_stats['speedup_factor']:.2f}x")
    report.append("")
    
    # Tendon Compliance
    if tendon_stats is not None:
        report.append("-" * 80)
        report.append("3. TENDON COMPLIANCE ANALYSIS (AMI MODEL)")
        report.append("-" * 80)
        report.append("")
        report.append(f"Initial Tendon Length:  {tendon_stats['initial_length']:.4f} cm")
        report.append(f"Maximum Deviation:      {tendon_stats['max_deviation']:.4f} cm")
        report.append(f"Deviation Percentage:   {tendon_stats['max_deviation_percent']:.2f}%")
        report.append("")
    
    # Key Findings for Paper
    report.append("-" * 80)
    key_section = "4. KEY FINDINGS FOR PAPER" if tendon_stats else "3. KEY FINDINGS FOR PAPER"
    report.append(key_section)
    report.append("-" * 80)
    report.append("")
    report.append(f"✓ ROM Correlation:   R² > {rom_analysis['r_squared']:.4f}")
    report.append(f"✓ Runtime Reduction: {runtime_stats['reduction_percent']:.1f}% "
                 f"({runtime_stats['runtime_8x8_avg_minutes']:.1f} min vs "
                 f"{runtime_stats['runtime_4x4_avg_minutes']:.1f} min)")
    if tendon_stats:
        report.append(f"✓ Tendon Compliance: Max deviation {tendon_stats['max_deviation']:.4f} cm "
                     f"({tendon_stats['max_deviation_percent']:.2f}%)")
    report.append("")
   
    report.append("=" * 80)
    
    # Save report
    report_text = "\n".join(report)
    with open(os.path.join(output_dir, 'analysis_summary.txt'), 'w') as f:
        f.write(report_text)
    
    print(report_text)
    
    return report_text

def save_data_tables(df_results, df_runtimes, df_rom, output_dir):
    """Save data tables as CSV and LaTeX"""
    
    # Save ROM data
    df_rom.to_csv(os.path.join(output_dir, 'rom_data.csv'), index=False)
    df_rom.to_latex(os.path.join(output_dir, 'rom_data.tex'), index=False, float_format="%.6f")
    
    # Save runtime data
    df_runtimes.to_csv(os.path.join(output_dir, 'runtime_data.csv'), index=False)
    df_runtimes.to_latex(os.path.join(output_dir, 'runtime_data.tex'), index=False, float_format="%.2f")
    
    # Save complete results
    df_results.to_csv(os.path.join(output_dir, 'complete_results.csv'), index=False)
    df_results.to_latex(os.path.join(output_dir, 'complete_results.tex'), index=False, float_format="%.6f")

def save_json_results(rom_analysis, runtime_stats, tendon_stats, output_dir):
    """Save results as JSON for easy integration"""
    
    results_json = {
        'rom_correlation': {
            'r_squared': float(rom_analysis['r_squared']),
            'correlation': float(rom_analysis['correlation']),
            'p_value': float(rom_analysis['p_value']),
            'slope': float(rom_analysis['slope']),
            'intercept': float(rom_analysis['intercept'])
        },
        'runtime_reduction': {
            'reduction_percent': float(runtime_stats['reduction_percent']),
            'runtime_4x4_minutes': float(runtime_stats['runtime_4x4_avg_minutes']),
            'runtime_8x8_minutes': float(runtime_stats['runtime_8x8_avg_minutes']),
            'speedup_factor': float(runtime_stats['speedup_factor'])
        },
        'suggested_values_for_paper': {
            'r_squared_threshold': f"> {rom_analysis['r_squared']:.4f}",
            'runtime_reduction_percent': f"{runtime_stats['reduction_percent']:.1f}%",
            'runtime_comparison': f"{runtime_stats['runtime_4x4_avg_minutes']:.1f} min vs {runtime_stats['runtime_8x8_avg_minutes']:.1f} min"
        }
    }
    
    if tendon_stats is not None:
        results_json['tendon_compliance'] = {
            'initial_length_cm': float(tendon_stats['initial_length']),
            'max_deviation_cm': float(tendon_stats['max_deviation']),
            'max_deviation_percent': float(tendon_stats['max_deviation_percent'])
        }
        results_json['suggested_values_for_paper']['tendon_compliance'] = f"{tendon_stats['max_deviation']:.4f} cm"
    
    with open(os.path.join(output_dir, 'analysis_results.json'), 'w') as f:
        json.dump(results_json, f, indent=2)
    
    return results_json

# =============================================================================
# Main Analysis Pipeline
# =============================================================================

def main():
    """Main analysis pipeline"""
    
    print("\n" + "="*80)
    print("FORWARD MODEL ANALYSIS - MESH RESOLUTION COMPARISON")
    print("="*80 + "\n")
    
    # Load data
    print("Loading data...")
    df_results, df_runtimes = load_all_data()
    
    print(f"✓ Loaded {len(df_results)} muscle length results")
    print(f"✓ Loaded {len(df_runtimes)} runtime results\n")
    
    # Load tendon data
    print("Loading tendon compliance data...")
    df_tendon = load_tendon_positions(AMI_PATH)
    if df_tendon is not None:
        print(f"✓ Loaded {len(df_tendon)} tendon position samples\n")
    else:
        print("  Warning: No tendon data found\n")
    
    # Compute ROM data
    print("Computing ROM values...")
    df_rom = compute_rom_values(df_results)
    print(f"✓ Computed ROM for {len(df_rom)} configurations\n")
    
    # Analyze ROM correlation
    print("Analyzing ROM correlation...")
    rom_analysis = compute_rom_correlation(df_results)
    print(f"✓ ROM Correlation: R² = {rom_analysis['r_squared']:.6f}\n")
    
    # Analyze runtime
    print("Analyzing runtime reduction...")
    runtime_stats = compute_runtime_reduction(df_runtimes)
    print(f"✓ Runtime Reduction: {runtime_stats['reduction_percent']:.2f}%\n")
    
    # Analyze tendon compliance
    tendon_stats = None
    if df_tendon is not None:
        print("Analyzing tendon compliance...")
        tendon_stats = analyze_tendon_compliance(df_tendon)
        print(f"✓ Max Tendon Deviation: {tendon_stats['max_deviation']:.4f} cm ({tendon_stats['max_deviation_percent']:.2f}%)\n")
    
    # Generate visualizations
    print("Generating visualizations...")
    plot_rom_correlation(rom_analysis, OUTPUT_DIR)
    print("  ✓ ROM correlation plot")
    
    plot_rom_comparison_bar(df_rom, OUTPUT_DIR)
    print("  ✓ ROM comparison bar chart")
    
    plot_runtime_comparison(df_runtimes, runtime_stats, OUTPUT_DIR)
    print("  ✓ Runtime comparison plots")
    
    plot_elongation_comparison(df_rom, OUTPUT_DIR)
    print("  ✓ Elongation/strain comparison")
    
    if df_tendon is not None and tendon_stats is not None:
        plot_tendon_compliance(df_tendon, tendon_stats, OUTPUT_DIR)
        print("  ✓ Tendon compliance plot")
    
    print()
    
    # Save data tables
    print("Saving data tables...")
    save_data_tables(df_results, df_runtimes, df_rom, OUTPUT_DIR)
    print("  ✓ CSV and LaTeX tables saved\n")
    
    # Save JSON results
    print("Saving JSON results...")
    json_results = save_json_results(rom_analysis, runtime_stats, tendon_stats, OUTPUT_DIR)
    print("  ✓ JSON results saved\n")
    
    # Generate summary report
    print("Generating summary report...")
    report = generate_summary_report(df_results, df_runtimes, rom_analysis, 
                                     runtime_stats, df_rom, tendon_stats, OUTPUT_DIR)
    print("\n✓ Summary report saved\n")
    
    print("="*80)
    print(f"Analysis complete! Results saved to: {OUTPUT_DIR}")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
