# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 9 N
- Force Actual (at this geometry): 12.246793 N
- Aspect Ratio (a/b): 6.8800
- muscle_extent: [4.046624, 4.046624, 27.840773] cm
- Volume: 455.9 cm³
- Surface Area: 16.375165 cm²
- Am: 550 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 16.375165 cm²
- Area Ratio: 1.3607
- Applied Stress: .74788821 N/cm²
- Reference Stress: .74788827 N/cm²

## Created
- Date: Mo 9. Feb 16:38:59 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (455.9/6.8800)^(1/3) = 4.046624 cm
- muscle_b = r × a = 6.8800 × 4.046624 = 27.840773 cm
- F_actual = F_target × (A/A_ref) = 9 × (16.375165/12.033883) = 12.246793 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F09_ratio6.8800_Vol455.9_Am550_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 12.246793 0 1
```
