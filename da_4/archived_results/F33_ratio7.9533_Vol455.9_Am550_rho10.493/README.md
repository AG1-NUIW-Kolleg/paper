# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 33 N
- Force Actual (at this geometry): 40.768227 N
- Aspect Ratio (a/b): 7.9533
- muscle_extent: [3.855732, 3.855732, 30.665793] cm
- Volume: 455.9 cm³
- Surface Area: 14.866669 cm²
- Am: 550 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 14.866669 cm²
- Area Ratio: 1.2354
- Applied Stress: 2.74225699 N/cm²
- Reference Stress: 2.74225700 N/cm²

## Created
- Date: Mo 9. Feb 17:02:33 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (455.9/7.9533)^(1/3) = 3.855732 cm
- muscle_b = r × a = 7.9533 × 3.855732 = 30.665793 cm
- F_actual = F_target × (A/A_ref) = 33 × (14.866669/12.033883) = 40.768227 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F33_ratio7.9533_Vol455.9_Am550_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 40.768227 0 1
```
