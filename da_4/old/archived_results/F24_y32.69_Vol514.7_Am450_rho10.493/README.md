# Parameter Sweep Simulation

## Parameters
- Force: 24 N
- muscle_extent: [3.967981, 3.967981, 32.69] cm
- Volume: 514.7 cm³
- Am: 450 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Mi 3. Dez 01:17:13 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(514.7/32.69) = 3.967981 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F24_y32.69_Vol514.7_Am450_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 24 0 1
```
