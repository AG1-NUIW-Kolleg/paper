# Parameter Sweep Simulation

## Parameters
- Force: 0 N
- muscle_extent: [3.564073, 3.564073, 33.19] cm
- Volume: 421.6 cm³
- Am: 550 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Mi 3. Dez 22:38:47 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(421.6/33.19) = 3.564073 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F00_y33.19_Vol421.6_Am550_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 0 0 1
```
