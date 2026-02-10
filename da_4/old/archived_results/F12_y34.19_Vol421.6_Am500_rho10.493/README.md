# Parameter Sweep Simulation

## Parameters
- Force: 12 N
- muscle_extent: [3.511565, 3.511565, 34.19] cm
- Volume: 421.6 cm³
- Am: 500 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Mi 3. Dez 07:36:10 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(421.6/34.19) = 3.511565 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F12_y34.19_Vol421.6_Am500_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 12 0 1
```
