# Parameter Sweep Simulation

## Parameters
- Force: 9 N
- muscle_extent: [3.706219, 3.706219, 33.19] cm
- Volume: 455.9 cm³
- Am: 450 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Fr 5. Dez 09:43:50 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(455.9/33.19) = 3.706219 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F09_y33.19_Vol455.9_Am450_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 9 0 1
```
