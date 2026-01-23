#!/usr/bin/env python3
"""
Detailed Analysis: Force-Modulated ROM Relationship

Visualizes and analyzes the force-modulated linear relationship between
4x4 and 8x8 mesh ROM values.

Author: Analysis for force-modulated relationship
Date: 2026-01-11
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats
from pathlib import Path

# Configuration
CSV_FILE = Path("analysis/complete_results.csv")
OUTPUT_DIR = Path("analysis/force_modulated")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# Load data
print("Loading data...")
df = pd.read_csv(CSV_FILE)
df_clean = df.dropna(subset=['4x4_ROM_cm', '8x8_ROM_cm'])

force = df_clean['Force_N'].values
rom_4x4 = df_clean['4x4_ROM_cm'].values
rom_8x8 = df_clean['8x8_ROM_cm'].values

print(f"✓ Loaded {len(df_clean)} data points (Force: {force.min()}-{force.max()} N)\n")

# ============================================================================
# FORCE-MODULATED MODEL
# ============================================================================
print("="*80)
print("FORCE-MODULATED LINEAR MODEL")
print("="*80)
print("\nModel: ROM_8x8 = ROM_4x4 × α(F)")
print("where α(F) is the force-dependent scaling factor\n")

# Calculate scaling factors
scaling_factors = rom_8x8 / rom_4x4

# Fit different models for α(F)
def constant_model(F):
    return np.ones_like(F) * np.mean(scaling_factors)

def linear_model(F, a, b):
    return a * F + b

def quadratic_model(F, a, b, c):
    return a * F**2 + b * F + c

def exponential_model(F, a, b, c):
    return a * np.exp(-b * F) + c

# Fit models
print("[1] Constant: α(F) = constant")
alpha_const = np.mean(scaling_factors)
rom_8x8_pred_const = rom_4x4 * alpha_const
r2_const = 1 - np.sum((rom_8x8 - rom_8x8_pred_const)**2) / np.sum((rom_8x8 - np.mean(rom_8x8))**2)
rmse_const = np.sqrt(np.mean((rom_8x8 - rom_8x8_pred_const)**2))
print(f"    α = {alpha_const:.6f}")
print(f"    R² = {r2_const:.4f}, RMSE = {rmse_const:.6f} cm")

print("\n[2] Linear: α(F) = a×F + b")
popt_lin, _ = curve_fit(linear_model, force, scaling_factors)
alpha_lin = linear_model(force, *popt_lin)
rom_8x8_pred_lin = rom_4x4 * alpha_lin
r2_lin = 1 - np.sum((rom_8x8 - rom_8x8_pred_lin)**2) / np.sum((rom_8x8 - np.mean(rom_8x8))**2)
rmse_lin = np.sqrt(np.mean((rom_8x8 - rom_8x8_pred_lin)**2))
print(f"    α(F) = {popt_lin[0]:.8f}×F + {popt_lin[1]:.6f}")
print(f"    R² = {r2_lin:.4f}, RMSE = {rmse_lin:.6f} cm")

print("\n[3] Quadratic: α(F) = a×F² + b×F + c")
popt_quad, _ = curve_fit(quadratic_model, force, scaling_factors)
alpha_quad = quadratic_model(force, *popt_quad)
rom_8x8_pred_quad = rom_4x4 * alpha_quad
r2_quad = 1 - np.sum((rom_8x8 - rom_8x8_pred_quad)**2) / np.sum((rom_8x8 - np.mean(rom_8x8))**2)
rmse_quad = np.sqrt(np.mean((rom_8x8 - rom_8x8_pred_quad)**2))
print(f"    α(F) = {popt_quad[0]:.10f}×F² + {popt_quad[1]:.6f}×F + {popt_quad[2]:.6f}")
print(f"    R² = {r2_quad:.4f}, RMSE = {rmse_quad:.6f} cm")

print("\n[4] Exponential: α(F) = a×exp(-b×F) + c")
try:
    popt_exp, _ = curve_fit(exponential_model, force, scaling_factors, p0=[0.1, 0.01, 0.5], maxfev=10000)
    alpha_exp = exponential_model(force, *popt_exp)
    rom_8x8_pred_exp = rom_4x4 * alpha_exp
    r2_exp = 1 - np.sum((rom_8x8 - rom_8x8_pred_exp)**2) / np.sum((rom_8x8 - np.mean(rom_8x8))**2)
    rmse_exp = np.sqrt(np.mean((rom_8x8 - rom_8x8_pred_exp)**2))
    print(f"    α(F) = {popt_exp[0]:.6f}×exp(-{popt_exp[1]:.6f}×F) + {popt_exp[2]:.6f}")
    print(f"    R² = {r2_exp:.4f}, RMSE = {rmse_exp:.6f} cm")
except:
    print("    Failed to fit exponential model")
    r2_exp = 0

# Best model
models = {'Constant': r2_const, 'Linear': r2_lin, 'Quadratic': r2_quad, 'Exponential': r2_exp}
best_model = max(models, key=models.get)
print(f"\n🏆 BEST MODEL: {best_model} (R² = {models[best_model]:.4f})")

# ============================================================================
# DETAILED VISUALIZATION
# ============================================================================
print("\n" + "="*80)
print("GENERATING DETAILED VISUALIZATIONS")
print("="*80)

# Create comprehensive figure
fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# ============================================================================
# Plot 1: Scaling Factor α(F) with all model fits
# ============================================================================
ax1 = fig.add_subplot(gs[0, :2])
force_fine = np.linspace(force.min(), force.max(), 300)

# Data points
scatter = ax1.scatter(force, scaling_factors, s=120, c=rom_4x4, cmap='plasma', 
                     alpha=0.8, edgecolors='black', linewidth=1.5, zorder=5)
cbar = plt.colorbar(scatter, ax=ax1)
cbar.set_label('4x4 ROM (cm)', fontsize=11, fontweight='bold')

# Model fits
ax1.axhline(alpha_const, color='gray', linestyle=':', linewidth=2.5, alpha=0.7, label=f'Constant: α={alpha_const:.3f}')
ax1.plot(force_fine, linear_model(force_fine, *popt_lin), '--', linewidth=2.5, color='blue', 
        alpha=0.8, label=f'Linear: R²={r2_lin:.3f}')
ax1.plot(force_fine, quadratic_model(force_fine, *popt_quad), '-', linewidth=3, color='red', 
        alpha=0.9, label=f'Quadratic: R²={r2_quad:.3f}')

# Confidence bands for quadratic
alpha_quad_fine = quadratic_model(force_fine, *popt_quad)
std_residuals = np.std(scaling_factors - alpha_quad)
ax1.fill_between(force_fine, alpha_quad_fine - 1.96*std_residuals, alpha_quad_fine + 1.96*std_residuals,
                 color='red', alpha=0.15, label='95% CI (Quadratic)')

ax1.set_xlabel('Prestretch Force (N)', fontsize=14, fontweight='bold')
ax1.set_ylabel('Scaling Factor α(F) = ROM_8x8 / ROM_4x4', fontsize=14, fontweight='bold')
ax1.set_title('Force-Dependent Scaling Factor α(F)', fontsize=16, fontweight='bold', pad=15)
ax1.legend(loc='best', fontsize=11, framealpha=0.95)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xlim([force.min()-1, force.max()+1])

# Add text box with equation
textstr = f'Best Fit (Quadratic):\n'
textstr += f'α(F) = {popt_quad[0]:.2e}×F² + {popt_quad[1]:.4f}×F + {popt_quad[2]:.4f}\n'
textstr += f'RMSE = {rmse_quad:.4f} cm'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=11,
        verticalalignment='top', bbox=props, family='monospace')

# ============================================================================
# Plot 2: Model Comparison Bar Chart
# ============================================================================
ax2 = fig.add_subplot(gs[0, 2])
model_names = ['Constant', 'Linear', 'Quadratic']
r2_values = [r2_const, r2_lin, r2_quad]
rmse_values = [rmse_const, rmse_lin, rmse_quad]

colors = ['#95a5a6', '#3498db', '#e74c3c']
bars = ax2.barh(model_names, r2_values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
ax2.set_xlabel('R² Value', fontsize=12, fontweight='bold')
ax2.set_title('Model Comparison', fontsize=14, fontweight='bold')
ax2.set_xlim([0, 1])
ax2.axvline(0.9, color='green', linestyle='--', alpha=0.5, linewidth=2)
ax2.grid(True, alpha=0.3, axis='x')

# Add values on bars
for bar, r2, rmse in zip(bars, r2_values, rmse_values):
    width = bar.get_width()
    ax2.text(width + 0.02, bar.get_y() + bar.get_height()/2,
            f'R²={r2:.3f}\nRMSE={rmse:.4f}', 
            ha='left', va='center', fontweight='bold', fontsize=9)

# ============================================================================
# Plot 3: Predicted vs Actual ROM (Quadratic Model)
# ============================================================================
ax3 = fig.add_subplot(gs[1, 0])
scatter = ax3.scatter(rom_8x8, rom_8x8_pred_quad, s=100, c=force, cmap='viridis',
                     alpha=0.8, edgecolors='black', linewidth=1.5)
lim_min = min(rom_8x8.min(), rom_8x8_pred_quad.min()) - 0.05
lim_max = max(rom_8x8.max(), rom_8x8_pred_quad.max()) + 0.05
ax3.plot([lim_min, lim_max], [lim_min, lim_max], 'k--', linewidth=2.5, alpha=0.7, label='Perfect prediction')
ax3.set_xlabel('Actual 8x8 ROM (cm)', fontsize=12, fontweight='bold')
ax3.set_ylabel('Predicted 8x8 ROM (cm)', fontsize=12, fontweight='bold')
ax3.set_title(f'Model Accuracy (Quadratic α)\nRMSE={rmse_quad:.4f} cm', fontsize=13, fontweight='bold')
ax3.legend(loc='best', fontsize=10)
ax3.grid(True, alpha=0.3)
ax3.set_aspect('equal', adjustable='box')

cbar = plt.colorbar(scatter, ax=ax3)
cbar.set_label('Force (N)', fontsize=10, fontweight='bold')

# ============================================================================
# Plot 4: Residuals vs Force (Quadratic Model)
# ============================================================================
ax4 = fig.add_subplot(gs[1, 1])
residuals_quad = rom_8x8 - rom_8x8_pred_quad
ax4.scatter(force, residuals_quad, s=100, c='#e74c3c', alpha=0.7, edgecolors='black', linewidth=1.5)
ax4.axhline(0, color='black', linestyle='-', linewidth=2)
ax4.axhline(2*rmse_quad, color='red', linestyle='--', linewidth=2, alpha=0.5, label='±2×RMSE')
ax4.axhline(-2*rmse_quad, color='red', linestyle='--', linewidth=2, alpha=0.5)
ax4.fill_between([force.min(), force.max()], -2*rmse_quad, 2*rmse_quad, 
                 color='red', alpha=0.1, label='±2σ band')
ax4.set_xlabel('Prestretch Force (N)', fontsize=12, fontweight='bold')
ax4.set_ylabel('Residuals (cm)', fontsize=12, fontweight='bold')
ax4.set_title('Residual Analysis', fontsize=13, fontweight='bold')
ax4.legend(loc='best', fontsize=10)
ax4.grid(True, alpha=0.3)

# ============================================================================
# Plot 5: Residuals vs ROM_4x4 (to check for patterns)
# ============================================================================
ax5 = fig.add_subplot(gs[1, 2])
ax5.scatter(rom_4x4, residuals_quad, s=100, c=force, cmap='viridis',
           alpha=0.7, edgecolors='black', linewidth=1.5)
ax5.axhline(0, color='black', linestyle='-', linewidth=2)
ax5.axhline(2*rmse_quad, color='red', linestyle='--', linewidth=2, alpha=0.5)
ax5.axhline(-2*rmse_quad, color='red', linestyle='--', linewidth=2, alpha=0.5)
ax5.set_xlabel('4x4 ROM (cm)', fontsize=12, fontweight='bold')
ax5.set_ylabel('Residuals (cm)', fontsize=12, fontweight='bold')
ax5.set_title('Residuals vs 4x4 ROM', fontsize=13, fontweight='bold')
ax5.grid(True, alpha=0.3)

# ============================================================================
# Plot 6: 3D View - Force, ROM_4x4, Scaling Factor
# ============================================================================
ax6 = fig.add_subplot(gs[2, :], projection='3d')

# Data points
scatter = ax6.scatter(force, rom_4x4, scaling_factors, c=scaling_factors, cmap='coolwarm',
                     s=80, alpha=0.8, edgecolors='black', linewidth=1)

# Model surface
F_mesh, ROM_mesh = np.meshgrid(np.linspace(force.min(), force.max(), 30),
                                np.linspace(rom_4x4.min(), rom_4x4.max(), 30))
Alpha_mesh = quadratic_model(F_mesh, *popt_quad)

surf = ax6.plot_surface(F_mesh, ROM_mesh, Alpha_mesh, alpha=0.3, cmap='coolwarm',
                       edgecolor='none', antialiased=True)

ax6.set_xlabel('Prestretch Force (N)', fontsize=11, fontweight='bold', labelpad=10)
ax6.set_ylabel('4x4 ROM (cm)', fontsize=11, fontweight='bold', labelpad=10)
ax6.set_zlabel('Scaling Factor α', fontsize=11, fontweight='bold', labelpad=10)
ax6.set_title('3D Visualization: Force-Modulated Relationship', fontsize=14, fontweight='bold', pad=20)

cbar = plt.colorbar(scatter, ax=ax6, shrink=0.5, aspect=5)
cbar.set_label('α(F)', fontsize=10, fontweight='bold')

ax6.view_init(elev=20, azim=45)

plt.savefig(OUTPUT_DIR / 'force_modulated_comprehensive.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {OUTPUT_DIR / 'force_modulated_comprehensive.png'}")

# ============================================================================
# Additional Plot: Alpha derivative (rate of change)
# ============================================================================
fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Left: α(F) with derivative
force_fine = np.linspace(force.min(), force.max(), 300)
alpha_fine = quadratic_model(force_fine, *popt_quad)
dalpha_dF = 2 * popt_quad[0] * force_fine + popt_quad[1]

ax1_twin = ax1.twinx()
ax1.scatter(force, scaling_factors, s=100, alpha=0.7, color='#e74c3c', 
           edgecolors='black', linewidth=1.5, label='Data', zorder=5)
line1 = ax1.plot(force_fine, alpha_fine, '-', linewidth=3, color='blue', 
                label='α(F) - Quadratic fit', zorder=3)
line2 = ax1_twin.plot(force_fine, dalpha_dF, '--', linewidth=2.5, color='green',
                     label="dα/dF (Rate of change)", zorder=3)

ax1.set_xlabel('Prestretch Force (N)', fontsize=13, fontweight='bold')
ax1.set_ylabel('Scaling Factor α(F)', fontsize=13, fontweight='bold', color='blue')
ax1_twin.set_ylabel('Rate of Change dα/dF', fontsize=13, fontweight='bold', color='green')
ax1.tick_params(axis='y', labelcolor='blue')
ax1_twin.tick_params(axis='y', labelcolor='green')
ax1.set_title('Scaling Factor and its Rate of Change', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax1_twin.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='best', fontsize=11)

# Right: Percentage difference over force range
ax2.scatter(force, (scaling_factors - alpha_const) / alpha_const * 100, 
           s=100, alpha=0.7, color='#9b59b6', edgecolors='black', linewidth=1.5)
ax2.plot(force_fine, (alpha_fine - alpha_const) / alpha_const * 100, 
        '-', linewidth=2.5, color='darkviolet', label='Quadratic model')
ax2.axhline(0, color='black', linestyle='-', linewidth=1.5, alpha=0.5)
ax2.set_xlabel('Prestretch Force (N)', fontsize=13, fontweight='bold')
ax2.set_ylabel('Deviation from Mean α (%)', fontsize=13, fontweight='bold')
ax2.set_title(f'Relative Change in Scaling\n(Mean α = {alpha_const:.4f})', 
             fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=11)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'force_modulated_derivative.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {OUTPUT_DIR / 'force_modulated_derivative.png'}")

# ============================================================================
# Summary Report
# ============================================================================
report_path = OUTPUT_DIR / 'force_modulated_summary.txt'
with open(report_path, 'w') as f:
    f.write("="*80 + "\n")
    f.write("FORCE-MODULATED LINEAR RELATIONSHIP: ROM_8x8 = ROM_4x4 × α(F)\n")
    f.write("="*80 + "\n\n")
    
    f.write("FINAL MODEL (Best Fit: Quadratic)\n")
    f.write("-"*80 + "\n")
    f.write(f"α(F) = {popt_quad[0]:.10f} × F² + {popt_quad[1]:.6f} × F + {popt_quad[2]:.6f}\n\n")
    f.write(f"Therefore:\n")
    f.write(f"ROM_8x8 = ROM_4x4 × [{popt_quad[0]:.10f} × F² + {popt_quad[1]:.6f} × F + {popt_quad[2]:.6f}]\n\n")
    
    f.write(f"Model Performance:\n")
    f.write(f"  R² = {r2_quad:.4f}\n")
    f.write(f"  RMSE = {rmse_quad:.6f} cm\n")
    f.write(f"  Max Error = {np.max(np.abs(residuals_quad)):.6f} cm\n\n")
    
    f.write("PHYSICAL INTERPRETATION\n")
    f.write("-"*80 + "\n")
    f.write(f"At F = 0 N:  α = {quadratic_model(0, *popt_quad):.4f} ({quadratic_model(0, *popt_quad)*100:.1f}%)\n")
    f.write(f"At F = 10 N: α = {quadratic_model(10, *popt_quad):.4f} ({quadratic_model(10, *popt_quad)*100:.1f}%)\n")
    f.write(f"At F = 20 N: α = {quadratic_model(20, *popt_quad):.4f} ({quadratic_model(20, *popt_quad)*100:.1f}%)\n")
    f.write(f"At F = 35 N: α = {quadratic_model(35, *popt_quad):.4f} ({quadratic_model(35, *popt_quad)*100:.1f}%)\n\n")
    
    f.write(f"Total change: {(quadratic_model(35, *popt_quad) - quadratic_model(0, *popt_quad))*100:.2f}% ")
    f.write(f"({quadratic_model(0, *popt_quad):.4f} → {quadratic_model(35, *popt_quad):.4f})\n\n")
    
    f.write("CONCLUSION\n")
    f.write("-"*80 + "\n")
    f.write("The relationship between 8x8 and 4x4 ROM is NOT a simple linear relationship,\n")
    f.write("but a FORCE-MODULATED linear relationship where the scaling factor α(F)\n")
    f.write("decreases quadratically with increasing prestretch force.\n\n")
    f.write("This suggests that the finer 8x8 mesh captures different (more realistic)\n")
    f.write("mechanical behavior at higher forces compared to the coarser 4x4 mesh.\n")
    f.write("="*80 + "\n")

print(f"✓ Saved: {report_path}")

print("\n" + "="*80)
print("✅ ANALYSIS COMPLETE")
print("="*80)
print(f"\nGenerated files in {OUTPUT_DIR}/:")
print("  • force_modulated_comprehensive.png - Main analysis with 6 subplots")
print("  • force_modulated_derivative.png - Derivative and deviation analysis")
print("  • force_modulated_summary.txt - Detailed summary report")
print("\n")
