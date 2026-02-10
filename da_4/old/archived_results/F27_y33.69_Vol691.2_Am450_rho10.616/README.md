# Parameter Sweep Simulation

## Parameters
- Force: 27 N
- muscle_extent: [4.529511, 4.529511, 33.69] cm
- Volume: 691.2 cm³
- Am: 450 cm⁻¹
- Rho: 10.616 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Sa 6. Dez 10:01:47 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(691.2/33.69) = 4.529511 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F27_y33.69_Vol691.2_Am450_rho10.616/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 27 0 1
```
