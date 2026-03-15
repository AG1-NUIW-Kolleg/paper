# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 30 N
- Force Actual (at this geometry): 34.062419 N
- Aspect Ratio (b/a): 9.0267
- muscle_extent: [3.696409, 3.696409, 33.366375] cm
- Volume: 455.9 cm³
- Surface Area: 13.663439 cm²
- Am: 450 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 13.663439 cm²
- Area Ratio: 1.1354
- Applied Stress: 2.49296088 N/cm²
- Reference Stress: 2.49296091 N/cm²

## Created
- Date: So 1. Mär 09:50:23 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (455.9/9.0267)^(1/3) = 3.696409 cm
- muscle_b = r × a = 9.0267 × 3.696409 = 33.366375 cm
- F_actual = F_target × (A/A_ref) = 30 × (13.663439/12.033883) = 34.062419 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F30_ratio9.0267_Vol455.9_Am450_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 34.062419 0 1
```
