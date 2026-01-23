#!/usr/bin/env python3
"""
Deep Investigation: ROM Relationship between 4x4 and 8x8 Mesh

Systematically tests different hypotheses for the relationship between
4x4 ROM and 8x8 ROM values.

Author: Analysis for ROM relationship investigation
Date: 2026-01-11
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
from pathlib import Path

# Configuration
CSV_FILE = Path("analysis/complete_results.csv")
OUTPUT_DIR = Path("analysis/rom_relationship")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# Load data
print("Loading data...")
df = pd.read_csv(CSV_FILE)
print(f"✓ Loaded {len(df)} data points\n")

# Extract clean data
df_clean = df.dropna(subset=['4x4_ROM_cm', '8x8_ROM_cm'])
force = df_clean['Force_N'].values
rom_4x4 = df_clean['4x4_ROM_cm'].values
rom_8x8 = df_clean['8x8_ROM_cm'].values

print("="*80)
print("HYPOTHESIS TESTING: What is the relationship ROM_8x8 = f(ROM_4x4)?")
print("="*80)

# ============================================================================
# HYPOTHESIS 1: Linear Relationship
# ============================================================================
print("\n[HYPOTHESIS 1] Linear: ROM_8x8 = a × ROM_4x4 + b")
print("-" * 80)

slope, intercept, r_value, p_value, std_err = stats.linregress(rom_4x4, rom_8x8)
rom_8x8_pred_linear = slope * rom_4x4 + intercept
residuals_linear = rom_8x8 - rom_8x8_pred_linear
r2_linear = r_value**2

print(f"  Slope (a):      {slope:.6f}")
print(f"  Intercept (b):  {intercept:.6f} cm")
print(f"  R²:             {r2_linear:.4f}")
print(f"  RMSE:           {np.sqrt(np.mean(residuals_linear**2)):.6f} cm")
print(f"  Max Error:      {np.max(np.abs(residuals_linear)):.6f} cm")
print(f"  p-value:        {p_value:.2e}")

# ============================================================================
# HYPOTHESIS 2: Force-Dependent Scaling
# ============================================================================
print("\n[HYPOTHESIS 2] Force-dependent scaling: ROM_8x8 = ROM_4x4 × f(Force)")
print("-" * 80)

# Calculate scaling factor for each point
scaling_factors = rom_8x8 / rom_4x4

# Fit scaling factor as function of force
def linear_scaling(F, a, b):
    return a * F + b

def quadratic_scaling(F, a, b, c):
    return a * F**2 + b * F + c

# Linear fit
popt_lin, _ = curve_fit(linear_scaling, force, scaling_factors)
scaling_pred_lin = linear_scaling(force, *popt_lin)
r2_scaling_lin = 1 - np.sum((scaling_factors - scaling_pred_lin)**2) / np.sum((scaling_factors - np.mean(scaling_factors))**2)

print(f"  Linear scaling: scale = {popt_lin[0]:.6f} × Force + {popt_lin[1]:.6f}")
print(f"  R²:             {r2_scaling_lin:.4f}")

# Quadratic fit
popt_quad, _ = curve_fit(quadratic_scaling, force, scaling_factors)
scaling_pred_quad = quadratic_scaling(force, *popt_quad)
r2_scaling_quad = 1 - np.sum((scaling_factors - scaling_pred_quad)**2) / np.sum((scaling_factors - np.mean(scaling_factors))**2)

print(f"  Quadratic: scale = {popt_quad[0]:.8f} × F² + {popt_quad[1]:.6f} × F + {popt_quad[2]:.6f}")
print(f"  R²:             {r2_scaling_quad:.4f}")

# Test reconstruction with quadratic scaling
rom_8x8_pred_scaling_quad = rom_4x4 * quadratic_scaling(force, *popt_quad)
residuals_scaling_quad = rom_8x8 - rom_8x8_pred_scaling_quad
rmse_scaling_quad = np.sqrt(np.mean(residuals_scaling_quad**2))

print(f"  Reconstruction RMSE: {rmse_scaling_quad:.6f} cm")
print(f"  Max Error:           {np.max(np.abs(residuals_scaling_quad)):.6f} cm")

# ============================================================================
# HYPOTHESIS 3: Polynomial Relationship
# ============================================================================
print("\n[HYPOTHESIS 3] Polynomial: ROM_8x8 = Σ aᵢ × (ROM_4x4)ⁱ")
print("-" * 80)

for degree in [2, 3, 4]:
    coeffs = np.polyfit(rom_4x4, rom_8x8, degree)
    rom_8x8_pred_poly = np.polyval(coeffs, rom_4x4)
    residuals_poly = rom_8x8 - rom_8x8_pred_poly
    r2_poly = 1 - np.sum(residuals_poly**2) / np.sum((rom_8x8 - np.mean(rom_8x8))**2)
    rmse_poly = np.sqrt(np.mean(residuals_poly**2))
    
    print(f"  Degree {degree}: R² = {r2_poly:.4f}, RMSE = {rmse_poly:.6f} cm")

# ============================================================================
# HYPOTHESIS 4: Separate Linear Relationships per Force Range
# ============================================================================
print("\n[HYPOTHESIS 4] Piecewise Linear: Different slopes for different force ranges")
print("-" * 80)

force_ranges = [(0, 10), (10, 20), (20, 35)]
for f_min, f_max in force_ranges:
    mask = (force >= f_min) & (force <= f_max)
    if np.sum(mask) < 3:
        continue
    
    slope_seg, intercept_seg, r_seg, _, _ = stats.linregress(rom_4x4[mask], rom_8x8[mask])
    r2_seg = r_seg**2
    
    print(f"  Force {f_min:2d}-{f_max:2d}N: ROM_8x8 = {slope_seg:.6f} × ROM_4x4 + {intercept_seg:.6f}, R² = {r2_seg:.4f}")

# ============================================================================
# HYPOTHESIS 5: Ratio Analysis
# ============================================================================
print("\n[HYPOTHESIS 5] Constant Ratio: ROM_8x8 / ROM_4x4 = constant")
print("-" * 80)

ratio = rom_8x8 / rom_4x4
print(f"  Mean Ratio:  {np.mean(ratio):.6f}")
print(f"  Std Dev:     {np.std(ratio):.6f}")
print(f"  Range:       [{np.min(ratio):.6f}, {np.max(ratio):.6f}]")
print(f"  CV:          {np.std(ratio)/np.mean(ratio)*100:.2f}%")

# Test constant ratio hypothesis
rom_8x8_pred_ratio = rom_4x4 * np.mean(ratio)
residuals_ratio = rom_8x8 - rom_8x8_pred_ratio
rmse_ratio = np.sqrt(np.mean(residuals_ratio**2))
r2_ratio = 1 - np.sum(residuals_ratio**2) / np.sum((rom_8x8 - np.mean(rom_8x8))**2)

print(f"  R² (constant ratio): {r2_ratio:.4f}")
print(f"  RMSE:                {rmse_ratio:.6f} cm")

# ============================================================================
# VISUALIZATION
# ============================================================================
print("\n" + "="*80)
print("GENERATING VISUALIZATIONS")
print("="*80)

# Plot 1: All hypotheses comparison
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# 1. Linear fit
ax = axes[0, 0]
ax.scatter(rom_4x4, rom_8x8, c=force, cmap='viridis', s=80, alpha=0.7, edgecolors='black')
rom_4x4_sorted = np.sort(rom_4x4)
ax.plot(rom_4x4_sorted, slope * rom_4x4_sorted + intercept, 'r-', linewidth=2, 
        label=f'Linear: R²={r2_linear:.3f}')
ax.plot(rom_4x4_sorted, rom_4x4_sorted * np.mean(ratio), 'g--', linewidth=2,
        label=f'Constant ratio: {np.mean(ratio):.3f}')
ax.set_xlabel('4x4 ROM (cm)', fontweight='bold', fontsize=11)
ax.set_ylabel('8x8 ROM (cm)', fontweight='bold', fontsize=11)
ax.set_title('Linear Relationship', fontweight='bold', fontsize=12)
ax.legend()
ax.grid(True, alpha=0.3)

# 2. Scaling factor vs Force
ax = axes[0, 1]
ax.scatter(force, scaling_factors, s=80, alpha=0.7, color='#E63946', edgecolors='black')
force_fine = np.linspace(force.min(), force.max(), 200)
ax.plot(force_fine, quadratic_scaling(force_fine, *popt_quad), 'b-', linewidth=2,
        label=f'Quadratic fit: R²={r2_scaling_quad:.3f}')
ax.axhline(np.mean(ratio), color='green', linestyle='--', linewidth=2, alpha=0.7,
          label=f'Mean = {np.mean(ratio):.3f}')
ax.set_xlabel('Prestretch Force (N)', fontweight='bold', fontsize=11)
ax.set_ylabel('Scaling Factor (ROM_8x8 / ROM_4x4)', fontweight='bold', fontsize=11)
ax.set_title('Force-Dependent Scaling', fontweight='bold', fontsize=12)
ax.legend()
ax.grid(True, alpha=0.3)

# 3. Residuals: Linear model
ax = axes[0, 2]
ax.scatter(force, residuals_linear, s=80, alpha=0.7, color='#F18F01', edgecolors='black')
ax.axhline(0, color='black', linestyle='-', linewidth=1)
ax.axhline(2*np.std(residuals_linear), color='red', linestyle='--', alpha=0.5)
ax.axhline(-2*np.std(residuals_linear), color='red', linestyle='--', alpha=0.5)
ax.set_xlabel('Prestretch Force (N)', fontweight='bold', fontsize=11)
ax.set_ylabel('Residuals (cm)', fontweight='bold', fontsize=11)
ax.set_title(f'Linear Model Residuals\nRMSE = {np.sqrt(np.mean(residuals_linear**2)):.4f} cm', 
             fontweight='bold', fontsize=12)
ax.grid(True, alpha=0.3)

# 4. Residuals: Force-dependent scaling
ax = axes[1, 0]
ax.scatter(force, residuals_scaling_quad, s=80, alpha=0.7, color='#2A9D8F', edgecolors='black')
ax.axhline(0, color='black', linestyle='-', linewidth=1)
ax.axhline(2*np.std(residuals_scaling_quad), color='red', linestyle='--', alpha=0.5)
ax.axhline(-2*np.std(residuals_scaling_quad), color='red', linestyle='--', alpha=0.5)
ax.set_xlabel('Prestretch Force (N)', fontweight='bold', fontsize=11)
ax.set_ylabel('Residuals (cm)', fontweight='bold', fontsize=11)
ax.set_title(f'Force-Scaled Model Residuals\nRMSE = {rmse_scaling_quad:.4f} cm', 
             fontweight='bold', fontsize=12)
ax.grid(True, alpha=0.3)

# 5. Q-Q Plot for residuals
ax = axes[1, 1]
stats.probplot(residuals_linear, dist="norm", plot=ax)
ax.set_title('Q-Q Plot (Linear Model Residuals)', fontweight='bold', fontsize=12)
ax.grid(True, alpha=0.3)

# 6. Model Comparison
ax = axes[1, 2]
models = ['Linear', 'Constant\nRatio', 'Force-Scaled\n(Quadratic)', 'Poly-2', 'Poly-3']
r2_values = [r2_linear, r2_ratio, 1 - np.sum(residuals_scaling_quad**2) / np.sum((rom_8x8 - np.mean(rom_8x8))**2)]

# Add polynomial R² values
for degree in [2, 3]:
    coeffs = np.polyfit(rom_4x4, rom_8x8, degree)
    rom_8x8_pred = np.polyval(coeffs, rom_4x4)
    r2 = 1 - np.sum((rom_8x8 - rom_8x8_pred)**2) / np.sum((rom_8x8 - np.mean(rom_8x8))**2)
    r2_values.append(r2)

colors = ['#E63946', '#F18F01', '#2A9D8F', '#264653', '#2E86AB']
bars = ax.bar(models, r2_values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
ax.set_ylabel('R² Value', fontweight='bold', fontsize=11)
ax.set_title('Model Comparison', fontweight='bold', fontsize=12)
ax.set_ylim([0, 1])
ax.axhline(0.9, color='green', linestyle='--', alpha=0.5, label='R²=0.9')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

# Add values on bars
for bar, r2 in zip(bars, r2_values):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{r2:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'hypothesis_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {OUTPUT_DIR / 'hypothesis_comparison.png'}")

# ============================================================================
# Plot 2: Detailed Force-Scaling Relationship
# ============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Left: Scaling factor with both fits
ax1.scatter(force, scaling_factors, s=100, alpha=0.7, color='#E63946', edgecolors='black', linewidth=1.5)
force_fine = np.linspace(force.min(), force.max(), 200)
ax1.plot(force_fine, linear_scaling(force_fine, *popt_lin), '--', linewidth=2, color='blue', alpha=0.7,
        label=f'Linear: R²={r2_scaling_lin:.3f}')
ax1.plot(force_fine, quadratic_scaling(force_fine, *popt_quad), '-', linewidth=3, color='darkgreen',
        label=f'Quadratic: R²={r2_scaling_quad:.3f}')
ax1.axhline(np.mean(ratio), color='orange', linestyle=':', linewidth=2, alpha=0.8,
           label=f'Mean = {np.mean(ratio):.4f}')
ax1.fill_between(force_fine, np.mean(ratio) - np.std(ratio), np.mean(ratio) + np.std(ratio),
                 color='orange', alpha=0.2, label=f'±1σ = {np.std(ratio):.4f}')

ax1.set_xlabel('Prestretch Force (N)', fontweight='bold', fontsize=13)
ax1.set_ylabel('Scaling Factor: ROM_8x8 / ROM_4x4', fontweight='bold', fontsize=13)
ax1.set_title('Force-Dependent Scaling Analysis', fontweight='bold', fontsize=14)
ax1.legend(loc='best', fontsize=11)
ax1.grid(True, alpha=0.3)

# Right: Predicted vs Actual (using best model - force-scaled)
ax2.scatter(rom_8x8, rom_8x8_pred_scaling_quad, s=100, c=force, cmap='viridis', 
           alpha=0.7, edgecolors='black', linewidth=1.5)
lim_min = min(rom_8x8.min(), rom_8x8_pred_scaling_quad.min())
lim_max = max(rom_8x8.max(), rom_8x8_pred_scaling_quad.max())
ax2.plot([lim_min, lim_max], [lim_min, lim_max], 'k--', linewidth=2, alpha=0.7, label='Perfect prediction')
ax2.set_xlabel('Actual 8x8 ROM (cm)', fontweight='bold', fontsize=13)
ax2.set_ylabel('Predicted 8x8 ROM (cm)\n(Force-Scaled Model)', fontweight='bold', fontsize=13)
ax2.set_title(f'Model Performance\nRMSE = {rmse_scaling_quad:.4f} cm', fontweight='bold', fontsize=14)
ax2.legend(loc='best', fontsize=11)
ax2.grid(True, alpha=0.3)

# Colorbar
sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=force.min(), vmax=force.max()))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax2)
cbar.set_label('Force (N)', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'force_scaling_detailed.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {OUTPUT_DIR / 'force_scaling_detailed.png'}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*80)
print("SUMMARY & RECOMMENDATIONS")
print("="*80)

# Find best model
models_summary = {
    'Linear': r2_linear,
    'Constant Ratio': r2_ratio,
    'Force-Scaled (Quadratic)': 1 - np.sum(residuals_scaling_quad**2) / np.sum((rom_8x8 - np.mean(rom_8x8))**2)
}

best_model = max(models_summary, key=models_summary.get)
best_r2 = models_summary[best_model]

print(f"\n🏆 BEST MODEL: {best_model} (R² = {best_r2:.4f})\n")

if best_model == 'Force-Scaled (Quadratic)':
    print("RECOMMENDED FORMULA:")
    print(f"  ROM_8x8 = ROM_4x4 × [{popt_quad[0]:.8f} × F² + {popt_quad[1]:.6f} × F + {popt_quad[2]:.6f}]")
    print(f"\nwhere F = Prestretch Force (N)")
    print(f"\nExpected error: RMSE = {rmse_scaling_quad:.4f} cm (±{2*rmse_scaling_quad:.4f} cm for 95% CI)")
elif best_model == 'Linear':
    print("RECOMMENDED FORMULA:")
    print(f"  ROM_8x8 = {slope:.6f} × ROM_4x4 + {intercept:.6f}")
    print(f"\nExpected error: RMSE = {np.sqrt(np.mean(residuals_linear**2)):.4f} cm")
else:
    print("RECOMMENDED FORMULA:")
    print(f"  ROM_8x8 = ROM_4x4 × {np.mean(ratio):.6f}")
    print(f"\nExpected error: RMSE = {rmse_ratio:.4f} cm")

print("\n" + "="*80)
print("PHYSICAL INTERPRETATION:")
print("-"*80)
print(f"• 8x8 mesh produces ROM that is ~{np.mean(ratio)*100:.1f}% of 4x4 ROM on average")
print(f"• This ratio varies from {np.min(ratio)*100:.1f}% to {np.max(ratio)*100:.1f}%")
print(f"• The scaling factor shows {'STRONG' if r2_scaling_quad > 0.9 else 'MODERATE'} force-dependence")
print(f"• Higher prestretch forces → {'MORE' if popt_quad[0] < 0 else 'LESS'} difference between meshes")

print("\n" + "="*80)
