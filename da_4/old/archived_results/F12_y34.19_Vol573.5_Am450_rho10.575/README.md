# Parameter Sweep Simulation

## Parameters
- Force: 12 N
- muscle_extent: [4.095596, 4.095596, 34.19] cm
- Volume: 573.5 cm³
- Am: 450 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Fr 5. Dez 11:52:18 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(573.5/34.19) = 4.095596 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F12_y34.19_Vol573.5_Am450_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 12 0 1
```
