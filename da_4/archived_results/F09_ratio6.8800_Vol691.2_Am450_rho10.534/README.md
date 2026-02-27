# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 9 N
- Force Actual (at this geometry): 16.162632 N
- Aspect Ratio (a/b): 6.8800
- muscle_extent: [4.648766, 4.648766, 31.983510] cm
- Volume: 691.2 cm³
- Surface Area: 21.611025 cm²
- Am: 450 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 21.611025 cm²
- Area Ratio: 1.7958
- Applied Stress: .74788826 N/cm²
- Reference Stress: .74788827 N/cm²

## Created
- Date: Di 10. Feb 03:08:13 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (691.2/6.8800)^(1/3) = 4.648766 cm
- muscle_b = r × a = 6.8800 × 4.648766 = 31.983510 cm
- F_actual = F_target × (A/A_ref) = 9 × (21.611025/12.033883) = 16.162632 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F09_ratio6.8800_Vol691.2_Am450_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 16.162632 0 1
```
