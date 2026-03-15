# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 9 N
- Force Actual (at this geometry): 13.071523 N
- Aspect Ratio (b/a): 10.1000
- muscle_extent: [4.180659, 4.180659, 42.224655] cm
- Volume: 738.0 cm³
- Surface Area: 17.477909 cm²
- Am: 500 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 17.477909 cm²
- Area Ratio: 1.4523
- Applied Stress: .74788826 N/cm²
- Reference Stress: .74788827 N/cm²

## Created
- Date: So 8. Mär 10:32:35 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (738.0/10.1000)^(1/3) = 4.180659 cm
- muscle_b = r × a = 10.1000 × 4.180659 = 42.224655 cm
- F_actual = F_target × (A/A_ref) = 9 × (17.477909/12.033883) = 13.071523 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F09_ratio10.1000_Vol738.0_Am500_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 13.071523 0 1
```
