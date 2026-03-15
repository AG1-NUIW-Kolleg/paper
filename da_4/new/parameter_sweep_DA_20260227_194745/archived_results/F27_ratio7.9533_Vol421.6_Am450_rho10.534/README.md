# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 27 N
- Force Actual (at this geometry): 31.661144 N
- Aspect Ratio (b/a): 7.9533
- muscle_extent: [3.756508, 3.756508, 29.876635] cm
- Volume: 421.6 cm³
- Surface Area: 14.111352 cm²
- Am: 450 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 14.111352 cm²
- Area Ratio: 1.1726
- Applied Stress: 2.24366481 N/cm²
- Reference Stress: 2.24366482 N/cm²

## Created
- Date: Sa 28. Feb 02:19:17 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (421.6/7.9533)^(1/3) = 3.756508 cm
- muscle_b = r × a = 7.9533 × 3.756508 = 29.876635 cm
- F_actual = F_target × (A/A_ref) = 27 × (14.111352/12.033883) = 31.661144 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F27_ratio7.9533_Vol421.6_Am450_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 31.661144 0 1
```
