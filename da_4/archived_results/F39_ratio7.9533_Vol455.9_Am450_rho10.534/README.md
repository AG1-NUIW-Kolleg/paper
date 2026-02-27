# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 39 N
- Force Actual (at this geometry): 48.180632 N
- Aspect Ratio (a/b): 7.9533
- muscle_extent: [3.855732, 3.855732, 30.665793] cm
- Volume: 455.9 cm³
- Surface Area: 14.866669 cm²
- Am: 450 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 14.866669 cm²
- Area Ratio: 1.2354
- Applied Stress: 3.24084917 N/cm²
- Reference Stress: 3.24084919 N/cm²

## Created
- Date: Di 10. Feb 01:26:35 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (455.9/7.9533)^(1/3) = 3.855732 cm
- muscle_b = r × a = 7.9533 × 3.855732 = 30.665793 cm
- F_actual = F_target × (A/A_ref) = 39 × (14.866669/12.033883) = 48.180632 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F39_ratio7.9533_Vol455.9_Am450_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 48.180632 0 1
```
