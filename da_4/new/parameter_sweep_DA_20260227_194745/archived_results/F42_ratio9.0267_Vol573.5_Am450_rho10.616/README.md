# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 42 N
- Force Actual (at this geometry): 55.570756 N
- Aspect Ratio (b/a): 9.0267
- muscle_extent: [3.990262, 3.990262, 36.018897] cm
- Volume: 573.5 cm³
- Surface Area: 15.922190 cm²
- Am: 450 cm⁻¹
- Rho: 10.616 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 15.922190 cm²
- Area Ratio: 1.3231
- Applied Stress: 3.49014526 N/cm²
- Reference Stress: 3.49014528 N/cm²

## Created
- Date: Mi 4. Mär 23:34:51 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (573.5/9.0267)^(1/3) = 3.990262 cm
- muscle_b = r × a = 9.0267 × 3.990262 = 36.018897 cm
- F_actual = F_target × (A/A_ref) = 42 × (15.922190/12.033883) = 55.570756 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F42_ratio9.0267_Vol573.5_Am450_rho10.616/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 55.570756 0 1
```
