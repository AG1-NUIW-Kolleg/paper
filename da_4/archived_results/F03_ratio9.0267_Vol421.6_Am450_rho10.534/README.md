# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 3 N
- Force Actual (at this geometry): 3.233171 N
- Aspect Ratio (a/b): 9.0267
- muscle_extent: [3.601278, 3.601278, 32.507656] cm
- Volume: 421.6 cm³
- Surface Area: 12.969203 cm²
- Am: 450 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 12.969203 cm²
- Area Ratio: 1.0777
- Applied Stress: .24929604 N/cm²
- Reference Stress: .24929609 N/cm²

## Created
- Date: Di 10. Feb 00:24:51 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (421.6/9.0267)^(1/3) = 3.601278 cm
- muscle_b = r × a = 9.0267 × 3.601278 = 32.507656 cm
- F_actual = F_target × (A/A_ref) = 3 × (12.969203/12.033883) = 3.233171 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F03_ratio9.0267_Vol421.6_Am450_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 3.233171 0 1
```
