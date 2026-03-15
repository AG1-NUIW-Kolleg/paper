# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 15 N
- Force Actual (at this geometry): 19.374308 N
- Aspect Ratio (b/a): 6.8800
- muscle_extent: [3.942488, 3.942488, 27.124317] cm
- Volume: 421.6 cm³
- Surface Area: 15.543211 cm²
- Am: 550 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 15.543211 cm²
- Area Ratio: 1.2916
- Applied Stress: 1.24648040 N/cm²
- Reference Stress: 1.24648045 N/cm²

## Created
- Date: Sa 28. Feb 00:25:23 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (421.6/6.8800)^(1/3) = 3.942488 cm
- muscle_b = r × a = 6.8800 × 3.942488 = 27.124317 cm
- F_actual = F_target × (A/A_ref) = 15 × (15.543211/12.033883) = 19.374308 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F15_ratio6.8800_Vol421.6_Am550_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 19.374308 0 1
```
