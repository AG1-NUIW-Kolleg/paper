# Parameter Sweep Simulation

## Parameters
- Force: 21 N
- muscle_extent: [3.967981, 3.967981, 32.69] cm
- Volume: 514.7 cm³
- Am: 500 cm⁻¹
- Rho: 10.616 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Sa 6. Dez 13:57:12 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(514.7/32.69) = 3.967981 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F21_y32.69_Vol514.7_Am500_rho10.616/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 21 0 1
```
