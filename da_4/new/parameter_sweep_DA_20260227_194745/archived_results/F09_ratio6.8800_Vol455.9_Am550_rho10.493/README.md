# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 9 N
- Force Actual (at this geometry): 12.246818 N
- Aspect Ratio (b/a): 6.8800
- muscle_extent: [4.046628, 4.046628, 27.840800] cm
- Volume: 455.9 cm³
- Surface Area: 16.375198 cm²
- Am: 550 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 16.375198 cm²
- Area Ratio: 1.3607
- Applied Stress: .74788823 N/cm²
- Reference Stress: .74788827 N/cm²

## Created
- Date: So 1. Mär 00:38:43 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (455.9/6.8800)^(1/3) = 4.046628 cm
- muscle_b = r × a = 6.8800 × 4.046628 = 27.840800 cm
- F_actual = F_target × (A/A_ref) = 9 × (16.375198/12.033883) = 12.246818 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F09_ratio6.8800_Vol455.9_Am550_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 12.246818 0 1
```
