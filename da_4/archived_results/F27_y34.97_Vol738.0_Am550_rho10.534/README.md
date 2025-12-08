# Parameter Sweep Simulation

## Parameters
- Force: 27 N
- muscle_extent: [4.593887, 4.593887, 34.97] cm
- Volume: 738.0 cm³
- Am: 550 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Fr 5. Dez 08:31:23 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(738.0/34.97) = 4.593887 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F27_y34.97_Vol738.0_Am550_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 27 0 1
```
