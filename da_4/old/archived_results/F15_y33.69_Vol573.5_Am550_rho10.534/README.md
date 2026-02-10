# Parameter Sweep Simulation

## Parameters
- Force: 15 N
- muscle_extent: [4.125876, 4.125876, 33.69] cm
- Volume: 573.5 cm³
- Am: 550 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Fr 5. Dez 05:15:41 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(573.5/33.69) = 4.125876 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F15_y33.69_Vol573.5_Am550_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 15 0 1
```
