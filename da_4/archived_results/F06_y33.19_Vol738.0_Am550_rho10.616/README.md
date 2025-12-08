# Parameter Sweep Simulation

## Parameters
- Force: 6 N
- muscle_extent: [4.715465, 4.715465, 33.19] cm
- Volume: 738.0 cm³
- Am: 550 cm⁻¹
- Rho: 10.616 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: So 7. Dez 00:47:03 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(738.0/33.19) = 4.715465 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F06_y33.19_Vol738.0_Am550_rho10.616/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 6 0 1
```
