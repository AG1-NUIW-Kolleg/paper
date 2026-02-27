# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 18 N
- Force Actual (at this geometry): 20.437418 N
- Aspect Ratio (a/b): 9.0267
- muscle_extent: [3.696406, 3.696406, 33.366348] cm
- Volume: 455.9 cm³
- Surface Area: 13.663417 cm²
- Am: 500 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 13.663417 cm²
- Area Ratio: 1.1354
- Applied Stress: 1.49577649 N/cm²
- Reference Stress: 1.49577655 N/cm²

## Created
- Date: Di 10. Feb 06:59:52 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (455.9/9.0267)^(1/3) = 3.696406 cm
- muscle_b = r × a = 9.0267 × 3.696406 = 33.366348 cm
- F_actual = F_target × (A/A_ref) = 18 × (13.663417/12.033883) = 20.437418 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F18_ratio9.0267_Vol455.9_Am500_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 20.437418 0 1
```
