# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 18 N
- Force Actual (at this geometry): 30.657614 N
- Aspect Ratio (b/a): 7.9533
- muscle_extent: [4.527264, 4.527264, 36.006688] cm
- Volume: 738.0 cm³
- Surface Area: 20.496119 cm²
- Am: 450 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 20.496119 cm²
- Area Ratio: 1.7032
- Applied Stress: 1.49577654 N/cm²
- Reference Stress: 1.49577655 N/cm²

## Created
- Date: Sa 7. Mär 12:43:27 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (738.0/7.9533)^(1/3) = 4.527264 cm
- muscle_b = r × a = 7.9533 × 4.527264 = 36.006688 cm
- F_actual = F_target × (A/A_ref) = 18 × (20.496119/12.033883) = 30.657614 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F18_ratio7.9533_Vol738.0_Am450_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 30.657614 0 1
```
