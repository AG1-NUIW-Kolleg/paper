# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 27 N
- Force Actual (at this geometry): 33.146003 N
- Aspect Ratio (a/b): 10.1000
- muscle_extent: [3.843586, 3.843586, 38.820218] cm
- Volume: 573.5 cm³
- Surface Area: 14.773153 cm²
- Am: 550 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 14.773153 cm²
- Area Ratio: 1.2276
- Applied Stress: 2.24366477 N/cm²
- Reference Stress: 2.24366482 N/cm²

## Created
- Date: Mo 9. Feb 18:37:36 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (573.5/10.1000)^(1/3) = 3.843586 cm
- muscle_b = r × a = 10.1000 × 3.843586 = 38.820218 cm
- F_actual = F_target × (A/A_ref) = 27 × (14.773153/12.033883) = 33.146003 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F27_ratio10.1000_Vol573.5_Am550_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 33.146003 0 1
```
