# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 9 N
- Force Actual (at this geometry): 10.553692 N
- Aspect Ratio (a/b): 7.9533
- muscle_extent: [3.756504, 3.756504, 29.876603] cm
- Volume: 421.6 cm³
- Surface Area: 14.111322 cm²
- Am: 500 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 14.111322 cm²
- Area Ratio: 1.1726
- Applied Stress: .74788825 N/cm²
- Reference Stress: .74788827 N/cm²

## Created
- Date: Di 10. Feb 05:40:49 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (421.6/7.9533)^(1/3) = 3.756504 cm
- muscle_b = r × a = 7.9533 × 3.756504 = 29.876603 cm
- F_actual = F_target × (A/A_ref) = 9 × (14.111322/12.033883) = 10.553692 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F09_ratio7.9533_Vol421.6_Am500_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 10.553692 0 1
```
