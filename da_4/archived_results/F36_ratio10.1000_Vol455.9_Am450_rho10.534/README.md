# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 36 N
- Force Actual (at this geometry): 37.925142 N
- Aspect Ratio (a/b): 10.1000
- muscle_extent: [3.560535, 3.560535, 35.961403] cm
- Volume: 455.9 cm³
- Surface Area: 12.677409 cm²
- Am: 450 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 12.677409 cm²
- Area Ratio: 1.0534
- Applied Stress: 2.99155308 N/cm²
- Reference Stress: 2.99155310 N/cm²

## Created
- Date: Di 10. Feb 01:58:12 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (455.9/10.1000)^(1/3) = 3.560535 cm
- muscle_b = r × a = 10.1000 × 3.560535 = 35.961403 cm
- F_actual = F_target × (A/A_ref) = 36 × (12.677409/12.033883) = 37.925142 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F36_ratio10.1000_Vol455.9_Am450_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 37.925142 0 1
```
