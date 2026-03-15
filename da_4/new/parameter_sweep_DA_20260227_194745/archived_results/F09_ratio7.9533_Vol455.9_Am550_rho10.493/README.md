# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 9 N
- Force Actual (at this geometry): 11.118630 N
- Aspect Ratio (b/a): 7.9533
- muscle_extent: [3.855736, 3.855736, 30.665825] cm
- Volume: 455.9 cm³
- Surface Area: 14.866700 cm²
- Am: 550 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 14.866700 cm²
- Area Ratio: 1.2354
- Applied Stress: .74788823 N/cm²
- Reference Stress: .74788827 N/cm²

## Created
- Date: So 1. Mär 06:39:01 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (455.9/7.9533)^(1/3) = 3.855736 cm
- muscle_b = r × a = 7.9533 × 3.855736 = 30.665825 cm
- F_actual = F_target × (A/A_ref) = 9 × (14.866700/12.033883) = 11.118630 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F09_ratio7.9533_Vol455.9_Am550_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 11.118630 0 1
```
