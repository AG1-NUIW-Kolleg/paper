# Parameter Sweep Simulation

## Parameters
- Force: 18 N
- muscle_extent: [4.529511, 4.529511, 33.69] cm
- Volume: 691.2 cm³
- Am: 500 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Fr 5. Dez 00:28:29 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(691.2/33.69) = 4.529511 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F18_y33.69_Vol691.2_Am500_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 18 0 1
```
