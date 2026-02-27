# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 36 N
- Force Actual (at this geometry): 51.826536 N
- Aspect Ratio (a/b): 7.9533
- muscle_extent: [4.162246, 4.162246, 33.103591] cm
- Volume: 573.5 cm³
- Surface Area: 17.324291 cm²
- Am: 450 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 17.324291 cm²
- Area Ratio: 1.4396
- Applied Stress: 2.99155307 N/cm²
- Reference Stress: 2.99155310 N/cm²

## Created
- Date: Di 10. Feb 02:24:06 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (573.5/7.9533)^(1/3) = 4.162246 cm
- muscle_b = r × a = 7.9533 × 4.162246 = 33.103591 cm
- F_actual = F_target × (A/A_ref) = 36 × (17.324291/12.033883) = 51.826536 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F36_ratio7.9533_Vol573.5_Am450_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 51.826536 0 1
```
