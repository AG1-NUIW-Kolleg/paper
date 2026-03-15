# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 27 N
- Force Actual (at this geometry): 42.814045 N
- Aspect Ratio (a/b): 6.8800
- muscle_extent: [4.368317, 4.368317, 30.054020] cm
- Volume: 573.5 cm³
- Surface Area: 19.082193 cm²
- Am: 450 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 19.082193 cm²
- Area Ratio: 1.5857
- Applied Stress: 2.24366481 N/cm²
- Reference Stress: 2.24366482 N/cm²

## Created
- Date: Di 10. Feb 02:13:32 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (573.5/6.8800)^(1/3) = 4.368317 cm
- muscle_b = r × a = 6.8800 × 4.368317 = 30.054020 cm
- F_actual = F_target × (A/A_ref) = 27 × (19.082193/12.033883) = 42.814045 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F27_ratio6.8800_Vol573.5_Am450_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 42.814045 0 1
```
