# Parameter Sweep Simulation

## Parameters
- Force: 21 N
- muscle_extent: [4.156837, 4.156837, 33.19] cm
- Volume: 573.5 cm³
- Am: 450 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Do 4. Dez 15:31:36 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(573.5/33.19) = 4.156837 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F21_y33.19_Vol573.5_Am450_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 21 0 1
```
