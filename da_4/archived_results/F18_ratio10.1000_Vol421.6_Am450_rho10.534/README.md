# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 18 N
- Force Actual (at this geometry): 17.999129 N
- Aspect Ratio (a/b): 10.1000
- muscle_extent: [3.468905, 3.468905, 35.035940] cm
- Volume: 421.6 cm³
- Surface Area: 12.033301 cm²
- Am: 450 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 12.033301 cm²
- Area Ratio: .9999
- Applied Stress: 1.49577651 N/cm²
- Reference Stress: 1.49577655 N/cm²

## Created
- Date: Di 10. Feb 00:47:46 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (421.6/10.1000)^(1/3) = 3.468905 cm
- muscle_b = r × a = 10.1000 × 3.468905 = 35.035940 cm
- F_actual = F_target × (A/A_ref) = 18 × (12.033301/12.033883) = 17.999129 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F18_ratio10.1000_Vol421.6_Am450_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 17.999129 0 1
```
