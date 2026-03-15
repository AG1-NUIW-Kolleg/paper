# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 27 N
- Force Actual (at this geometry): 48.487999 N
- Aspect Ratio (b/a): 6.8800
- muscle_extent: [4.648771, 4.648771, 31.983544] cm
- Volume: 691.2 cm³
- Surface Area: 21.611071 cm²
- Am: 500 cm⁻¹
- Rho: 10.616 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 21.611071 cm²
- Area Ratio: 1.7958
- Applied Stress: 2.24366478 N/cm²
- Reference Stress: 2.24366482 N/cm²

## Created
- Date: Do 5. Mär 23:24:15 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (691.2/6.8800)^(1/3) = 4.648771 cm
- muscle_b = r × a = 6.8800 × 4.648771 = 31.983544 cm
- F_actual = F_target × (A/A_ref) = 27 × (21.611071/12.033883) = 48.487999 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F27_ratio6.8800_Vol691.2_Am500_rho10.616/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 48.487999 0 1
```
