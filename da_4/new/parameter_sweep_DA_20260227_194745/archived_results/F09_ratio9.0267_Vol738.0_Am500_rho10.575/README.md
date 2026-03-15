# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 9 N
- Force Actual (at this geometry): 14.088150 N
- Aspect Ratio (b/a): 9.0267
- muscle_extent: [4.340189, 4.340189, 39.177584] cm
- Volume: 738.0 cm³
- Surface Area: 18.837240 cm²
- Am: 500 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 18.837240 cm²
- Area Ratio: 1.5653
- Applied Stress: .74788822 N/cm²
- Reference Stress: .74788827 N/cm²

## Created
- Date: So 8. Mär 04:51:23 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (738.0/9.0267)^(1/3) = 4.340189 cm
- muscle_b = r × a = 9.0267 × 4.340189 = 39.177584 cm
- F_actual = F_target × (A/A_ref) = 9 × (18.837240/12.033883) = 14.088150 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F09_ratio9.0267_Vol738.0_Am500_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 14.088150 0 1
```
