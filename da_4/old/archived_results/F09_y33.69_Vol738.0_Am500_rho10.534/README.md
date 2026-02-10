# Parameter Sweep Simulation

## Parameters
- Force: 9 N
- muscle_extent: [4.680342, 4.680342, 33.69] cm
- Volume: 738.0 cm³
- Am: 500 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Fr 5. Dez 01:17:10 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(738.0/33.69) = 4.680342 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F09_y33.69_Vol738.0_Am500_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 9 0 1
```
