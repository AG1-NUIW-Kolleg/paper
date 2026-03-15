# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 27 N
- Force Actual (at this geometry): 36.740455 N
- Aspect Ratio (b/a): 6.8800
- muscle_extent: [4.046628, 4.046628, 27.840800] cm
- Volume: 455.9 cm³
- Surface Area: 16.375198 cm²
- Am: 500 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 16.375198 cm²
- Area Ratio: 1.3607
- Applied Stress: 2.24366477 N/cm²
- Reference Stress: 2.24366482 N/cm²

## Created
- Date: Sa 28. Feb 22:55:58 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (455.9/6.8800)^(1/3) = 4.046628 cm
- muscle_b = r × a = 6.8800 × 4.046628 = 27.840800 cm
- F_actual = F_target × (A/A_ref) = 27 × (16.375198/12.033883) = 36.740455 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F27_ratio6.8800_Vol455.9_Am500_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 36.740455 0 1
```
