# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 12 N
- Force Actual (at this geometry): 19.028508 N
- Aspect Ratio (b/a): 6.8800
- muscle_extent: [4.368322, 4.368322, 30.054055] cm
- Volume: 573.5 cm³
- Surface Area: 19.082237 cm²
- Am: 500 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 19.082237 cm²
- Area Ratio: 1.5857
- Applied Stress: .99718434 N/cm²
- Reference Stress: .99718436 N/cm²

## Created
- Date: Mo 2. Mär 10:29:45 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (573.5/6.8800)^(1/3) = 4.368322 cm
- muscle_b = r × a = 6.8800 × 4.368322 = 30.054055 cm
- F_actual = F_target × (A/A_ref) = 12 × (19.082237/12.033883) = 19.028508 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F12_ratio6.8800_Vol573.5_Am500_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 19.028508 0 1
```
