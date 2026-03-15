# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 6 N
- Force Actual (at this geometry): 6.466357 N
- Aspect Ratio (b/a): 9.0267
- muscle_extent: [3.601282, 3.601282, 32.507692] cm
- Volume: 421.6 cm³
- Surface Area: 12.969232 cm²
- Am: 450 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 12.969232 cm²
- Area Ratio: 1.0777
- Applied Stress: .49859212 N/cm²
- Reference Stress: .49859218 N/cm²

## Created
- Date: Sa 28. Feb 08:55:09 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (421.6/9.0267)^(1/3) = 3.601282 cm
- muscle_b = r × a = 9.0267 × 3.601282 = 32.507692 cm
- F_actual = F_target × (A/A_ref) = 6 × (12.969232/12.033883) = 6.466357 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F06_ratio9.0267_Vol421.6_Am450_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 6.466357 0 1
```
