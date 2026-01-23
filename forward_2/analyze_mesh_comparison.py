#!/usr/bin/env python3
"""
Mesh Resolution Comparison Analysis (4x4 vs 8x8)

Analyzes the relationship between 4x4 and 8x8 mesh resolutions
for muscle simulation results with varying prestretch forces.

Author: Generated for forward model analysis
Date: 2026-01-11
"""

import os
import re
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats
from scipy.optimize import curve_fit

# Configuration
RESULTS_DIR = Path("archived_results")
OUTPUT_DIR = Path("analysis")
OUTPUT_DIR.mkdir(exist_ok=True)

# Plot styling
plt.style.use('seaborn-v0_8-darkgrid')
COLORS = {'4x4': '#2E86AB', '8x8': '#A23B72'}


def parse_results_directory(mesh_size="4x4"):
    """
    Parse all simulation results for a given mesh size.
    
    Returns:
        dict: {force: {'rom': float, 'z_max': float, 'z_min': float, 
                       'initial_length': float, 'final_length': float}}
    """
    results = {}
    
    pattern = re.compile(rf"{mesh_size}_F(\d+)N")
    
    for dir_name in sorted(RESULTS_DIR.glob(f"{mesh_size}_F*N")):
        match = pattern.match(dir_name.name)
        if not match:
            continue
            
        force = int(match.group(1))
        
        # Read range_of_motion.txt
        rom_file = dir_name / "range_of_motion.txt"
        summary_file = dir_name / "summary.txt"
        
        if not rom_file.exists() or not summary_file.exists():
            print(f"Warning: Missing files in {dir_name.name}")
            continue
        
        # Parse ROM data
        rom_data = {}
        with open(rom_file, 'r') as f:
            for line in f:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    try:
                        rom_data[key] = float(value)
                    except ValueError:
                        pass
        
        # Parse summary data
        with open(summary_file, 'r') as f:
            content = f.read()
            
            # Extract initial and final lengths
            initial_match = re.search(r'Initial Length:\s*([\d.]+)', content)
            final_match = re.search(r'Final Length.*?:\s*([\d.]+)', content)
            
            initial_length = float(initial_match.group(1)) if initial_match else None
            final_length = float(final_match.group(1)) if final_match else None
        
        results[force] = {
            'rom': rom_data.get('ROM', np.nan),
            'z_max': rom_data.get('z_max', np.nan),
            'z_min': rom_data.get('z_min', np.nan),
            'initial_length': initial_length,
            'final_length': final_length,
            'prestretch_elongation': final_length - initial_length if (initial_length and final_length) else 0
        }
    
    return results


def linear_model(x, a, b):
    """Linear model: y = ax + b"""
    return a * x + b


def quadratic_model(x, a, b, c):
    """Quadratic model: y = ax² + bx + c"""
    return a * x**2 + b * x + c


def exponential_model(x, a, b, c):
    """Exponential saturation model: y = a(1 - exp(-bx)) + c"""
    return a * (1 - np.exp(-b * x)) + c


def analyze_relationship(forces_4x4, rom_4x4, forces_8x8, rom_8x8):
    """
    Analyze the relationship between 4x4 and 8x8 ROM values.
    
    Returns:
        dict: Analysis results including correlations and model fits
    """
    analysis = {}
    
    # Find common forces
    common_forces = sorted(set(forces_4x4) & set(forces_8x8))
    
    if len(common_forces) < 3:
        print("Warning: Not enough common data points for analysis")
        return analysis
    
    # Extract matched data
    rom_4x4_matched = [rom_4x4[forces_4x4.index(f)] for f in common_forces]
    rom_8x8_matched = [rom_8x8[forces_8x8.index(f)] for f in common_forces]
    
    analysis['common_forces'] = common_forces
    analysis['rom_4x4_matched'] = rom_4x4_matched
    analysis['rom_8x8_matched'] = rom_8x8_matched
    
    # Correlation analysis
    pearson_corr, pearson_p = stats.pearsonr(rom_4x4_matched, rom_8x8_matched)
    spearman_corr, spearman_p = stats.spearmanr(rom_4x4_matched, rom_8x8_matched)
    
    analysis['pearson_corr'] = pearson_corr
    analysis['pearson_p'] = pearson_p
    analysis['spearman_corr'] = spearman_corr
    analysis['spearman_p'] = spearman_p
    
    # Linear regression (4x4 vs 8x8)
    slope, intercept, r_value, p_value, std_err = stats.linregress(rom_4x4_matched, rom_8x8_matched)
    
    analysis['linear_slope'] = slope
    analysis['linear_intercept'] = intercept
    analysis['linear_r2'] = r_value**2
    analysis['linear_p'] = p_value
    
    # Residuals analysis
    rom_8x8_predicted = slope * np.array(rom_4x4_matched) + intercept
    residuals = np.array(rom_8x8_matched) - rom_8x8_predicted
    
    analysis['residuals'] = residuals
    analysis['residuals_mean'] = np.mean(residuals)
    analysis['residuals_std'] = np.std(residuals)
    analysis['max_abs_residual'] = np.max(np.abs(residuals))
    
    return analysis


def analyze_force_rom_relationship(forces, rom, mesh_size):
    """
    Analyze Force-ROM relationship for a specific mesh.
    
    Returns:
        dict: Model fits and goodness-of-fit metrics
    """
    analysis = {'mesh_size': mesh_size}
    
    forces_arr = np.array(forces)
    rom_arr = np.array(rom)
    
    # Linear fit
    try:
        popt_lin, _ = curve_fit(linear_model, forces_arr, rom_arr)
        rom_pred_lin = linear_model(forces_arr, *popt_lin)
        r2_lin = 1 - np.sum((rom_arr - rom_pred_lin)**2) / np.sum((rom_arr - np.mean(rom_arr))**2)
        
        analysis['linear_params'] = popt_lin
        analysis['linear_r2'] = r2_lin
    except:
        analysis['linear_params'] = None
        analysis['linear_r2'] = None
    
    # Quadratic fit
    try:
        popt_quad, _ = curve_fit(quadratic_model, forces_arr, rom_arr)
        rom_pred_quad = quadratic_model(forces_arr, *popt_quad)
        r2_quad = 1 - np.sum((rom_arr - rom_pred_quad)**2) / np.sum((rom_arr - np.mean(rom_arr))**2)
        
        analysis['quadratic_params'] = popt_quad
        analysis['quadratic_r2'] = r2_quad
    except:
        analysis['quadratic_params'] = None
        analysis['quadratic_r2'] = None
    
    # Exponential saturation fit
    try:
        # Initial guess
        p0 = [np.max(rom_arr), 0.1, np.min(rom_arr)]
        popt_exp, _ = curve_fit(exponential_model, forces_arr, rom_arr, p0=p0, maxfev=10000)
        rom_pred_exp = exponential_model(forces_arr, *popt_exp)
        r2_exp = 1 - np.sum((rom_arr - rom_pred_exp)**2) / np.sum((rom_arr - np.mean(rom_arr))**2)
        
        analysis['exponential_params'] = popt_exp
        analysis['exponential_r2'] = r2_exp
    except:
        analysis['exponential_params'] = None
        analysis['exponential_r2'] = None
    
    return analysis


def plot_force_rom_comparison(results_4x4, results_8x8, force_analysis_4x4, force_analysis_8x8):
    """Plot Force vs ROM for both mesh sizes with model fits."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Extract data
    forces_4x4 = sorted(results_4x4.keys())
    rom_4x4 = [results_4x4[f]['rom'] for f in forces_4x4]
    
    forces_8x8 = sorted(results_8x8.keys())
    rom_8x8 = [results_8x8[f]['rom'] for f in forces_8x8]
    
    # Left plot: Raw data comparison
    ax1.scatter(forces_4x4, rom_4x4, label='4x4 mesh', color=COLORS['4x4'], s=80, alpha=0.7, edgecolors='black')
    ax1.scatter(forces_8x8, rom_8x8, label='8x8 mesh', color=COLORS['8x8'], s=80, alpha=0.7, edgecolors='black')
    
    # Add model fits
    forces_fine = np.linspace(0, max(max(forces_4x4), max(forces_8x8)), 200)
    
    # 4x4 fits
    if force_analysis_4x4.get('linear_params') is not None:
        rom_fit_4x4 = linear_model(forces_fine, *force_analysis_4x4['linear_params'])
        ax1.plot(forces_fine, rom_fit_4x4, '--', color=COLORS['4x4'], alpha=0.5, 
                label=f"4x4 linear (R²={force_analysis_4x4['linear_r2']:.3f})")
    
    if force_analysis_4x4.get('quadratic_params') is not None:
        rom_fit_4x4 = quadratic_model(forces_fine, *force_analysis_4x4['quadratic_params'])
        ax1.plot(forces_fine, rom_fit_4x4, '-', color=COLORS['4x4'], alpha=0.8, linewidth=2,
                label=f"4x4 quadratic (R²={force_analysis_4x4['quadratic_r2']:.3f})")
    
    # 8x8 fits
    if force_analysis_8x8.get('linear_params') is not None:
        rom_fit_8x8 = linear_model(forces_fine, *force_analysis_8x8['linear_params'])
        ax1.plot(forces_fine, rom_fit_8x8, '--', color=COLORS['8x8'], alpha=0.5,
                label=f"8x8 linear (R²={force_analysis_8x8['linear_r2']:.3f})")
    
    if force_analysis_8x8.get('quadratic_params') is not None:
        rom_fit_8x8 = quadratic_model(forces_fine, *force_analysis_8x8['quadratic_params'])
        ax1.plot(forces_fine, rom_fit_8x8, '-', color=COLORS['8x8'], alpha=0.8, linewidth=2,
                label=f"8x8 quadratic (R²={force_analysis_8x8['quadratic_r2']:.3f})")
    
    ax1.set_xlabel('Prestretch Force (N)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Range of Motion (cm)', fontsize=12, fontweight='bold')
    ax1.set_title('Force-ROM Relationship\n(Linear vs Quadratic Models)', fontsize=14, fontweight='bold')
    ax1.legend(loc='best', fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # Right plot: Difference between meshes
    common_forces = sorted(set(forces_4x4) & set(forces_8x8))
    rom_4x4_matched = [results_4x4[f]['rom'] for f in common_forces]
    rom_8x8_matched = [results_8x8[f]['rom'] for f in common_forces]
    rom_diff = np.array(rom_8x8_matched) - np.array(rom_4x4_matched)
    rom_diff_percent = 100 * rom_diff / np.array(rom_4x4_matched)
    
    ax2.scatter(common_forces, rom_diff_percent, color='#F18F01', s=80, alpha=0.7, edgecolors='black')
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    
    # Trend line
    z = np.polyfit(common_forces, rom_diff_percent, 2)
    p = np.poly1d(z)
    ax2.plot(forces_fine, p(forces_fine), '--', color='#F18F01', alpha=0.8, linewidth=2, label='Quadratic trend')
    
    ax2.set_xlabel('Prestretch Force (N)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('ROM Difference: (8x8 - 4x4) / 4x4 (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Mesh Resolution Effect on ROM\n(Relative Difference)', fontsize=14, fontweight='bold')
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'force_rom_comparison.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'force_rom_comparison.pdf', bbox_inches='tight')
    print(f"✓ Saved: {OUTPUT_DIR / 'force_rom_comparison.png'}")
    
    return fig


def plot_4x4_vs_8x8_direct(analysis):
    """Direct comparison plot: 4x4 ROM vs 8x8 ROM."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    rom_4x4 = analysis['rom_4x4_matched']
    rom_8x8 = analysis['rom_8x8_matched']
    forces = analysis['common_forces']
    
    # Left: Direct comparison with linear fit
    ax1.scatter(rom_4x4, rom_8x8, s=100, alpha=0.7, c=forces, cmap='viridis', edgecolors='black')
    
    # Perfect agreement line
    min_rom = min(min(rom_4x4), min(rom_8x8))
    max_rom = max(max(rom_4x4), max(rom_8x8))
    ax1.plot([min_rom, max_rom], [min_rom, max_rom], 'k--', alpha=0.5, linewidth=2, label='Perfect agreement')
    
    # Linear fit
    rom_fit = analysis['linear_slope'] * np.array(rom_4x4) + analysis['linear_intercept']
    sorted_indices = np.argsort(rom_4x4)
    ax1.plot(np.array(rom_4x4)[sorted_indices], rom_fit[sorted_indices], 'r-', linewidth=2, alpha=0.8,
            label=f"Linear fit (R²={analysis['linear_r2']:.3f})\ny = {analysis['linear_slope']:.3f}x + {analysis['linear_intercept']:.3f}")
    
    ax1.set_xlabel('4x4 ROM (cm)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('8x8 ROM (cm)', fontsize=12, fontweight='bold')
    ax1.set_title(f"Direct Mesh Comparison\nPearson r={analysis['pearson_corr']:.3f} (p={analysis['pearson_p']:.2e})", 
                 fontsize=14, fontweight='bold')
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    
    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=min(forces), vmax=max(forces)))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax1)
    cbar.set_label('Force (N)', fontsize=10, fontweight='bold')
    
    # Right: Residuals plot
    residuals = analysis['residuals']
    ax2.scatter(forces, residuals, s=100, alpha=0.7, color='#E63946', edgecolors='black')
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    ax2.axhline(y=analysis['residuals_mean'] + 2*analysis['residuals_std'], color='red', linestyle='--', alpha=0.5, label='±2σ')
    ax2.axhline(y=analysis['residuals_mean'] - 2*analysis['residuals_std'], color='red', linestyle='--', alpha=0.5)
    
    ax2.set_xlabel('Prestretch Force (N)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Residuals: 8x8 - Predicted (cm)', fontsize=12, fontweight='bold')
    ax2.set_title(f'Residuals Analysis\nMean={analysis["residuals_mean"]:.4f} cm, Std={analysis["residuals_std"]:.4f} cm', 
                 fontsize=14, fontweight='bold')
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'mesh_direct_comparison.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'mesh_direct_comparison.pdf', bbox_inches='tight')
    print(f"✓ Saved: {OUTPUT_DIR / 'mesh_direct_comparison.png'}")
    
    return fig


def plot_prestretch_analysis(results_4x4, results_8x8):
    """Analyze and plot prestretch elongation vs force."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    forces_4x4 = sorted(results_4x4.keys())
    prestretch_4x4 = [results_4x4[f]['prestretch_elongation'] for f in forces_4x4]
    
    forces_8x8 = sorted(results_8x8.keys())
    prestretch_8x8 = [results_8x8[f]['prestretch_elongation'] for f in forces_8x8]
    
    ax.scatter(forces_4x4, prestretch_4x4, label='4x4 mesh', color=COLORS['4x4'], s=80, alpha=0.7, edgecolors='black')
    ax.scatter(forces_8x8, prestretch_8x8, label='8x8 mesh', color=COLORS['8x8'], s=80, alpha=0.7, edgecolors='black')
    
    # Trend lines
    if len(forces_4x4) > 2:
        z4 = np.polyfit(forces_4x4, prestretch_4x4, 2)
        p4 = np.poly1d(z4)
        forces_fine = np.linspace(0, max(forces_4x4), 200)
        ax.plot(forces_fine, p4(forces_fine), '-', color=COLORS['4x4'], alpha=0.6, linewidth=2)
    
    if len(forces_8x8) > 2:
        z8 = np.polyfit(forces_8x8, prestretch_8x8, 2)
        p8 = np.poly1d(z8)
        forces_fine = np.linspace(0, max(forces_8x8), 200)
        ax.plot(forces_fine, p8(forces_fine), '-', color=COLORS['8x8'], alpha=0.6, linewidth=2)
    
    ax.set_xlabel('Prestretch Force (N)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Muscle Elongation during Prestretch (cm)', fontsize=12, fontweight='bold')
    ax.set_title('Prestretch Force-Elongation Relationship', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'prestretch_elongation.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {OUTPUT_DIR / 'prestretch_elongation.png'}")
    
    return fig


def export_complete_results_csv(results_4x4, results_8x8):
    """Export all data points to CSV for detailed inspection."""
    csv_path = OUTPUT_DIR / 'complete_results.csv'
    
    # Get all forces
    all_forces = sorted(set(results_4x4.keys()) | set(results_8x8.keys()))
    
    with open(csv_path, 'w') as f:
        # Header
        f.write("Force_N,4x4_ROM_cm,4x4_z_max_cm,4x4_z_min_cm,4x4_prestretch_elongation_cm,")
        f.write("8x8_ROM_cm,8x8_z_max_cm,8x8_z_min_cm,8x8_prestretch_elongation_cm,")
        f.write("ROM_Difference_cm,ROM_Difference_Percent\n")
        
        # Data rows
        for force in all_forces:
            data_4x4 = results_4x4.get(force, {})
            data_8x8 = results_8x8.get(force, {})
            
            rom_4x4 = data_4x4.get('rom', np.nan)
            rom_8x8 = data_8x8.get('rom', np.nan)
            
            rom_diff = rom_8x8 - rom_4x4 if (not np.isnan(rom_4x4) and not np.isnan(rom_8x8)) else np.nan
            rom_diff_pct = 100 * rom_diff / rom_4x4 if (not np.isnan(rom_4x4) and rom_4x4 != 0) else np.nan
            
            f.write(f"{force},")
            f.write(f"{data_4x4.get('rom', '')},{data_4x4.get('z_max', '')},{data_4x4.get('z_min', '')},{data_4x4.get('prestretch_elongation', '')},")
            f.write(f"{data_8x8.get('rom', '')},{data_8x8.get('z_max', '')},{data_8x8.get('z_min', '')},{data_8x8.get('prestretch_elongation', '')},")
            f.write(f"{rom_diff if not np.isnan(rom_diff) else ''},{rom_diff_pct if not np.isnan(rom_diff_pct) else ''}\n")
    
    print(f"✓ Saved: {csv_path}")
    return csv_path


def generate_report(results_4x4, results_8x8, mesh_comparison, force_analysis_4x4, force_analysis_8x8):
    """Generate comprehensive analysis report."""
    report_path = OUTPUT_DIR / 'analysis_report.txt'
    
    with open(report_path, 'w') as f:
        f.write("="*80 + "\n")
        f.write("MESH RESOLUTION COMPARISON ANALYSIS (4x4 vs 8x8)\n")
        f.write("="*80 + "\n\n")
        
        # Dataset summary
        f.write("1. DATASET SUMMARY\n")
        f.write("-" * 80 + "\n")
        f.write(f"4x4 Mesh: {len(results_4x4)} simulations (Force: {min(results_4x4.keys())}-{max(results_4x4.keys())} N in 1N steps)\n")
        f.write(f"8x8 Mesh: {len(results_8x8)} simulations (Force: {min(results_8x8.keys())}-{max(results_8x8.keys())} N in 1N steps)\n")
        f.write(f"Common data points: {len(mesh_comparison['common_forces'])}\n")
        f.write(f"All force values analyzed: {sorted(mesh_comparison['common_forces'])}\n\n")
        
        # ROM statistics
        rom_4x4_all = [r['rom'] for r in results_4x4.values()]
        rom_8x8_all = [r['rom'] for r in results_8x8.values()]
        
        f.write("ROM Statistics:\n")
        f.write(f"  4x4: Mean={np.mean(rom_4x4_all):.3f} cm, Std={np.std(rom_4x4_all):.3f} cm, Range=[{np.min(rom_4x4_all):.3f}, {np.max(rom_4x4_all):.3f}] cm\n")
        f.write(f"  8x8: Mean={np.mean(rom_8x8_all):.3f} cm, Std={np.std(rom_8x8_all):.3f} cm, Range=[{np.min(rom_8x8_all):.3f}, {np.max(rom_8x8_all):.3f}] cm\n\n")
        
        # Correlation analysis
        f.write("2. CORRELATION ANALYSIS (4x4 vs 8x8)\n")
        f.write("-" * 80 + "\n")
        f.write(f"Pearson Correlation: r={mesh_comparison['pearson_corr']:.4f} (p={mesh_comparison['pearson_p']:.2e})\n")
        f.write(f"Spearman Correlation: ρ={mesh_comparison['spearman_corr']:.4f} (p={mesh_comparison['spearman_p']:.2e})\n\n")
        
        # Linear relationship
        f.write("3. LINEAR RELATIONSHIP (8x8 = slope × 4x4 + intercept)\n")
        f.write("-" * 80 + "\n")
        f.write(f"Slope: {mesh_comparison['linear_slope']:.4f}\n")
        f.write(f"Intercept: {mesh_comparison['linear_intercept']:.4f} cm\n")
        f.write(f"R²: {mesh_comparison['linear_r2']:.4f}\n")
        f.write(f"p-value: {mesh_comparison['linear_p']:.2e}\n\n")
        
        f.write(f"Interpretation:\n")
        if abs(mesh_comparison['linear_slope'] - 1.0) < 0.1:
            f.write(f"  → Slope ≈ 1.0: 8x8 and 4x4 ROM are approximately equal\n")
        elif mesh_comparison['linear_slope'] > 1.0:
            f.write(f"  → Slope > 1.0: 8x8 ROM is {(mesh_comparison['linear_slope']-1)*100:.1f}% larger on average\n")
        else:
            f.write(f"  → Slope < 1.0: 8x8 ROM is {(1-mesh_comparison['linear_slope'])*100:.1f}% smaller on average\n")
        
        f.write(f"\nResiduals:\n")
        f.write(f"  Mean: {mesh_comparison['residuals_mean']:.4f} cm\n")
        f.write(f"  Std Dev: {mesh_comparison['residuals_std']:.4f} cm\n")
        f.write(f"  Max Abs: {mesh_comparison['max_abs_residual']:.4f} cm\n\n")
        
        # Force-ROM relationship
        f.write("4. FORCE-ROM RELATIONSHIP MODELS\n")
        f.write("-" * 80 + "\n")
        
        f.write("4x4 Mesh:\n")
        if force_analysis_4x4.get('linear_r2'):
            f.write(f"  Linear: R²={force_analysis_4x4['linear_r2']:.4f}, ROM = {force_analysis_4x4['linear_params'][0]:.4f}×F + {force_analysis_4x4['linear_params'][1]:.4f}\n")
        if force_analysis_4x4.get('quadratic_r2'):
            f.write(f"  Quadratic: R²={force_analysis_4x4['quadratic_r2']:.4f}\n")
            f.write(f"    ROM = {force_analysis_4x4['quadratic_params'][0]:.6f}×F² + {force_analysis_4x4['quadratic_params'][1]:.4f}×F + {force_analysis_4x4['quadratic_params'][2]:.4f}\n")
        
        f.write("\n8x8 Mesh:\n")
        if force_analysis_8x8.get('linear_r2'):
            f.write(f"  Linear: R²={force_analysis_8x8['linear_r2']:.4f}, ROM = {force_analysis_8x8['linear_params'][0]:.4f}×F + {force_analysis_8x8['linear_params'][1]:.4f}\n")
        if force_analysis_8x8.get('quadratic_r2'):
            f.write(f"  Quadratic: R²={force_analysis_8x8['quadratic_r2']:.4f}\n")
            f.write(f"    ROM = {force_analysis_8x8['quadratic_params'][0]:.6f}×F² + {force_analysis_8x8['quadratic_params'][1]:.4f}×F + {force_analysis_8x8['quadratic_params'][2]:.4f}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("5. CONCLUSIONS\n")
        f.write("-" * 80 + "\n")
        
        # Determine linearity
        if force_analysis_4x4.get('quadratic_r2') and force_analysis_4x4.get('linear_r2'):
            r2_improvement_4x4 = force_analysis_4x4['quadratic_r2'] - force_analysis_4x4['linear_r2']
            if r2_improvement_4x4 > 0.05:
                f.write(f"• 4x4 Mesh: NON-LINEAR relationship (quadratic improves R² by {r2_improvement_4x4:.3f})\n")
            else:
                f.write(f"• 4x4 Mesh: APPROXIMATELY LINEAR relationship (quadratic improvement: {r2_improvement_4x4:.3f})\n")
        
        if force_analysis_8x8.get('quadratic_r2') and force_analysis_8x8.get('linear_r2'):
            r2_improvement_8x8 = force_analysis_8x8['quadratic_r2'] - force_analysis_8x8['linear_r2']
            if r2_improvement_8x8 > 0.05:
                f.write(f"• 8x8 Mesh: NON-LINEAR relationship (quadratic improves R² by {r2_improvement_8x8:.3f})\n")
            else:
                f.write(f"• 8x8 Mesh: APPROXIMATELY LINEAR relationship (quadratic improvement: {r2_improvement_8x8:.3f})\n")
        
        f.write(f"\n• Mesh agreement: R²={mesh_comparison['linear_r2']:.3f} suggests ")
        if mesh_comparison['linear_r2'] > 0.95:
            f.write("EXCELLENT agreement between mesh sizes\n")
        elif mesh_comparison['linear_r2'] > 0.85:
            f.write("GOOD agreement between mesh sizes\n")
        else:
            f.write("MODERATE agreement - mesh size has notable impact\n")
        
        f.write("\n" + "="*80 + "\n")
    
    print(f"✓ Saved: {report_path}")
    return report_path


def main():
    """Main analysis workflow."""
    print("="*80)
    print("MESH RESOLUTION COMPARISON ANALYSIS")
    print("="*80)
    
    # Parse results
    print("\n[1/6] Parsing simulation results...")
    results_4x4 = parse_results_directory("4x4")
    results_8x8 = parse_results_directory("8x8")
    
    print(f"  ✓ Found {len(results_4x4)} simulations for 4x4 mesh")
    print(f"  ✓ Found {len(results_8x8)} simulations for 8x8 mesh")
    
    if len(results_4x4) == 0 or len(results_8x8) == 0:
        print("\n❌ ERROR: No data found. Check RESULTS_DIR path.")
        return
    
    # Extract ROM data
    forces_4x4 = sorted(results_4x4.keys())
    rom_4x4 = [results_4x4[f]['rom'] for f in forces_4x4]
    
    forces_8x8 = sorted(results_8x8.keys())
    rom_8x8 = [results_8x8[f]['rom'] for f in forces_8x8]
    
    # Mesh comparison analysis
    print("\n[2/6] Analyzing 4x4 vs 8x8 relationship...")
    mesh_comparison = analyze_relationship(forces_4x4, rom_4x4, forces_8x8, rom_8x8)
    
    if mesh_comparison:
        print(f"  ✓ Pearson correlation: r={mesh_comparison['pearson_corr']:.3f}")
        print(f"  ✓ Linear R²: {mesh_comparison['linear_r2']:.3f}")
    
    # Force-ROM relationship analysis
    print("\n[3/6] Analyzing Force-ROM relationships...")
    force_analysis_4x4 = analyze_force_rom_relationship(forces_4x4, rom_4x4, "4x4")
    force_analysis_8x8 = analyze_force_rom_relationship(forces_8x8, rom_8x8, "8x8")
    
    if force_analysis_4x4.get('linear_r2'):
        print(f"  ✓ 4x4 Linear R²: {force_analysis_4x4['linear_r2']:.3f}")
    if force_analysis_4x4.get('quadratic_r2'):
        print(f"  ✓ 4x4 Quadratic R²: {force_analysis_4x4['quadratic_r2']:.3f}")
    if force_analysis_8x8.get('linear_r2'):
        print(f"  ✓ 8x8 Linear R²: {force_analysis_8x8['linear_r2']:.3f}")
    if force_analysis_8x8.get('quadratic_r2'):
        print(f"  ✓ 8x8 Quadratic R²: {force_analysis_8x8['quadratic_r2']:.3f}")
    
    # Generate plots
    print("\n[4/6] Generating Force-ROM comparison plots...")
    plot_force_rom_comparison(results_4x4, results_8x8, force_analysis_4x4, force_analysis_8x8)
    
    print("\n[5/6] Generating mesh comparison plots...")
    if mesh_comparison:
        plot_4x4_vs_8x8_direct(mesh_comparison)
    
    print("\n[6/6] Generating prestretch analysis...")
    plot_prestretch_analysis(results_4x4, results_8x8)
    
    # Generate report
    print("\n[7/8] Generating analysis report...")
    report_path = generate_report(results_4x4, results_8x8, mesh_comparison, force_analysis_4x4, force_analysis_8x8)
    
    # Export complete CSV
    print("\n[8/8] Exporting complete results CSV...")
    csv_path = export_complete_results_csv(results_4x4, results_8x8)
    
    print("\n" + "="*80)
    print("✅ ANALYSIS COMPLETE")
    print("="*80)
    print(f"\nResults saved in: {OUTPUT_DIR}/")
    print(f"  • force_rom_comparison.png/pdf")
    print(f"  • mesh_direct_comparison.png/pdf")
    print(f"  • prestretch_elongation.png")
    print(f"  • analysis_report.txt")
    print(f"  • complete_results.csv (ALL {len(results_4x4)} force values)")
    print("\n")


if __name__ == "__main__":
    main()
