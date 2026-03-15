# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 27 N
- Force Actual (at this geometry): 34.873755 N
- Aspect Ratio (b/a): 6.8800
- muscle_extent: [3.942488, 3.942488, 27.124317] cm
- Volume: 421.6 cm³
- Surface Area: 15.543211 cm²
- Am: 450 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 15.543211 cm²
- Area Ratio: 1.2916
- Applied Stress: 2.24366477 N/cm²
- Reference Stress: 2.24366482 N/cm²

## Created
- Date: Fr 27. Feb 19:47:53 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (421.6/6.8800)^(1/3) = 3.942488 cm
- muscle_b = r × a = 6.8800 × 3.942488 = 27.124317 cm
- F_actual = F_target × (A/A_ref) = 27 × (15.543211/12.033883) = 34.873755 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F27_ratio6.8800_Vol421.6_Am450_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 34.873755 0 1
```
