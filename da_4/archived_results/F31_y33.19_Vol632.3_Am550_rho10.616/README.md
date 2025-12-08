# Parameter Sweep Simulation

## Parameters
- Force: 31 N
- muscle_extent: [4.364735, 4.364735, 33.19] cm
- Volume: 632.3 cm³
- Am: 550 cm⁻¹
- Rho: 10.616 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Sa 6. Dez 23:00:54 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(632.3/33.19) = 4.364735 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F31_y33.19_Vol632.3_Am550_rho10.616/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 31 0 1
```
