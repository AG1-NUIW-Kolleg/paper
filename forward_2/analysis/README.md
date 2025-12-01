# Forward Model Analysis - Chapter 2

## Overview

This directory contains the analysis scripts and results for the forward model mesh resolution comparison study (Chapter 2 of the paper).

## Study Design

### Experimental Setup

- **Mesh Resolutions**: 4x4 vs 8x8
- **Prestretch Forces**: 0N and 31N
- **Parameters** (from `documentation.txt`):
  - muscle_extent_y: 34.97 cm (average men VL)
  - Volume: 691.2 cm³ (average men VL)
  - muscle_extent_x (calculated): 4.45 cm
  - Am: 500 cm⁻¹
  - Rho: 10.616 [1e-4 kg/cm³]
  - End time: 100 ms

### Research Questions

1. **ROM Correlation**: How well do the ROM values correlate between 4x4 and 8x8 mesh resolutions?
2. **Runtime Reduction**: What is the computational cost reduction when using 4x4 vs 8x8 mesh?
3. **Accuracy vs Efficiency**: Does the reduced mesh resolution maintain sufficient accuracy while improving efficiency?

## File Structure

```
analysis/
├── README.md                          # This file
├── forward_model_analysis.py          # Main analysis script
├── analysis_summary.txt               # Generated summary report
├── analysis_results.json              # Machine-readable results
├── rom_data.csv                       # ROM data table
├── rom_data.tex                       # LaTeX table for ROM data
├── runtime_data.csv                   # Runtime data table
├── runtime_data.tex                   # LaTeX table for runtime data
├── complete_results.csv               # All results combined
├── complete_results.tex               # LaTeX table for all results
├── rom_correlation_4x4_vs_8x8.png     # ROM correlation plot (PNG)
├── rom_correlation_4x4_vs_8x8.pdf     # ROM correlation plot (PDF)
├── rom_comparison_bar.png             # ROM comparison bar chart (PNG)
├── rom_comparison_bar.pdf             # ROM comparison bar chart (PDF)
├── runtime_comparison.png             # Runtime comparison (PNG)
├── runtime_comparison.pdf             # Runtime comparison (PDF)
├── elongation_strain_comparison.png   # Elongation/strain comparison (PNG)
└── elongation_strain_comparison.pdf   # Elongation/strain comparison (PDF)
```

## Usage

### Running the Analysis

```bash
# Navigate to the analysis directory
cd forward_2/analysis

# Activate virtual environment (if needed)
source ../../.venv/bin/activate

# Run the analysis
python forward_model_analysis.py
```

### Dependencies

```bash
pip install pandas numpy matplotlib seaborn scipy
```

## Results

### Key Findings

The analysis computes:

1. **ROM Correlation**: R² value showing correlation between 4x4 and 8x8 mesh resolutions
2. **Runtime Reduction**: Percentage reduction in computational time
3. **Elongation and Strain**: Detailed mechanical response metrics

### Output Files

- **Plots**: High-resolution PNG (300 dpi) and PDF versions for publication
- **Tables**: CSV for data analysis and LaTeX for direct inclusion in paper
- **JSON**: Structured results for integration with other tools
- **Summary**: Human-readable text report with key findings

### Suggested Text for Paper

The script automatically generates suggested text for the paper manuscript, filling in the TODO placeholders:

```
Analysis of the achieved muscle ROM reveals a high correlation of ROM for both
mesh resolutions (R² > [COMPUTED VALUE]) in single-point comparison of different
prestretches (0N and 31N), confirming that variations in ROM arise purely from
discretization-dependent mechanical response rather than inconsistent geometric
deformation. Regarding the runtime, the reduced mesh resolution results in a
reduction of runtime by [COMPUTED]% ([COMPUTED] min vs [COMPUTED] min).
Therefore, the single-muscle cuboid model with reduced spatial resolution serves
as a complexity reduced model, that retains similar accuracy in ROM-values and is
thereby used for further algorithmic implementations in Section~\ref{sec:bayesian_optimization}
and~\ref{sec:data_augmentation}.
```

## Data Sources

The analysis reads data from:

- `../4x4/4x4_0N/build_release_4x4_0N/`
  - `muscle_length_prestretch.csv`: Muscle length data
  - `logs/log.csv`: Runtime and performance metrics

- `../4x4/4x4_31N/build_release/`
  - `muscle_length_prestretch.csv`: Muscle length data
  - `logs/log.csv`: Runtime and performance metrics

- `../8x8/8x8_0N/build_release/`
  - `muscle_length_prestretch.csv`: Muscle length data
  - `logs/log.csv`: Runtime and performance metrics

- `../8x8/8x8_31N/build_release/`
  - `muscle_length_prestretch.csv`: Muscle length data
  - `logs/log.csv`: Runtime and performance metrics

## Analysis Methodology

### ROM Correlation Analysis

- Extracts final muscle length (ROM) for each configuration
- Computes Pearson correlation coefficient and R² between 4x4 and 8x8
- Performs linear regression to assess relationship
- Statistical significance testing (p-value)

### Runtime Analysis

- Extracts total simulation runtime from log files
- Computes average runtime for each mesh resolution
- Calculates percentage reduction and speedup factor
- Compares individual experiments and averages

### Mechanical Response

- Computes elongation (final - initial length)
- Calculates strain (elongation / initial length)
- Compares mechanical response across configurations

## Visualization

All plots include:
- High-quality figures (300 dpi for PNG)
- Publication-ready formatting
- Clear labels and legends
- Statistical annotations (R², p-values)
- Error bars where applicable

## Integration with Paper

### LaTeX Tables

The generated `.tex` files can be directly included in your LaTeX manuscript:

```latex
\begin{table}[h]
\centering
\input{analysis/rom_data.tex}
\caption{Range of motion comparison between 4x4 and 8x8 mesh resolutions.}
\label{tab:rom_comparison}
\end{table}
```

### Figures

```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{analysis/rom_correlation_4x4_vs_8x8.pdf}
\caption{ROM correlation between 4x4 and 8x8 mesh resolutions showing high agreement (R² > [VALUE]).}
\label{fig:rom_correlation}
\end{figure}
```

## Notes

- All analyses are fully automated and reproducible
- Results are generated from raw simulation data
- Statistical tests ensure reliability of findings
- Visualization follows publication standards

## Contact

For questions or issues with the analysis, refer to the main project documentation or contact the project maintainers.

---

**Last Updated**: 2025-12-01  
**Analysis Version**: 1.0
