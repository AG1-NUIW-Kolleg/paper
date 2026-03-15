# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 0 N
- Force Actual (at this geometry): 0 N
- Aspect Ratio (a/b): 7.9533
- muscle_extent: [3.855732, 3.855732, 30.665793] cm
- Volume: 455.9 cm³
- Surface Area: 14.866669 cm²
- Am: 500 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 14.866669 cm²
- Area Ratio: 1.2354
- Applied Stress: 0 N/cm²
- Reference Stress: 0 N/cm²

## Created
- Date: Di 10. Feb 06:36:36 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (455.9/7.9533)^(1/3) = 3.855732 cm
- muscle_b = r × a = 7.9533 × 3.855732 = 30.665793 cm
- F_actual = F_target × (A/A_ref) = 0 × (14.866669/12.033883) = 0 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F00_ratio7.9533_Vol455.9_Am500_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 0 0 1
```
