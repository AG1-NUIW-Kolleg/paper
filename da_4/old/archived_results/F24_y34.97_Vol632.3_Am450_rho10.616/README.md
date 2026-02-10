# Parameter Sweep Simulation

## Parameters
- Force: 24 N
- muscle_extent: [4.252200, 4.252200, 34.97] cm
- Volume: 632.3 cm³
- Am: 450 cm⁻¹
- Rho: 10.616 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Sa 6. Dez 09:36:25 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(632.3/34.97) = 4.252200 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F24_y34.97_Vol632.3_Am450_rho10.616/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 24 0 1
```
