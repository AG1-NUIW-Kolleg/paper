# Parameter Sweep Simulation

## Parameters
- Force: 27 N
- muscle_extent: [4.095596, 4.095596, 34.19] cm
- Volume: 573.5 cm³
- Am: 550 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Do 4. Dez 02:07:05 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(573.5/34.19) = 4.095596 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F27_y34.19_Vol573.5_Am550_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 27 0 1
```
