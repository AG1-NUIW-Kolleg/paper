# Parameter Sweep Simulation

## Parameters
- Force: 15 N
- muscle_extent: [3.836447, 3.836447, 34.97] cm
- Volume: 514.7 cm³
- Am: 500 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Fr 5. Dez 18:07:00 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(514.7/34.97) = 3.836447 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F15_y34.97_Vol514.7_Am500_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 15 0 1
```
