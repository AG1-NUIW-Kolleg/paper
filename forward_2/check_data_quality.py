#!/usr/bin/env python3
"""
Deep Data Quality Check: Why is R² only 0.83?

Investigates potential issues with the data or model assumptions.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

# Load data
CSV_FILE = Path("analysis/complete_results.csv")
OUTPUT_DIR = Path("analysis/data_quality_check")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

df = pd.read_csv(CSV_FILE)
df_clean = df.dropna(subset=['4x4_ROM_cm', '8x8_ROM_cm'])

force = df_clean['Force_N'].values
rom_4x4 = df_clean['4x4_ROM_cm'].values
rom_8x8 = df_clean['8x8_ROM_cm'].values
z_max_4x4 = df_clean['4x4_z_max_cm'].values
z_min_4x4 = df_clean['4x4_z_min_cm'].values
z_max_8x8 = df_clean['8x8_z_max_cm'].values
z_min_8x8 = df_clean['8x8_z_min_cm'].values
prestretch_4x4 = df_clean['4x4_prestretch_elongation_cm'].values
prestretch_8x8 = df_clean['8x8_prestretch_elongation_cm'].values

print("="*80)
print("DATA QUALITY & HYPOTHESIS CHECK")
print("="*80)

# ============================================================================
# HYPOTHESIS 1: Maybe z_max and z_min are comparable, but ROM calculation differs?
# ============================================================================
print("\n[HYPOTHESIS 1] Are z_max and z_min comparable between meshes?")
print("-"*80)

# Check if z_max is similar
slope_zmax, intercept_zmax, r_zmax, _, _ = stats.linregress(z_max_4x4, z_max_8x8)
r2_zmax = r_zmax**2
print(f"z_max relationship: 8x8 = {slope_zmax:.4f} × 4x4 + {intercept_zmax:.4f}")
print(f"  R² = {r2_zmax:.4f}")

# Check if z_min is similar
slope_zmin, intercept_zmin, r_zmin, _, _ = stats.linregress(z_min_4x4, z_min_8x8)
r2_zmin = r_zmin**2
print(f"z_min relationship: 8x8 = {slope_zmin:.4f} × 4x4 + {intercept_zmin:.4f}")
print(f"  R² = {r2_zmin:.4f}")

if r2_zmax > 0.95 and r2_zmin > 0.95:
    print("✓ z_max and z_min are highly correlated! ROM difference is calculation artifact.")
else:
    print("✗ z_max or z_min differ significantly between meshes")

# ============================================================================
# HYPOTHESIS 2: Check if muscle lengths are comparable
# ============================================================================
print("\n[HYPOTHESIS 2] Are the muscle geometries actually the same?")
print("-"*80)

# Initial length should be identical if same geometry
print(f"Initial muscle length (should be ~35 cm):")
print(f"  4x4: {z_max_4x4[0]:.6f} cm (at F=0)")
print(f"  8x8: {z_max_8x8[0]:.6f} cm (at F=0)")
print(f"  Difference: {abs(z_max_4x4[0] - z_max_8x8[0])*1000:.3f} μm")

if abs(z_max_4x4[0] - z_max_8x8[0]) > 0.001:
    print("⚠️  WARNING: Initial lengths differ! Meshes may have different geometries!")

# ============================================================================
# HYPOTHESIS 3: Are prestretch elongations consistent?
# ============================================================================
print("\n[HYPOTHESIS 3] Prestretch behavior comparison")
print("-"*80)

print(f"4x4 prestretch range: {prestretch_4x4.min():.6f} to {prestretch_4x4.max():.6f} cm")
print(f"8x8 prestretch range: {prestretch_8x8.min():.6f} to {prestretch_8x8.max():.6f} cm")

if np.allclose(prestretch_4x4, prestretch_4x4[0]):
    print("⚠️  WARNING: All 4x4 prestretch values are identical (likely all 0)!")
    print("   4x4 mesh shows NO prestretch elongation")
    r2_pre = 0
else:
    slope_pre, intercept_pre, r_pre, _, _ = stats.linregress(prestretch_4x4, prestretch_8x8)
    r2_pre = r_pre**2
    print(f"Prestretch elongation: 8x8 = {slope_pre:.4f} × 4x4 + {intercept_pre:.4f}")
    print(f"  R² = {r2_pre:.4f}")

if np.allclose(prestretch_8x8, prestretch_8x8[0]):
    print("⚠️  WARNING: All 8x8 prestretch values are identical!")
else:
    print(f"✓ 8x8 shows prestretch response to force")

# ============================================================================
# HYPOTHESIS 4: Check for outliers
# ============================================================================
print("\n[HYPOTHESIS 4] Outlier detection")
print("-"*80)

# Simple linear model
slope_simple, intercept_simple, _, _, _ = stats.linregress(rom_4x4, rom_8x8)
rom_8x8_pred = slope_simple * rom_4x4 + intercept_simple
residuals = rom_8x8 - rom_8x8_pred

# Find outliers (>2 std)
outlier_threshold = 2 * np.std(residuals)
outliers = np.abs(residuals) > outlier_threshold
n_outliers = np.sum(outliers)

print(f"Outliers (>2σ): {n_outliers}/{len(residuals)}")
if n_outliers > 0:
    print("\nOutlier forces:")
    for i, is_outlier in enumerate(outliers):
        if is_outlier:
            print(f"  F={force[i]:2.0f}N: ROM_4x4={rom_4x4[i]:.4f}, ROM_8x8={rom_8x8[i]:.4f}, "
                  f"Residual={residuals[i]:.4f}")

# ============================================================================
# HYPOTHESIS 5: Maybe the relationship IS actually linear, but slope ≠ 1?
# ============================================================================
print("\n[HYPOTHESIS 5] What if we enforce different physical assumptions?")
print("-"*80)

# Assumption A: Same ROM (slope=1, intercept=0)
rom_8x8_pred_same = rom_4x4
r2_same = 1 - np.sum((rom_8x8 - rom_8x8_pred_same)**2) / np.sum((rom_8x8 - np.mean(rom_8x8))**2)
rmse_same = np.sqrt(np.mean((rom_8x8 - rom_8x8_pred_same)**2))

print(f"A) ROM_8x8 = ROM_4x4 (slope=1, intercept=0)")
print(f"   R² = {r2_same:.4f}, RMSE = {rmse_same:.4f} cm")

# Assumption B: Linear but free slope
rom_8x8_pred_linear = slope_simple * rom_4x4 + intercept_simple
r2_linear = 1 - np.sum((rom_8x8 - rom_8x8_pred_linear)**2) / np.sum((rom_8x8 - np.mean(rom_8x8))**2)
rmse_linear = np.sqrt(np.mean((rom_8x8 - rom_8x8_pred_linear)**2))

print(f"B) ROM_8x8 = {slope_simple:.4f} × ROM_4x4 + {intercept_simple:.4f}")
print(f"   R² = {r2_linear:.4f}, RMSE = {rmse_linear:.4f} cm")

# Assumption C: Constant ratio (through origin)
ratio_mean = np.mean(rom_8x8 / rom_4x4)
rom_8x8_pred_ratio = rom_4x4 * ratio_mean
r2_ratio = 1 - np.sum((rom_8x8 - rom_8x8_pred_ratio)**2) / np.sum((rom_8x8 - np.mean(rom_8x8))**2)
rmse_ratio = np.sqrt(np.mean((rom_8x8 - rom_8x8_pred_ratio)**2))

print(f"C) ROM_8x8 = {ratio_mean:.4f} × ROM_4x4 (constant ratio)")
print(f"   R² = {r2_ratio:.4f}, RMSE = {rmse_ratio:.4f} cm")

# ============================================================================
# HYPOTHESIS 6: Maybe ROM itself has issues - check absolute values
# ============================================================================
print("\n[HYPOTHESIS 6] Are ROM values physically reasonable?")
print("-"*80)

print(f"4x4 ROM range: {rom_4x4.min():.2f} - {rom_4x4.max():.2f} cm (mean: {rom_4x4.mean():.2f})")
print(f"8x8 ROM range: {rom_8x8.min():.2f} - {rom_8x8.max():.2f} cm (mean: {rom_8x8.mean():.2f})")
print(f"\n4x4 ROM / muscle length: {rom_4x4.mean()/35*100:.1f}%")
print(f"8x8 ROM / muscle length: {rom_8x8.mean()/35*100:.1f}%")

# Check variance
print(f"\n4x4 ROM std dev: {rom_4x4.std():.4f} cm (CV: {rom_4x4.std()/rom_4x4.mean()*100:.1f}%)")
print(f"8x8 ROM std dev: {rom_8x8.std():.4f} cm (CV: {rom_8x8.std()/rom_8x8.mean()*100:.1f}%)")

if rom_8x8.std() < rom_4x4.std() / 2:
    print("⚠️  WARNING: 8x8 ROM shows much less variation than 4x4!")
    print("   This could indicate convergence issues or different physics")

# ============================================================================
# VISUALIZATION
# ============================================================================
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# Plot 1: z_max comparison
ax = axes[0, 0]
ax.scatter(z_max_4x4, z_max_8x8, c=force, cmap='viridis', s=80, alpha=0.7, edgecolors='black')
lim = [min(z_max_4x4.min(), z_max_8x8.min()), max(z_max_4x4.max(), z_max_8x8.max())]
ax.plot(lim, lim, 'k--', linewidth=2, alpha=0.5, label='y=x')
ax.plot(lim, slope_zmax*np.array(lim)+intercept_zmax, 'r-', linewidth=2, 
        label=f'R²={r2_zmax:.3f}')
ax.set_xlabel('4x4 z_max (cm)', fontweight='bold')
ax.set_ylabel('8x8 z_max (cm)', fontweight='bold')
ax.set_title(f'Maximum Muscle Length\nSlope={slope_zmax:.4f}', fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 2: z_min comparison
ax = axes[0, 1]
ax.scatter(z_min_4x4, z_min_8x8, c=force, cmap='viridis', s=80, alpha=0.7, edgecolors='black')
lim = [min(z_min_4x4.min(), z_min_8x8.min()), max(z_min_4x4.max(), z_min_8x8.max())]
ax.plot(lim, lim, 'k--', linewidth=2, alpha=0.5, label='y=x')
ax.plot(lim, slope_zmin*np.array(lim)+intercept_zmin, 'r-', linewidth=2,
        label=f'R²={r2_zmin:.3f}')
ax.set_xlabel('4x4 z_min (cm)', fontweight='bold')
ax.set_ylabel('8x8 z_min (cm)', fontweight='bold')
ax.set_title(f'Minimum Muscle Length\nSlope={slope_zmin:.4f}', fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 3: ROM comparison with different models
ax = axes[0, 2]
ax.scatter(rom_4x4, rom_8x8, c=force, cmap='viridis', s=80, alpha=0.7, edgecolors='black')
rom_range = np.array([rom_4x4.min(), rom_4x4.max()])
ax.plot(rom_range, rom_range, 'k--', linewidth=2, alpha=0.5, label='y=x (R²={:.3f})'.format(r2_same))
ax.plot(rom_range, slope_simple*rom_range+intercept_simple, 'r-', linewidth=2,
        label=f'Linear fit (R²={r2_linear:.3f})')
ax.plot(rom_range, ratio_mean*rom_range, 'g-', linewidth=2,
        label=f'Const ratio (R²={r2_ratio:.3f})')
ax.set_xlabel('4x4 ROM (cm)', fontweight='bold')
ax.set_ylabel('8x8 ROM (cm)', fontweight='bold')
ax.set_title('ROM Comparison\nAll Models', fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 4: Prestretch elongation
ax = axes[1, 0]
ax.scatter(prestretch_4x4, prestretch_8x8, c=force, cmap='viridis', s=80, alpha=0.7, edgecolors='black')
ax.set_xlabel('4x4 Prestretch Elongation (cm)', fontweight='bold')
ax.set_ylabel('8x8 Prestretch Elongation (cm)', fontweight='bold')
ax.set_title(f'Prestretch Behavior\nR²={r2_pre:.3f}', fontweight='bold')
ax.grid(True, alpha=0.3)

# Plot 5: ROM vs Force for both
ax = axes[1, 1]
ax.scatter(force, rom_4x4, label='4x4', s=80, alpha=0.7, color='blue', edgecolors='black')
ax.scatter(force, rom_8x8, label='8x8', s=80, alpha=0.7, color='red', edgecolors='black')
ax.set_xlabel('Force (N)', fontweight='bold')
ax.set_ylabel('ROM (cm)', fontweight='bold')
ax.set_title('ROM vs Force\n(Notice 8x8 is flatter!)', fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 6: Residuals histogram
ax = axes[1, 2]
ax.hist(residuals, bins=20, alpha=0.7, color='purple', edgecolor='black')
ax.axvline(0, color='black', linestyle='--', linewidth=2)
ax.set_xlabel('Residuals (cm)', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title(f'Residual Distribution\nMean={np.mean(residuals):.4f}, Std={np.std(residuals):.4f}',
             fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'data_quality_check.png', dpi=300, bbox_inches='tight')
print(f"\n✓ Saved: {OUTPUT_DIR / 'data_quality_check.png'}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("DIAGNOSTIC SUMMARY")
print("="*80)

issues = []

if abs(slope_zmax - 1.0) > 0.05 or abs(slope_zmin - 1.0) > 0.05:
    issues.append("❌ z_max or z_min have non-unity slopes → Meshes measure differently!")

if r2_zmax < 0.95 or r2_zmin < 0.95:
    issues.append("❌ z_max or z_min poorly correlated → Different physics!")

if abs(z_max_4x4[0] - z_max_8x8[0]) > 0.001:
    issues.append("❌ Initial muscle lengths differ → Geometry mismatch!")

if r2_pre < 0.9:
    issues.append("❌ Prestretch behavior differs → Material properties differ!")

if rom_8x8.std() < rom_4x4.std() * 0.5:
    issues.append("⚠️  8x8 ROM variance is much smaller → Possible convergence issue")

if r2_linear < 0.95:
    issues.append("⚠️  Linear ROM relationship is poor (R²={:.3f})".format(r2_linear))

if len(issues) == 0:
    print("\n✅ No major issues detected!")
    print("The relationship is simply force-dependent, which may be physical.")
else:
    print("\n🔍 POTENTIAL ISSUES DETECTED:\n")
    for issue in issues:
        print(f"  {issue}")

print("\n" + "="*80)
print("RECOMMENDATION")
print("="*80)

if abs(slope_zmax - 1.0) < 0.05 and abs(slope_zmin - 1.0) < 0.05 and r2_zmax > 0.95 and r2_zmin > 0.95:
    print("\n✅ z_max and z_min are well-correlated with near-unity slopes!")
    print("   → The ROM calculation itself is consistent")
    print("   → The poor ROM correlation is due to different contraction physics")
    print("\n   CONCLUSION: 8x8 mesh has fundamentally different mechanics")
else:
    print("\n❌ There appear to be systematic differences in how the meshes behave!")
    print("   → Check simulation setup, mesh generation, or material parameters")
    print("   → The meshes may not be properly comparable")

print("\n" + "="*80)
