# Parameter Sweep Simulation

## Parameters
- Force: 18 N
- muscle_extent: [4.751390, 4.751390, 32.69] cm
- Volume: 738.0 cm³
- Am: 550 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Do 4. Dez 04:26:00 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(738.0/32.69) = 4.751390 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F18_y32.69_Vol738.0_Am550_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 18 0 1
```
