# Cuboid Muscle with Prestretch

This folder contains a cuboid muscle simulation with **force-based prestretch**.

## Overview

The simulation runs in two phases:

1. **Prestretch Phase** (`dynamic = False`): 
   - Applies initial traction force to the muscle via Neumann boundary conditions
   - The muscle is stretched by applying tensile force on the top surface
   - The resulting elongation depends on material properties (nonlinear)
   - This creates an initial strained configuration before activation

2. **Contraction Phase** (`dynamic = True`):
   - Starts from the pre-stretched state
   - Simulates muscle activation and contraction
   - Boundary conditions are changed (top surface force is removed)

Both phases couple `FastMonodomainSolver` + `MuscleContractionSolver`.

## Prestretch Definition

**IMPORTANT**: Prestretch is specified as **Traction Force** in Newtons.

### Force-Based Approach:

```
F = traction force applied to top surface [N]
```

where:
- `L₀` = unloaded muscle length (rest length) = 15 cm
- `F` = tensile force applied to top surface
- Actual elongation depends on **nonlinear material response**

### Example Force Values:

| Force F | Approximate Elongation* | Approximate Strain* |
|---------|------------------------|---------------------|
| 0.0 N   | 0.0 cm                 | 0%                  |
| 2.0 N   | ~0.5 cm                | ~3%                 |
| 5.0 N   | ~1.5 cm                | ~10%                |
| 10.0 N  | ~3.0 cm                | ~20%                |

*Actual values depend on Mooney-Rivlin parameters and must be measured a posteriori.

### Implementation:

- Applied via **Neumann boundary conditions** (prescribed traction)
- Top surface elements receive: `traction_vector = [0, 0, F]`
- Resulting elongation depends on material stiffness (nonlinear)
- More physiologically realistic than displacement control
- Actual elongation measured from output file `muscle_length_prestretch.csv`

## Compilation

```bash
mkorn && sr
```

Or:

```bash
scons
```

## Running the Simulation

```bash
cd build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py <force> [<rank>] [<n_ranks>]
```

where:
- `<force>` = traction force in Newtons (optional, default: 0.0 or from variables.py)
- `<rank>` = MPI rank (optional, auto-filled by MPI)
- `<n_ranks>` = total MPI processes (optional, auto-filled by MPI)

### Examples:

```bash
# No prestretch (rest length)
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 0.0

# 2 N force (produces ~0.5 cm elongation)
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 2.0

# 5 N force (produces ~1.5 cm elongation)
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 5.0

# 10 N force (produces ~3.0 cm elongation, ~20% strain)
./muscle_with_prestretch ../settings_muscle_with_prestretch.py 10.0
```

### Useful Range:

- **Physiological**: F = 0.0 to ~10 N (produces 0% to ~20% elongation)
- **Extended**: F = 0.0 to ~15 N (may produce up to ~30% elongation)
- Values > 15 N may cause numerical instability or exceed physiological limits
- **Note**: Actual elongations are nonlinear and must be verified from output files

## Requirements

- `OPENDIHU_HOME` environment variable must be set
- CellML model files in `$OPENDIHU_HOME/examples/electrophysiology/input/`

## Output Files

- `muscle_length_prestretch.csv`: Muscle length during prestretch phase
- `muscle_length_contraction.csv`: Muscle length during contraction phase
- `out/default/`: Paraview visualization files
- `logs/log.csv`: Simulation metrics (runtime, DOFs, etc.)

## Implementation Details

### Boundary Conditions

#### Mathematical Background

**Dirichlet Boundary Conditions (Essential BC):**
- Prescribe the **displacement field** directly: $\mathbf{u}|_{\Gamma_D} = \bar{\mathbf{u}}$
- Example: $u_z = \varepsilon \cdot L_0$ on top surface (displacement-controlled)
- **Geometric control**: Exact elongation known a priori
- **Force unknown**: Reaction force depends on material stiffness
- In weak form: Enforced as **constraints** on displacement DOFs

**Neumann Boundary Conditions (Natural BC):**
- Prescribe the **traction vector** (stress boundary condition): $\boldsymbol{\sigma} \cdot \mathbf{n}|_{\Gamma_N} = \bar{\mathbf{t}}$
- Example: $\mathbf{t} = [0, 0, F/A]$ on top surface (force-controlled)
- **Force control**: Applied force known a priori
- **Displacement unknown**: Elongation depends on material response
- In weak form: Appears as **surface integral** in right-hand side: $\int_{\Gamma_N} \bar{\mathbf{t}} \cdot \mathbf{v} \, dA$

**Key Difference:**
- Dirichlet: "Move surface to position X" → material must generate whatever force needed
- Neumann: "Apply force F to surface" → material deforms according to stiffness
- For nonlinear materials (Mooney-Rivlin), force-displacement relationship is **not linear**!

#### Boundary Conditions in This Simulation

**Prestretch Phase:**
- Bottom surface: Fixed (z = 0) — **Dirichlet BC**
- Top surface: Neumann BC with traction force (traction_vector = [0, 0, F]) — **Neumann BC**
- Lateral surfaces: Rigid body constraints (prevent rotation/lateral translation) — **Dirichlet BC**

**Contraction Phase:**
- Bottom surface: Fixed (z = 0) — **Dirichlet BC**
- All other surfaces: Free (natural BC with zero traction) — **Neumann BC**
- No external loads applied

### Mesh

- **Linear elements**: Used for fiber discretization
  - `n_elements = [4, 4, 10]`
- **Quadratic elements**: Used for mechanics
  - `n_elements_quadratic = [2, 2, 5]` (half in each direction)

### Physical Parameters

- Muscle dimensions: 3 × 3 × 15 cm
- Fibers: 3 × 3 grid
- Material: Mooney-Rivlin with anisotropy (Heidlauf 2016 parameters)
- Density: ρ = 10 × 10⁻⁴ kg/cm³ 