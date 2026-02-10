# Parameter Sweep Simulation

## Parameters
- Force: 3 N
- muscle_extent: [3.678614, 3.678614, 33.69] cm
- Volume: 455.9 cm³
- Am: 500 cm⁻¹
- Rho: 10.616 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Sa 6. Dez 13:21:58 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(455.9/33.69) = 3.678614 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F03_y33.69_Vol455.9_Am500_rho10.616/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 3 0 1
```
