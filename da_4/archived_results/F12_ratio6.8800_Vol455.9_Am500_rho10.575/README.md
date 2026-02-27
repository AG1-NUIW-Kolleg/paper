# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 12 N
- Force Actual (at this geometry): 16.329058 N
- Aspect Ratio (a/b): 6.8800
- muscle_extent: [4.046624, 4.046624, 27.840773] cm
- Volume: 455.9 cm³
- Surface Area: 16.375165 cm²
- Am: 500 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 16.375165 cm²
- Area Ratio: 1.3607
- Applied Stress: .99718433 N/cm²
- Reference Stress: .99718436 N/cm²

## Created
- Date: Di 10. Feb 06:30:23 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (455.9/6.8800)^(1/3) = 4.046624 cm
- muscle_b = r × a = 6.8800 × 4.046624 = 27.840773 cm
- F_actual = F_target × (A/A_ref) = 12 × (16.375165/12.033883) = 16.329058 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F12_ratio6.8800_Vol455.9_Am500_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 16.329058 0 1
```
