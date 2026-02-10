# Parameter Sweep Simulation

## Parameters
- Force: 15 N
- muscle_extent: [3.651617, 3.651617, 34.19] cm
- Volume: 455.9 cm³
- Am: 450 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Mi 3. Dez 00:42:01 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(455.9/34.19) = 3.651617 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F15_y34.19_Vol455.9_Am450_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 15 0 1
```
