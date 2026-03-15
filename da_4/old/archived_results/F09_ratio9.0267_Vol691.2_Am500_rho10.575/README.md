# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 9 N
- Force Actual (at this geometry): 13.486053 N
- Aspect Ratio (a/b): 9.0267
- muscle_extent: [4.246431, 4.246431, 38.331258] cm
- Volume: 691.2 cm³
- Surface Area: 18.032176 cm²
- Am: 500 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 18.032176 cm²
- Area Ratio: 1.4984
- Applied Stress: .74788827 N/cm²
- Reference Stress: .74788827 N/cm²

## Created
- Date: Di 10. Feb 14:00:09 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (691.2/9.0267)^(1/3) = 4.246431 cm
- muscle_b = r × a = 9.0267 × 4.246431 = 38.331258 cm
- F_actual = F_target × (A/A_ref) = 9 × (18.032176/12.033883) = 13.486053 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F09_ratio9.0267_Vol691.2_Am500_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 13.486053 0 1
```
