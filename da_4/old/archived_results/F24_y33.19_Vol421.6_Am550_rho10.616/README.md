# Parameter Sweep Simulation

## Parameters
- Force: 24 N
- muscle_extent: [3.564073, 3.564073, 33.19] cm
- Volume: 421.6 cm³
- Am: 550 cm⁻¹
- Rho: 10.616 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Sa 6. Dez 18:57:04 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(421.6/33.19) = 3.564073 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F24_y33.19_Vol421.6_Am550_rho10.616/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 24 0 1
```
