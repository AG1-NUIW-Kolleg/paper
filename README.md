# Code Supplement — *Toward individualised surgical parameter selection via numerical simulations and Bayesian statistics*

The paper develops a three-stage computational pipeline to investigate the
*Agonist–Antagonist Myoneural Interface* (AMI) — a surgical technique that
reconnects an amputated agonist/antagonist muscle pair via a tendon to restore
proprioceptive feedback. The single most influential surgical parameter is the
**prestretch force** applied to the antagonist muscle when it is connected: it
controls the resulting **range of motion (ROM)** but is currently chosen
heuristically because clinical data and high-fidelity simulations are both
scarce.

The pipeline has three components, each one section of the paper and one
top-level directory of this repository:

## 1. Scientific overview

### Forward model (Section 2)
The "canonical" AMI simulation of Homs-Pons et al. (2024) couples two muscles
and a rigid tendon through `preCICE` and is too expensive for iterative
parameter studies. Section 2 reduces the model in two steps:

1. **Geometric reduction**: replace the full agonist–tendon–antagonist chain
   with a single cuboid muscle that mirrors the agonist (the tendon is
   essentially rigid, so its compliance is negligible).
2. **Spatial reduction**: coarsen the 3D mechanics mesh from
   `8 × 8 × 20` linear hexahedral elements (60 fibres, 60 points/fibre) to
   `4 × 4 × 10` (16 fibres, 30 points/fibre).

The reduced model preserves the electromechanical coupling (FastMonodomain +
MuscleContraction with `hodgkin_huxley-razumova` CellML) and the
Mooney-Rivlin material; it reduces wall-clock time per simulation by ≈ 92 %
(7.24 min vs 88.06 min) while reproducing ROM to R² = 1.0000. This is the
simulator used by every downstream stage.

A passive **prestretch phase** (Neumann BC: traction `[0, 0, F]` on the top
surface, bottom face fixed, lateral rigid-body constraints) is followed by an
**activation phase** (top traction released, motor-unit firing pattern from
`MU_firing_times_always.txt`).  The output is the muscle length time-series;
ROM is the peak-to-peak excursion during the activation phase.

### Bayesian optimisation (Section 3)
With the reduced forward model, Section 3 uses BoTorch to search for
`argmax_F ROM(F)`. A Gaussian-process surrogate with an Upper-Confidence-Bound
acquisition (`β = 0.1`) selects the next prestretch to simulate; the loop
terminates by an exponential-moving-average stopping rule (window 2). BO
converges in 13 iterations to a near-optimal prestretch of ≈ 45 N — notably,
ROM is **non-monotone** in F: pushing the prestretch beyond that interior
maximum *decreases* ROM, contrary to a naive intuition.

### Data augmentation (Section 4)
Section 4 embeds the ROM observations into a Bayesian mixed-effects model
to obtain *distributional* ROM predictions that account for inter-subject
variability that the deterministic forward model alone cannot express. Fixed
effects: the prestretch force `θ₁` (quadratic, with cross-terms in aspect
ratio) and muscle geometry `θ₂`. Random effects: membrane surface-to-volume
ratio `Aₘ` (45–55 mm⁻¹) and tissue density `ρ` (1.05–1.06 g/cm³). Inference
follows the two-step working-parameter scheme of Van Dyk & Meng (2001) with a
normal–inverse–Wishart prior, alternating between drawing random-effect
coefficients (Step 1) and drawing fixed effects together with augmented data
(Step 2). The training data is a 1280-point parameter sweep
(5 forces × 4⁴ for `y, V, Aₘ, ρ`) executed on the cuboid simulator.

## 2. Repository layout

```text
paper/
├── cuboid_muscle_with_prestretch/         # Base OpenDiHu simulator (single cuboid muscle)
├── forward_2/                             # Section 2: forward simulation + mesh comparison
│   ├── 4x4/{4x4_0N, 4x4_31N}/             #   reduced-mesh runs (no / max prestretch)
│   ├── 8x8/{8x8_0N, 8x8_31N}/             #   reference-mesh runs
│   ├── ami/                               #   full agonist+tendon+antagonist preCICE setup
│   ├── archived_results/4x4_F*, 8x8_F*/   #   one config per integer prestretch force [N]
│   ├── analysis/                          #   mesh comparison analysis + paper Table 2 inputs
│   ├── run_force_sweep.sh                 #   driver that fires the F=0…31 N sweep in parallel
│   ├── calculate_rom.py                   #   helper: ROM = max(L) − min(L)
│   └── ROM_Analysis_Old_Simulations.ipynb
├── bo_3/                                  # Section 3: Bayesian optimisation
│   ├── src/muscle_with_prestretch.cpp     #   OpenDiHu binary (objective evaluator)
│   ├── settings_muscle_with_prestretch.py
│   ├── variables/variables.py
│   ├── out/bo_cuboid_gp_iter_*.pt         #   GP-state snapshots, one per BO iteration
│   └── out/bo_cuboid.csv                  #   (prestretch_force, ROM) at every BO step
├── da_4/                                  # Section 4: data augmentation
│   ├── new/
│   │   ├── cuboid_muscle_with_prestretch_4x4/        # patched simulator (forces/areas)
│   │   ├── run_parameter_sweep_2702.sh               # 3 840-simulation sweep driver
│   │   ├── parameter_sweep_DA_20260227_194745/       # results of the final sweep
│   │   └── analyze_results_*.ipynb                   # mixed-effect-model analyses
│   └── old/                                          # earlier (deprecated) sweep iterations
├── data/                                  # Curated outputs read by plotting/
│   ├── bo_results/
│   │   ├── bo_cuboid.csv                  #   13 BO evaluations
│   │   └── bo_cuboid_gp_iter_*.pt         #   GP checkpoints
│   ├── data_augmentation_results/
│   │   ├── uniform_prestretches_100.csv   #   DA posterior samples, 100-point training
│   │   ├── uniform_prestretches_500.csv   #   …500-point training
│   │   ├── uniform_prestretches_3764.csv  #   full dataset (3 764 valid simulations)
│   │   └── bo_prestretches_3764.csv       #   DA predictions at the BO-queried prestretches
│   └── all_results_summary.csv            #   master CSV of every simulation in the DA sweep
└── plotting/                              # Final paper figures
    ├── plotting.py                        #   builds Figures 2–4 from data/
    ├── utils.py                           #   shared style + I/O helpers
    └── paper_figures/{*.pdf,*.png}        #   the five rendered figures
```

## 3. Dependencies

### Native (C++) simulator
- [**OpenDiHu**](https://github.com/maierbn/opendihu) — environment variable
  `OPENDIHU_HOME` must point at its top-level directory. `SConstruct`
  delegates to OpenDiHu's `SConstructGeneral` to pick up the compilers and
  PETSc / preCICE bindings.
- [**preCICE**](https://precice.org) — required only by the full AMI case in
  `forward_2/ami/` (the cuboid model is self-contained).
- MPI (any compatible distribution; sweeps run each simulation on
  `mpirun -n 1`).
- The CellML inputs (motor-unit firing patterns and fibre distribution) are
  taken from `$OPENDIHU_HOME/examples/electrophysiology/input/`.

### Python (analysis and plotting)
The Python side uses, broadly:

- `numpy`, `scipy`, `pandas`
- `matplotlib`, `seaborn` (analysis); the paper figures use `matplotlib` only
- `torch`, `botorch`, `gpytorch` (BO; GP checkpoints in `data/bo_results/`
  are PyTorch `.pt` files)
- `jupyter` for the analysis notebooks in `da_4/new/` and `da_4/old/`

There is no top-level lock file; install whatever is needed in a virtualenv.

## 4. How to use each part

### 4.1. Build the cuboid simulator
The same code is reused under three roots
(`cuboid_muscle_with_prestretch/`, `bo_3/`, `da_4/new/cuboid_muscle_with_prestretch_4x4/`,
and every `forward_2/{4x4,8x8}/*/`). In any of these directories:

```bash
mkorn && sr             # alias from the OpenDiHu install (== scons BUILD_TYPE=release)
cd build_release
./muscle_with_prestretch ../settings_muscle_with_prestretch.py <F>
```

`<F>` is the prestretch traction force in newtons (positional argument).
Useful ranges:

- `cuboid_muscle_with_prestretch/`: F ∈ [0, ≈ 10] N (rest length L₀ = 15 cm)
- `bo_3/` and `da_4/`: F ∈ [0, 31] N (L₀ = 34.97 cm — vastus-lateralis-sized)

Outputs end up in the run directory:

- `muscle_length_prestretch.csv` — length time series during the passive phase
- `muscle_length_contraction.csv` — length time series during activation
- `out/default/` — ParaView VTK
- `logs/log.csv` — DOFs and per-stage runtimes

### 4.2. Reproduce the forward-model comparison (Section 2)
```bash
cd forward_2/analysis
python forward_model_analysis.py
```
Reads `muscle_length_prestretch.csv` and `logs/log.csv` from the four
canonical runs `{4x4,8x8} × {0N, 31N}` and writes the ROM / runtime plots
and the corresponding `.tex` tables used in Table 2 of the paper.

To regenerate the 36-force sweep that backs the archive of
`forward_2/archived_results/`, run `forward_2/run_force_sweep.sh` on the
machine that hosts the simulator (the script is set up for the
`cmcs09.mathematik.uni-stuttgart.de` cluster but the configuration block is
easy to retarget).

### 4.3. Bayesian optimisation (Section 3)
The objective is `ROM(F)` evaluated by the simulator in
`bo_3/src/muscle_with_prestretch.cpp`. A single BO step (i) calls the binary
with the next candidate `F*`, (ii) parses the produced `muscle_length_*.csv`,
(iii) updates the GP and (iv) saves the new state as
`out/bo_cuboid_gp_iter_NNNN.pt`. The full converged trace (13 evaluations)
ships in `data/bo_results/bo_cuboid.csv`; the 13 GP snapshots in
`data/bo_results/bo_cuboid_gp_iter_*.pt` can be loaded with `torch.load`
to inspect mean and variance at any iteration (this is exactly what
`plotting/plotting.py::make_bo_progression_plot` does to reproduce Figure 2).

### 4.4. Data augmentation (Section 4)
```bash
cd da_4/new
bash run_parameter_sweep_2702.sh                   # one-shot remote driver
# or, to resume an existing batch:
bash run_parameter_sweep_2702.sh parameter_sweep_DA_20260227_194745 4
```
The script enumerates the cross-product

```
Force_Target_N ∈ {0,3,6,9,12,15,18,21,24,27,30,33,36,39,42,45}    # 16 values
Aspect_Ratio_b_a ∈ {6.88, 7.95, 9.03, 10.10}                       # 4 values
Volume_cm3       ∈ {421.6, 455.9, 573.5, 691.2, 738.0}              # 5 values
Am               ∈ {410, 483, 557, 630}                             # 4 values
Rho              ∈ {10.493, 10.534, 10.575, 10.616} ×1e-4 kg/cm³    # 4 values
```
(3 840 simulations; the cleaned set in
`data/data_augmentation_results/uniform_prestretches_3764.csv` is the 3 764
runs that finished without numerical failure.) Force values are rescaled to a
common reference cross-section so that *stress* is held constant across the
sweep — see `da_4/old/calculate_new_parameters.ipynb` for the derivation and
`da_4/old/recalculate_force_with_area_correction.ipynb` for the correction
applied to earlier sweeps. The notebooks in `da_4/new/analyze_results_*.ipynb`
fit the mixed-effects model (per Equations (6)–(16) of the paper) and produce
the predictive distributions in `data/data_augmentation_results/`.

### 4.5. Paper figures
```bash
cd plotting
python plotting.py
```
Reads from `../data/` and writes
[`paper_figures/`](plotting/paper_figures/):

- `bo_progression.{pdf,png}` — Figure 2: GP posterior at initial / midpoint /
  final BO iterations.
- `augmentation_density_ridgeline*.{pdf,png}` and
  `augmentation_density_xy*.{pdf,png}` — Figure 3: ROM densities from the DA
  posterior at 100 / 500 / 3 764 training samples.
- `bo_augmentation_overlay*.{pdf,png}` — Figure 4: BO point-estimates overlaid
  on DA-conditional ROM densities at the prestretches BO actually queried.

The `_with_underlay` variants add a light grey scatter of every DA sample
behind the densities.

## 5. Coordinates between code and paper

| Paper item | Where in this repo |
|---|---|
| Figure 1 (workflow diagram) | LaTeX figure only |
| Table 1 (mesh DOFs)         | hard-coded in the paper; numbers come from `forward_2/analysis/complete_results.{csv,tex}` |
| Table 2 (Δz and runtime)    | `forward_2/analysis/{rom_data,runtime_data}.{csv,tex}` |
| Table 3 (DA parameter sweep)| `da_4/new/run_parameter_sweep_2702.sh` header + `da_4/old/calculate_new_parameters.ipynb` |
| §2 reduced cuboid model     | `cuboid_muscle_with_prestretch/`, `forward_2/4x4/`, `forward_2/8x8/` |
| §2 full AMI model           | `forward_2/ami/` |
| §3 BO algorithm             | `bo_3/` (simulator) + `data/bo_results/` (results) |
| §4 mixed-effects DA model   | `da_4/new/` (sweep + notebooks); `data/data_augmentation_results/` (posterior samples) |
| Figure 2                    | `plotting/plotting.py::make_bo_progression_plot` |
| Figure 3                    | `plotting/plotting.py::make_augmentation_density_{ridgeline,xy}_plot` |
| Figure 4                    | `plotting/plotting.py::make_bo_augmentation_overlay_plot` |

## 6. Notes and caveats

- The Sections-3 and -4 results in the paper use the **reduced 4 × 4 × 10**
  cuboid simulator with `L₀ = 34.97 cm` and the Heidlauf 2016 Mooney-Rivlin
  parameters; both are baked into `variables.py` under `bo_3/` and
  `da_4/new/cuboid_muscle_with_prestretch_4x4/`. The legacy
  `cuboid_muscle_with_prestretch/` uses a smaller 15 cm muscle and is kept
  because it is the cleanest single-purpose example of the simulator.
- The sweep drivers in `da_4/new/` and `forward_2/` were authored to run on
  the `cmcs09.mathematik.uni-stuttgart.de` cluster; the absolute paths in the
  header blocks and in `forward_2/analysis/forward_model_analysis.py` need to
  be retargeted for any other host.
- `forward_2/archived_results/8x8_F23N/` is missing from `8x8_F23N` because
  that single configuration failed convergence in the original sweep; the
  `.csv` aggregations correctly skip it.
- The "old vs new" split inside `da_4/` reflects an in-paper revision: the
  earlier sweep applied the prestretch force absolutely (no cross-sectional
  rescaling), which conflated force with stress when the muscle aspect ratio
  changed. The corrected sweep lives in `da_4/new/`. Only the corrected data
  feeds into the paper figures.
