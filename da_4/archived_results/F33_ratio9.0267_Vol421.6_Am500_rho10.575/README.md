# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 33 N
- Force Actual (at this geometry): 35.564887 N
- Aspect Ratio (a/b): 9.0267
- muscle_extent: [3.601278, 3.601278, 32.507656] cm
- Volume: 421.6 cm³
- Surface Area: 12.969203 cm²
- Am: 500 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 12.969203 cm²
- Area Ratio: 1.0777
- Applied Stress: 2.74225694 N/cm²
- Reference Stress: 2.74225700 N/cm²

## Created
- Date: Di 10. Feb 06:04:56 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (421.6/9.0267)^(1/3) = 3.601278 cm
- muscle_b = r × a = 9.0267 × 3.601278 = 32.507656 cm
- F_actual = F_target × (A/A_ref) = 33 × (12.969203/12.033883) = 35.564887 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F33_ratio9.0267_Vol421.6_Am500_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 35.564887 0 1
```
