# Parameter Sweep Simulation

## Parameters
- Force: 15 N
- muscle_extent: [4.598269, 4.598269, 32.69] cm
- Volume: 691.2 cm³
- Am: 450 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Fr 5. Dez 13:21:01 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(691.2/32.69) = 4.598269 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F15_y32.69_Vol691.2_Am450_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 15 0 1
```
