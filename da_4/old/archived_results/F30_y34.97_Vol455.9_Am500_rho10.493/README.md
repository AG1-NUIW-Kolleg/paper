# Parameter Sweep Simulation

## Parameters
- Force: 30 N
- muscle_extent: [3.610663, 3.610663, 34.97] cm
- Volume: 455.9 cm³
- Am: 500 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Mi 3. Dez 09:07:49 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(455.9/34.97) = 3.610663 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F30_y34.97_Vol455.9_Am500_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 30 0 1
```
