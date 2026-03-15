# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 36 N
- Force Actual (at this geometry): 56.352499 N
- Aspect Ratio (a/b): 9.0267
- muscle_extent: [4.340185, 4.340185, 39.177547] cm
- Volume: 738.0 cm³
- Surface Area: 18.837205 cm²
- Am: 500 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 18.837205 cm²
- Area Ratio: 1.5653
- Applied Stress: 2.99155309 N/cm²
- Reference Stress: 2.99155310 N/cm²

## Created
- Date: Di 10. Feb 15:10:04 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (738.0/9.0267)^(1/3) = 4.340185 cm
- muscle_b = r × a = 9.0267 × 4.340185 = 39.177547 cm
- F_actual = F_target × (A/A_ref) = 36 × (18.837205/12.033883) = 56.352499 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F36_ratio9.0267_Vol738.0_Am500_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 56.352499 0 1
```
