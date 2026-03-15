# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 36 N
- Force Actual (at this geometry): 50.051588 N
- Aspect Ratio (b/a): 10.1000
- muscle_extent: [4.090351, 4.090351, 41.312545] cm
- Volume: 691.2 cm³
- Surface Area: 16.730971 cm²
- Am: 500 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 16.730971 cm²
- Area Ratio: 1.3903
- Applied Stress: 2.99155309 N/cm²
- Reference Stress: 2.99155310 N/cm²

## Created
- Date: Sa 7. Mär 01:36:29 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (691.2/10.1000)^(1/3) = 4.090351 cm
- muscle_b = r × a = 10.1000 × 4.090351 = 41.312545 cm
- F_actual = F_target × (A/A_ref) = 36 × (16.730971/12.033883) = 50.051588 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F36_ratio10.1000_Vol691.2_Am500_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 50.051588 0 1
```
