# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 30 N
- Force Actual (at this geometry): 37.062102 N
- Aspect Ratio (b/a): 7.9533
- muscle_extent: [3.855736, 3.855736, 30.665825] cm
- Volume: 455.9 cm³
- Surface Area: 14.866700 cm²
- Am: 450 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 14.866700 cm²
- Area Ratio: 1.2354
- Applied Stress: 2.49296091 N/cm²
- Reference Stress: 2.49296091 N/cm²

## Created
- Date: So 1. Mär 03:28:04 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (455.9/7.9533)^(1/3) = 3.855736 cm
- muscle_b = r × a = 7.9533 × 3.855736 = 30.665825 cm
- F_actual = F_target × (A/A_ref) = 30 × (14.866700/12.033883) = 37.062102 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F30_ratio7.9533_Vol455.9_Am450_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 37.062102 0 1
```
