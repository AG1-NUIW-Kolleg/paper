# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 21 N
- Force Actual (at this geometry): 35.767216 N
- Aspect Ratio (b/a): 7.9533
- muscle_extent: [4.527264, 4.527264, 36.006688] cm
- Volume: 738.0 cm³
- Surface Area: 20.496119 cm²
- Am: 500 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 20.496119 cm²
- Area Ratio: 1.7032
- Applied Stress: 1.74507261 N/cm²
- Reference Stress: 1.74507264 N/cm²

## Created
- Date: Sa 7. Mär 16:10:58 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (738.0/7.9533)^(1/3) = 4.527264 cm
- muscle_b = r × a = 7.9533 × 4.527264 = 36.006688 cm
- F_actual = F_target × (A/A_ref) = 21 × (20.496119/12.033883) = 35.767216 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F21_ratio7.9533_Vol738.0_Am500_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 35.767216 0 1
```
