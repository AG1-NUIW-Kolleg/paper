# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 3 N
- Force Actual (at this geometry): 3.969331 N
- Aspect Ratio (a/b): 9.0267
- muscle_extent: [3.990258, 3.990258, 36.018861] cm
- Volume: 573.5 cm³
- Surface Area: 15.922158 cm²
- Am: 500 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 15.922158 cm²
- Area Ratio: 1.3231
- Applied Stress: .24929604 N/cm²
- Reference Stress: .24929609 N/cm²

## Created
- Date: Di 10. Feb 11:56:03 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (573.5/9.0267)^(1/3) = 3.990258 cm
- muscle_b = r × a = 9.0267 × 3.990258 = 36.018861 cm
- F_actual = F_target × (A/A_ref) = 3 × (15.922158/12.033883) = 3.969331 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F03_ratio9.0267_Vol573.5_Am500_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 3.969331 0 1
```
