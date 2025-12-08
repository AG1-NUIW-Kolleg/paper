# Parameter Sweep Simulation

## Parameters
- Force: 6 N
- muscle_extent: [3.511565, 3.511565, 34.19] cm
- Volume: 421.6 cm³
- Am: 550 cm⁻¹
- Rho: 10.616 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Sa 6. Dez 19:14:29 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(421.6/34.19) = 3.511565 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F06_y34.19_Vol421.6_Am550_rho10.616/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 6 0 1
```
