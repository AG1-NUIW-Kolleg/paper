# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 39 N
- Force Actual (at this geometry): 51.601416 N
- Aspect Ratio (b/a): 9.0267
- muscle_extent: [3.990262, 3.990262, 36.018897] cm
- Volume: 573.5 cm³
- Surface Area: 15.922190 cm²
- Am: 550 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 15.922190 cm²
- Area Ratio: 1.3231
- Applied Stress: 3.24084915 N/cm²
- Reference Stress: 3.24084919 N/cm²

## Created
- Date: Do 5. Mär 03:15:27 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (573.5/9.0267)^(1/3) = 3.990262 cm
- muscle_b = r × a = 9.0267 × 3.990262 = 36.018897 cm
- F_actual = F_target × (A/A_ref) = 39 × (15.922190/12.033883) = 51.601416 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F39_ratio9.0267_Vol573.5_Am550_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 51.601416 0 1
```
