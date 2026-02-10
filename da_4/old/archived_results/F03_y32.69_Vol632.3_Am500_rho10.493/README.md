# Parameter Sweep Simulation

## Parameters
- Force: 3 N
- muscle_extent: [4.397988, 4.397988, 32.69] cm
- Volume: 632.3 cm³
- Am: 500 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Mi 3. Dez 11:28:45 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(632.3/32.69) = 4.397988 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F03_y32.69_Vol632.3_Am500_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 3 0 1
```
