# Parameter Sweep Simulation

## Parameters
- Force: 3 N
- muscle_extent: [4.496269, 4.496269, 34.19] cm
- Volume: 691.2 cm³
- Am: 500 cm⁻¹
- Rho: 10.616 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Sa 6. Dez 17:27:28 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(691.2/34.19) = 4.496269 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F03_y34.19_Vol691.2_Am500_rho10.616/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 3 0 1
```
