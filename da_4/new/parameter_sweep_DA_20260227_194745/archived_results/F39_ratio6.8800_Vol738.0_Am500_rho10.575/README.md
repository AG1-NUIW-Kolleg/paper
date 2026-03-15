# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 39 N
- Force Actual (at this geometry): 73.165012 N
- Aspect Ratio (b/a): 6.8800
- muscle_extent: [4.751408, 4.751408, 32.689687] cm
- Volume: 738.0 cm³
- Surface Area: 22.575877 cm²
- Am: 500 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 200 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 22.575877 cm²
- Area Ratio: 1.8760
- Applied Stress: 3.24084915 N/cm²
- Reference Stress: 3.24084919 N/cm²

## Created
- Date: Sa 7. Mär 09:09:38 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_muscle_with_prestretch_4x4

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (738.0/6.8800)^(1/3) = 4.751408 cm
- muscle_b = r × a = 6.8800 × 4.751408 = 32.689687 cm
- F_actual = F_target × (A/A_ref) = 39 × (22.575877/12.033883) = 73.165012 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260227_194745/F39_ratio6.8800_Vol738.0_Am500_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 73.165012 0 1
```
