# Parameter Sweep Simulation

## Parameters
- Force: 12 N
- muscle_extent: [3.967981, 3.967981, 32.69] cm
- Volume: 514.7 cm³
- Am: 500 cm⁻¹
- Rho: 10.534 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Do 4. Dez 20:58:18 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(514.7/32.69) = 3.967981 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F12_y32.69_Vol514.7_Am500_rho10.534/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 12 0 1
```
