# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 3 N
- Force Actual (at this geometry): 4.757127 N
- Aspect Ratio (b/a): 6.8800
- muscle_extent: [4.368322, 4.368322, 30.054055] cm
- Volume: 573.5 cm³
- Surface Area: 19.082237 cm²
- Am: 450 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 19.082237 cm²
- Area Ratio: 1.5857
- Applied Stress: .24929608 N/cm²
- Reference Stress: .24929609 N/cm²

## Created
- Date: Mo 2. Mär 08:38:06 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (573.5/6.8800)^(1/3) = 4.368322 cm
- muscle_b = r × a = 6.8800 × 4.368322 = 30.054055 cm
- F_actual = F_target × (A/A_ref) = 3 × (19.082237/12.033883) = 4.757127 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F03_ratio6.8800_Vol573.5_Am450_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 4.757127 0 1
```
