# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 0 N
- Force Actual (at this geometry): 0 N
- Aspect Ratio (a/b): 6.8800
- muscle_extent: [3.942484, 3.942484, 27.124289] cm
- Volume: 421.6 cm³
- Surface Area: 15.543180 cm²
- Am: 550 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 15.543180 cm²
- Area Ratio: 1.2916
- Applied Stress: 0 N/cm²
- Reference Stress: 0 N/cm²

## Created
- Date: Di 10. Feb 17:54:26 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (421.6/6.8800)^(1/3) = 3.942484 cm
- muscle_b = r × a = 6.8800 × 3.942484 = 27.124289 cm
- F_actual = F_target × (A/A_ref) = 0 × (15.543180/12.033883) = 0 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260210_175424/F00_ratio6.8800_Vol421.6_Am550_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 0 0 1
```
