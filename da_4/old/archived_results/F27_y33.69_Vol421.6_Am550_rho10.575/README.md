# Parameter Sweep Simulation

## Parameters
- Force: 27 N
- muscle_extent: [3.537527, 3.537527, 33.69] cm
- Volume: 421.6 cm³
- Am: 550 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Fr 5. Dez 22:47:00 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(421.6/33.69) = 3.537527 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F27_y33.69_Vol421.6_Am550_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 27 0 1
```
