# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 15 N
- Force Actual (at this geometry): 19.374270 N
- Aspect Ratio (a/b): 6.8800
- muscle_extent: [3.942484, 3.942484, 27.124289] cm
- Volume: 421.6 cm³
- Surface Area: 15.543180 cm²
- Am: 500 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 15.543180 cm²
- Area Ratio: 1.2916
- Applied Stress: 1.24648044 N/cm²
- Reference Stress: 1.24648045 N/cm²

## Created
- Date: Di 10. Feb 05:25:10 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (421.6/6.8800)^(1/3) = 3.942484 cm
- muscle_b = r × a = 6.8800 × 3.942484 = 27.124289 cm
- F_actual = F_target × (A/A_ref) = 15 × (15.543180/12.033883) = 19.374270 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F15_ratio6.8800_Vol421.6_Am500_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 19.374270 0 1
```
