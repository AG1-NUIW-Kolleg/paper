# Parameter Sweep Simulation (Surface-Area-Adjusted Forces)

## Parameters
- Force Target (at reference area): 39 N
- Force Actual (at this geometry): 56.643160 N
- Aspect Ratio (a/b): 10.1000
- muscle_extent: [4.180655, 4.180655, 42.224615] cm
- Volume: 738.0 cm³
- Surface Area: 17.477876 cm²
- Am: 450 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Force Adjustment
- Reference Area: 12.033883 cm²
- Geometry Area: 17.477876 cm²
- Area Ratio: 1.4523
- Applied Stress: 3.24084917 N/cm²
- Reference Stress: 3.24084919 N/cm²

## Created
- Date: Di 10. Feb 05:18:28 CET 2026
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_a = (Vol/r)^(1/3) = (738.0/10.1000)^(1/3) = 4.180655 cm
- muscle_b = r × a = 10.1000 × 4.180655 = 42.224615 cm
- F_actual = F_target × (A/A_ref) = 39 × (17.477876/12.033883) = 56.643160 N

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20260209_153039/F39_ratio10.1000_Vol738.0_Am450_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 56.643160 0 1
```
