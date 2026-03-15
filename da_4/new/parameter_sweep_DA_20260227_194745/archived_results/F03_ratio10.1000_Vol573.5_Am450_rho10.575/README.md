# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 3 N
- Force Actual (at this geometry): 3.682897 N
- Aspect Ratio (b/a): 10.1000
- muscle_extent: [3.843590, 3.843590, 38.820259] cm
- Volume: 573.5 cm³
- Surface Area: 14.773184 cm²
- Am: 450 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 14.773184 cm²
- Area Ratio: 1.2276
- Applied Stress: .24929608 N/cm²
- Reference Stress: .24929609 N/cm²

## Created
- Date: Do 5. Mär 05:07:31 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (573.5/10.1000)^(1/3) = 3.843590 cm
- muscle_b = r × a = 10.1000 × 3.843590 = 38.820259 cm
- F_actual = F_target × (A/A_ref) = 3 × (14.773184/12.033883) = 3.682897 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F03_ratio10.1000_Vol573.5_Am450_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 3.682897 0 1
```
