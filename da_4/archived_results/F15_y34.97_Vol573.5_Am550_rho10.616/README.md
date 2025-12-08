# Parameter Sweep Simulation

## Parameters
- Force: 15 N
- muscle_extent: [4.049663, 4.049663, 34.97] cm
- Volume: 573.5 cm³
- Am: 550 cm⁻¹
- Rho: 10.616 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Sa 6. Dez 22:26:30 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(573.5/34.97) = 4.049663 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F15_y34.97_Vol573.5_Am550_rho10.616/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 15 0 1
```
