# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 18 N
- Force Actual (at this geometry): 26.972156 N
- Aspect Ratio (b/a): 9.0267
- muscle_extent: [4.246435, 4.246435, 38.331294] cm
- Volume: 691.2 cm³
- Surface Area: 18.032210 cm²
- Am: 450 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 18.032210 cm²
- Area Ratio: 1.4984
- Applied Stress: 1.49577650 N/cm²
- Reference Stress: 1.49577655 N/cm²

## Created
- Date: Fr 6. Mär 09:49:27 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (691.2/9.0267)^(1/3) = 4.246435 cm
- muscle_b = r × a = 9.0267 × 4.246435 = 38.331294 cm
- F_actual = F_target × (A/A_ref) = 18 × (18.032210/12.033883) = 26.972156 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F18_ratio9.0267_Vol691.2_Am450_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 26.972156 0 1
```
