# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 39 N
- Force Actual (at this geometry): 38.998181 N
- Aspect Ratio (b/a): 10.1000
- muscle_extent: [3.468908, 3.468908, 35.035970] cm
- Volume: 421.6 cm³
- Surface Area: 12.033322 cm²
- Am: 550 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 12.033322 cm²
- Area Ratio: .9999
- Applied Stress: 3.24084911 N/cm²
- Reference Stress: 3.24084919 N/cm²

## Created
- Date: Sa 28. Feb 19:25:37 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (421.6/10.1000)^(1/3) = 3.468908 cm
- muscle_b = r × a = 10.1000 × 3.468908 = 35.035970 cm
- F_actual = F_target × (A/A_ref) = 39 × (12.033322/12.033883) = 38.998181 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F39_ratio10.1000_Vol421.6_Am550_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 38.998181 0 1
```
