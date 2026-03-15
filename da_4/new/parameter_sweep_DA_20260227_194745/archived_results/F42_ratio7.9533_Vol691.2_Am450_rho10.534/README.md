# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 42 N
- Force Actual (at this geometry): 68.477362 N
- Aspect Ratio (b/a): 7.9533
- muscle_extent: [4.429470, 4.429470, 35.228903] cm
- Volume: 691.2 cm³
- Surface Area: 19.620204 cm²
- Am: 450 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 19.620204 cm²
- Area Ratio: 1.6304
- Applied Stress: 3.49014526 N/cm²
- Reference Stress: 3.49014528 N/cm²

## Created
- Date: Fr 6. Mär 04:13:52 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (691.2/7.9533)^(1/3) = 4.429470 cm
- muscle_b = r × a = 7.9533 × 4.429470 = 35.228903 cm
- F_actual = F_target × (A/A_ref) = 42 × (19.620204/12.033883) = 68.477362 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F42_ratio7.9533_Vol691.2_Am450_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 68.477362 0 1
```
