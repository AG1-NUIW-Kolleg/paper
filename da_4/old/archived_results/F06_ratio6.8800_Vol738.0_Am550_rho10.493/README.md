# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 6 N
- Force Actual (at this geometry): 11.256132 N
- Aspect Ratio (a/b): 6.8800
- muscle_extent: [4.751403, 4.751403, 32.689652] cm
- Volume: 738.0 cm³
- Surface Area: 22.575830 cm²
- Am: 550 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 22.575830 cm²
- Area Ratio: 1.8760
- Applied Stress: .49859216 N/cm²
- Reference Stress: .49859218 N/cm²

## Created
- Date: Mo 9. Feb 22:49:34 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (738.0/6.8800)^(1/3) = 4.751403 cm
- muscle_b = r × a = 6.8800 × 4.751403 = 32.689652 cm
- F_actual = F_target × (A/A_ref) = 6 × (22.575830/12.033883) = 11.256132 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F06_ratio6.8800_Vol738.0_Am550_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 11.256132 0 1
```
