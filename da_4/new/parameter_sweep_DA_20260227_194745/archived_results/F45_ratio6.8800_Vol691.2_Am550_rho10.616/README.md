# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 45 N
- Force Actual (at this geometry): 80.813333 N
- Aspect Ratio (b/a): 6.8800
- muscle_extent: [4.648771, 4.648771, 31.983544] cm
- Volume: 691.2 cm³
- Surface Area: 21.611071 cm²
- Am: 550 cm⁻¹
- Rho: 10.616 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 21.611071 cm²
- Area Ratio: 1.7958
- Applied Stress: 3.73944137 N/cm²
- Reference Stress: 3.73944137 N/cm²

## Created
- Date: Fr 6. Mär 02:53:16 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (691.2/6.8800)^(1/3) = 4.648771 cm
- muscle_b = r × a = 6.8800 × 4.648771 = 31.983544 cm
- F_actual = F_target × (A/A_ref) = 45 × (21.611071/12.033883) = 80.813333 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F45_ratio6.8800_Vol691.2_Am550_rho10.616/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 80.813333 0 1
```
