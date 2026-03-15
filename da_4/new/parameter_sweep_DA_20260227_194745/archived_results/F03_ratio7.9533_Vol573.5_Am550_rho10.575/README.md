# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 3 N
- Force Actual (at this geometry): 4.318886 N
- Aspect Ratio (b/a): 7.9533
- muscle_extent: [4.162250, 4.162250, 33.103622] cm
- Volume: 573.5 cm³
- Surface Area: 17.324325 cm²
- Am: 550 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 17.324325 cm²
- Area Ratio: 1.4396
- Applied Stress: .24929606 N/cm²
- Reference Stress: .24929609 N/cm²

## Created
- Date: Mi 4. Mär 12:43:43 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (573.5/7.9533)^(1/3) = 4.162250 cm
- muscle_b = r × a = 7.9533 × 4.162250 = 33.103622 cm
- F_actual = F_target × (A/A_ref) = 3 × (17.324325/12.033883) = 4.318886 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F03_ratio7.9533_Vol573.5_Am550_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 4.318886 0 1
```
