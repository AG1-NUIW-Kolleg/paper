# Parameter Sweep Simulation

## Parameters
- Force: 27 N
- muscle_extent: [4.188507, 4.188507, 32.69] cm
- Volume: 573.5 cm³
- Am: 500 cm⁻¹
- Rho: 10.575 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Fr 5. Dez 18:24:11 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(573.5/32.69) = 4.188507 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F27_y32.69_Vol573.5_Am500_rho10.575/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 27 0 1
```
