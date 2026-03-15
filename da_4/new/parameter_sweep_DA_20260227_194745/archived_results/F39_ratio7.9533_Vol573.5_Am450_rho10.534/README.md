# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 39 N
- Force Actual (at this geometry): 56.145524 N
- Aspect Ratio (b/a): 7.9533
- muscle_extent: [4.162250, 4.162250, 33.103622] cm
- Volume: 573.5 cm³
- Surface Area: 17.324325 cm²
- Am: 450 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 17.324325 cm²
- Area Ratio: 1.4396
- Applied Stress: 3.24084915 N/cm²
- Reference Stress: 3.24084919 N/cm²

## Created
- Date: Mo 2. Mär 18:09:54 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (573.5/7.9533)^(1/3) = 4.162250 cm
- muscle_b = r × a = 7.9533 × 4.162250 = 33.103622 cm
- F_actual = F_target × (A/A_ref) = 39 × (17.324325/12.033883) = 56.145524 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F39_ratio7.9533_Vol573.5_Am450_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 56.145524 0 1
```
