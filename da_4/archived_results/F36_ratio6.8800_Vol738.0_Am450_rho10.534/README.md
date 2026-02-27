# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 36 N
- Force Actual (at this geometry): 67.536794 N
- Aspect Ratio (a/b): 6.8800
- muscle_extent: [4.751403, 4.751403, 32.689652] cm
- Volume: 738.0 cm³
- Surface Area: 22.575830 cm²
- Am: 450 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 22.575830 cm²
- Area Ratio: 1.8760
- Applied Stress: 2.99155309 N/cm²
- Reference Stress: 2.99155310 N/cm²

## Created
- Date: Di 10. Feb 04:30:17 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (738.0/6.8800)^(1/3) = 4.751403 cm
- muscle_b = r × a = 6.8800 × 4.751403 = 32.689652 cm
- F_actual = F_target × (A/A_ref) = 36 × (22.575830/12.033883) = 67.536794 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F36_ratio6.8800_Vol738.0_Am450_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 67.536794 0 1
```
