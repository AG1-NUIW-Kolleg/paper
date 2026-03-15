# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 45 N
- Force Actual (at this geometry): 52.768573 N
- Aspect Ratio (b/a): 7.9533
- muscle_extent: [3.756508, 3.756508, 29.876635] cm
- Volume: 421.6 cm³
- Surface Area: 14.111352 cm²
- Am: 550 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 14.111352 cm²
- Area Ratio: 1.1726
- Applied Stress: 3.73944133 N/cm²
- Reference Stress: 3.73944137 N/cm²

## Created
- Date: Sa 28. Feb 07:43:52 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (421.6/7.9533)^(1/3) = 3.756508 cm
- muscle_b = r × a = 7.9533 × 3.756508 = 29.876635 cm
- F_actual = F_target × (A/A_ref) = 45 × (14.111352/12.033883) = 52.768573 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F45_ratio7.9533_Vol421.6_Am550_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 52.768573 0 1
```
