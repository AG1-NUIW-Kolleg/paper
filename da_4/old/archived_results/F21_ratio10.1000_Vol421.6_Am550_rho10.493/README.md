# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 21 N
- Force Actual (at this geometry): 20.998984 N
- Aspect Ratio (a/b): 10.1000
- muscle_extent: [3.468905, 3.468905, 35.035940] cm
- Volume: 421.6 cm³
- Surface Area: 12.033301 cm²
- Am: 550 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 12.033301 cm²
- Area Ratio: .9999
- Applied Stress: 1.74507261 N/cm²
- Reference Stress: 1.74507264 N/cm²

## Created
- Date: Mo 9. Feb 16:38:52 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (421.6/10.1000)^(1/3) = 3.468905 cm
- muscle_b = r × a = 10.1000 × 3.468905 = 35.035940 cm
- F_actual = F_target × (A/A_ref) = 21 × (12.033301/12.033883) = 20.998984 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F21_ratio10.1000_Vol421.6_Am550_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 20.998984 0 1
```
