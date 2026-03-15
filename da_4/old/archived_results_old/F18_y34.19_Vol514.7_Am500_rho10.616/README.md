# Parameter Sweep Simulation

## Parameters
- Force: 18 N
- muscle_extent: [3.879962, 3.879962, 34.19] cm
- Volume: 514.7 cm³
- Am: 500 cm⁻¹
- Rho: 10.616 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Sa 6. Dez 14:32:09 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(514.7/34.19) = 3.879962 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F18_y34.19_Vol514.7_Am500_rho10.616/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 18 0 1
```
