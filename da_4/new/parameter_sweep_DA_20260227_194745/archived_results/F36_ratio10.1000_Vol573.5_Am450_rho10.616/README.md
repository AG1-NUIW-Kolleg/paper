# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 36 N
- Force Actual (at this geometry): 44.194764 N
- Aspect Ratio (b/a): 10.1000
- muscle_extent: [3.843590, 3.843590, 38.820259] cm
- Volume: 573.5 cm³
- Surface Area: 14.773184 cm²
- Am: 450 cm⁻¹
- Rho: 10.616 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 14.773184 cm²
- Area Ratio: 1.2276
- Applied Stress: 2.99155307 N/cm²
- Reference Stress: 2.99155310 N/cm²

## Created
- Date: Do 5. Mär 06:03:40 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (573.5/10.1000)^(1/3) = 3.843590 cm
- muscle_b = r × a = 10.1000 × 3.843590 = 38.820259 cm
- F_actual = F_target × (A/A_ref) = 36 × (14.773184/12.033883) = 44.194764 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F36_ratio10.1000_Vol573.5_Am450_rho10.616/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 44.194764 0 1
```
