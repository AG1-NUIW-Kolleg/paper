# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 0 N
- Force Actual (at this geometry): 0 N
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
- Applied Stress: 0 N/cm²
- Reference Stress: 0 N/cm²

## Created
- Date: Sa 28. Feb 00:25:08 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (421.6/6.8800)^(1/3) = 3.942488 cm
- muscle_b = r × a = 6.8800 × 3.942488 = 27.124317 cm
- F_actual = F_target × (A/A_ref) = 0 × (15.543211/12.033883) = 0 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F00_ratio6.8800_Vol421.6_Am550_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 0 0 1
```
