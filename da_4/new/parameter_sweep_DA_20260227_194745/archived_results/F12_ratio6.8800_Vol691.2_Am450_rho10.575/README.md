# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 12 N
- Force Actual (at this geometry): 21.550222 N
- Aspect Ratio (b/a): 6.8800
- muscle_extent: [4.648771, 4.648771, 31.983544] cm
- Volume: 691.2 cm³
- Surface Area: 21.611071 cm²
- Am: 450 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 21.611071 cm²
- Area Ratio: 1.7958
- Applied Stress: .99718435 N/cm²
- Reference Stress: .99718436 N/cm²

## Created
- Date: Do 5. Mär 12:55:33 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (691.2/6.8800)^(1/3) = 4.648771 cm
- muscle_b = r × a = 6.8800 × 4.648771 = 31.983544 cm
- F_actual = F_target × (A/A_ref) = 12 × (21.611071/12.033883) = 21.550222 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F12_ratio6.8800_Vol691.2_Am450_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 21.550222 0 1
```
