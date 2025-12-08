# Parameter Sweep Simulation

## Parameters
- Force: 6 N
- muscle_extent: [4.332225, 4.332225, 33.69] cm
- Volume: 632.3 cm³
- Am: 550 cm⁻¹
- Rho: 10.493 [1e-4 kg/cm³]
- Simulation Time: 100 ms

## Created
- Date: Do 4. Dez 02:43:00 CET 2025
- Template: /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/cuboid_4x4_prestretch_for_DA

## Calculated Values
- muscle_x = sqrt(Vol/y) = sqrt(632.3/33.69) = 4.332225 cm

## Run Command
```bash
cd /usr/local/home/cmcs-fa01/opendihu-elise/examples/electrophysiology/neuromuscular/parameter_sweep_DA_20251202_130337/F06_y33.69_Vol632.3_Am550_rho10.493/build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 6 0 1
```
