# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 39 N
- Force Actual (at this geometry): 47.877661 N
- Aspect Ratio (b/a): 10.1000
- muscle_extent: [3.843590, 3.843590, 38.820259] cm
- Volume: 573.5 cm³
- Surface Area: 14.773184 cm²
- Am: 450 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 14.773184 cm²
- Area Ratio: 1.2276
- Applied Stress: 3.24084916 N/cm²
- Reference Stress: 3.24084919 N/cm²

## Created
- Date: Do 5. Mär 04:16:07 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (573.5/10.1000)^(1/3) = 3.843590 cm
- muscle_b = r × a = 10.1000 × 3.843590 = 38.820259 cm
- F_actual = F_target × (A/A_ref) = 39 × (14.773184/12.033883) = 47.877661 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F39_ratio10.1000_Vol573.5_Am450_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 47.877661 0 1
```
