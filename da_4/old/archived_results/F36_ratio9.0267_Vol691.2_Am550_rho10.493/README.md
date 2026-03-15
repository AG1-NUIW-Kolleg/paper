# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 36 N
- Force Actual (at this geometry): 53.944212 N
- Aspect Ratio (a/b): 9.0267
- muscle_extent: [4.246431, 4.246431, 38.331258] cm
- Volume: 691.2 cm³
- Surface Area: 18.032176 cm²
- Am: 550 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 18.032176 cm²
- Area Ratio: 1.4984
- Applied Stress: 2.99155309 N/cm²
- Reference Stress: 2.99155310 N/cm²

## Created
- Date: Mo 9. Feb 22:27:01 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (691.2/9.0267)^(1/3) = 4.246431 cm
- muscle_b = r × a = 9.0267 × 4.246431 = 38.331258 cm
- F_actual = F_target × (A/A_ref) = 36 × (18.032176/12.033883) = 53.944212 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F36_ratio9.0267_Vol691.2_Am550_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 53.944212 0 1
```
