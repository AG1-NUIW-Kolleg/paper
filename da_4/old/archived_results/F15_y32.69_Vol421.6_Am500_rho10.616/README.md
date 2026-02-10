# Parameter Sweep Simulation

## Parameters
- Force: 15 N
- muscle_extent: [3.591226, 3.591226, 32.69] cm
- Volume: 421.6 cm³
- Am: 500 cm⁻¹
- Rho: 10.616 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Sa 6. Dez 11:55:16 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(421.6/32.69) = 3.591226 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F15_y32.69_Vol421.6_Am500_rho10.616/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 15 0 1
```
