# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 6 N
- Force Actual (at this geometry): 8.714348 N
- Aspect Ratio (b/a): 10.1000
- muscle_extent: [4.180659, 4.180659, 42.224655] cm
- Volume: 738.0 cm³
- Surface Area: 17.477909 cm²
- Am: 450 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 17.477909 cm²
- Area Ratio: 1.4523
- Applied Stress: .49859213 N/cm²
- Reference Stress: .49859218 N/cm²

## Created
- Date: So 8. Mär 08:52:09 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (738.0/10.1000)^(1/3) = 4.180659 cm
- muscle_b = r × a = 10.1000 × 4.180659 = 42.224655 cm
- F_actual = F_target × (A/A_ref) = 6 × (17.477909/12.033883) = 8.714348 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F06_ratio10.1000_Vol738.0_Am450_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 8.714348 0 1
```
