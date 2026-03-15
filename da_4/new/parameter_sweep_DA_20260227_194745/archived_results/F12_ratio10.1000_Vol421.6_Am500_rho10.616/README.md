# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 12 N
- Force Actual (at this geometry): 11.999440 N
- Aspect Ratio (b/a): 10.1000
- muscle_extent: [3.468908, 3.468908, 35.035970] cm
- Volume: 421.6 cm³
- Surface Area: 12.033322 cm²
- Am: 500 cm⁻¹
- Rho: 10.616 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 12.033322 cm²
- Area Ratio: .9999
- Applied Stress: .99718431 N/cm²
- Reference Stress: .99718436 N/cm²

## Created
- Date: Sa 28. Feb 17:38:04 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (421.6/10.1000)^(1/3) = 3.468908 cm
- muscle_b = r × a = 10.1000 × 3.468908 = 35.035970 cm
- F_actual = F_target × (A/A_ref) = 12 × (12.033322/12.033883) = 11.999440 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F12_ratio10.1000_Vol421.6_Am500_rho10.616/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 11.999440 0 1
```
