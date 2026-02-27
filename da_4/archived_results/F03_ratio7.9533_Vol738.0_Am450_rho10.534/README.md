# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 3 N
- Force Actual (at this geometry): 5.109593 N
- Aspect Ratio (a/b): 7.9533
- muscle_extent: [4.527260, 4.527260, 36.006656] cm
- Volume: 738.0 cm³
- Surface Area: 20.496083 cm²
- Am: 450 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 20.496083 cm²
- Area Ratio: 1.7031
- Applied Stress: .24929607 N/cm²
- Reference Stress: .24929609 N/cm²

## Created
- Date: Di 10. Feb 04:35:08 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (738.0/7.9533)^(1/3) = 4.527260 cm
- muscle_b = r × a = 7.9533 × 4.527260 = 36.006656 cm
- F_actual = F_target × (A/A_ref) = 3 × (20.496083/12.033883) = 5.109593 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F03_ratio7.9533_Vol738.0_Am450_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 5.109593 0 1
```
