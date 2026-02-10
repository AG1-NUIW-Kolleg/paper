# Parameter Sweep Simulation

## Parameters
- Force: 27 N
- muscle_extent: [4.715465, 4.715465, 33.19] cm
- Volume: 738.0 cm³
- Am: 550 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Do 4. Dez 04:38:33 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(738.0/33.19) = 4.715465 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F27_y33.19_Vol738.0_Am550_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 27 0 1
```
