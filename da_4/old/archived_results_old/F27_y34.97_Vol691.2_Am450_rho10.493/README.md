# Parameter Sweep Simulation

## Parameters
- Force: 27 N
- muscle_extent: [4.445842, 4.445842, 34.97] cm
- Volume: 691.2 cm³
- Am: 450 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Mi 3. Dez 05:36:48 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(691.2/34.97) = 4.445842 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F27_y34.97_Vol691.2_Am450_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 27 0 1
```
