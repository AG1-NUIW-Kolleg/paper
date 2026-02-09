#!/usr/bin/env python3
"""
Analyze summary statistics for DA_4 parameter sweep results
Focus on range of motion, elongation, and length changes
"""

import pandas as pd
import numpy as np

# Load CSV
df = pd.read_csv('/Users/canis/Library/CloudStorage/OneDrive-Persönlich/work/SdV/natwissKolleg/results/final_results/results_for_paper/da_4/only_summary/all_results_summary_new2.csv')

print('=' * 80)
print('SUMMARY STATISTICS - DATA AUGMENTATION RESULTS')
print('=' * 80)
print()

# Total count
print(f'Total number of simulations: {len(df)}')
print()

print('=' * 80)
print('ELONGATION STATISTICS (Range of Motion)')
print('=' * 80)
print()

# Elongation Statistics
print('Elongation [cm]:')
print(f'  Min:    {df["Elongation_cm"].min():.6f} cm')
print(f'  Max:    {df["Elongation_cm"].max():.6f} cm')
print(f'  Mean:   {df["Elongation_cm"].mean():.6f} cm')
print(f'  Median: {df["Elongation_cm"].median():.6f} cm')
print(f'  Std:    {df["Elongation_cm"].std():.6f} cm')
print()

# Strain Statistics
print('Strain [-]:')
print(f'  Min:    {df["Strain"].min():.6f}')
print(f'  Max:    {df["Strain"].max():.6f}')
print(f'  Mean:   {df["Strain"].mean():.6f}')
print(f'  Median: {df["Strain"].median():.6f}')
print(f'  Std:    {df["Strain"].std():.6f}')
print()

print('=' * 80)
print('LENGTH CHANGE STATISTICS')
print('=' * 80)
print()

# Initial vs Final Length
print('Initial Length [cm]:')
print(f'  Min:    {df["Initial_Length_cm"].min():.6f} cm')
print(f'  Max:    {df["Initial_Length_cm"].max():.6f} cm')
print(f'  Mean:   {df["Initial_Length_cm"].mean():.6f} cm')
print()

print('Final Length [cm]:')
print(f'  Min:    {df["Final_Length_cm"].min():.6f} cm')
print(f'  Max:    {df["Final_Length_cm"].max():.6f} cm')
print(f'  Mean:   {df["Final_Length_cm"].mean():.6f} cm')
print()

# Absolute length change
absolute_change = df['Final_Length_cm'] - df['Initial_Length_cm']
print('Absolute Length Change [cm]:')
print(f'  Range:  {absolute_change.min():.6f} to {absolute_change.max():.6f} cm')
print(f'  Mean:   {absolute_change.mean():.6f} cm')
print()

print('=' * 80)
print('STATISTICS BY FORCE TARGET')
print('=' * 80)
print()

# Group by Force Target
force_groups = df.groupby('Force_Target_N')
print('Force_Target_N | Count | Mean_Elongation | Std_Elongation | Mean_Strain | Std_Strain')
print('-' * 80)
for force, group in force_groups:
    print(f'{force:14.0f} | {len(group):5d} | {group["Elongation_cm"].mean():15.6f} | {group["Elongation_cm"].std():14.6f} | {group["Strain"].mean():11.6f} | {group["Strain"].std():10.6f}')
print()

print('=' * 80)
print('STATISTICS BY ASPECT RATIO')
print('=' * 80)
print()

# Group by Aspect Ratio
ratio_groups = df.groupby('Aspect_Ratio_a_b')
print('Aspect_Ratio | Count | Mean_Elongation | Std_Elongation | Mean_Strain | Std_Strain')
print('-' * 80)
for ratio, group in ratio_groups:
    print(f'{ratio:12.4f} | {len(group):5d} | {group["Elongation_cm"].mean():15.6f} | {group["Elongation_cm"].std():14.6f} | {group["Strain"].mean():11.6f} | {group["Strain"].std():10.6f}')
print()

print('=' * 80)
print('STATISTICS BY VOLUME')
print('=' * 80)
print()

# Group by Volume
volume_groups = df.groupby('Volume_cm3')
print('Volume [cm³] | Count | Mean_Elongation | Std_Elongation | Mean_Strain | Std_Strain')
print('-' * 80)
for volume, group in volume_groups:
    print(f'{volume:12.1f} | {len(group):5d} | {group["Elongation_cm"].mean():15.6f} | {group["Elongation_cm"].std():14.6f} | {group["Strain"].mean():11.6f} | {group["Strain"].std():10.6f}')
print()

print('=' * 80)
print('STATISTICS BY Am VALUE')
print('=' * 80)
print()

# Group by Am
am_groups = df.groupby('Am')
print('Am [cm⁻¹] | Count | Mean_Elongation | Std_Elongation | Mean_Strain | Std_Strain')
print('-' * 80)
for am, group in am_groups:
    print(f'{am:9.0f} | {len(group):5d} | {group["Elongation_cm"].mean():15.6f} | {group["Elongation_cm"].std():14.6f} | {group["Strain"].mean():11.6f} | {group["Strain"].std():10.6f}')
print()

print('=' * 80)
print('STATISTICS BY Rho VALUE')
print('=' * 80)
print()

# Group by Rho
rho_groups = df.groupby('Rho')
print('Rho [1e-4 kg/cm³] | Count | Mean_Elongation | Std_Elongation | Mean_Strain | Std_Strain')
print('-' * 80)
for rho, group in rho_groups:
    print(f'{rho:17.3f} | {len(group):5d} | {group["Elongation_cm"].mean():15.6f} | {group["Elongation_cm"].std():14.6f} | {group["Strain"].mean():11.6f} | {group["Strain"].std():10.6f}')
print()

print('=' * 80)
print('PERCENTILES FOR ELONGATION')
print('=' * 80)
print()

percentiles = [0, 10, 25, 50, 75, 90, 95, 99, 100]
for p in percentiles:
    value = np.percentile(df['Elongation_cm'], p)
    print(f'{p:3.0f}th percentile: {value:.6f} cm')
print()

print('=' * 80)
print('CORRELATIONS')
print('=' * 80)
print()

# Correlation analysis
print('Correlation of Elongation with:')
print(f'  Force_Target_N:    {df["Elongation_cm"].corr(df["Force_Target_N"]):.4f}')
print(f'  Force_Actual_N:    {df["Elongation_cm"].corr(df["Force_Actual_N"]):.4f}')
print(f'  Aspect_Ratio_a_b:  {df["Elongation_cm"].corr(df["Aspect_Ratio_a_b"]):.4f}')
print(f'  Volume_cm3:        {df["Elongation_cm"].corr(df["Volume_cm3"]):.4f}')
print(f'  Am:                {df["Elongation_cm"].corr(df["Am"]):.4f}')
print(f'  Rho:               {df["Elongation_cm"].corr(df["Rho"]):.4f}')
print()

print('Correlation of Strain with:')
print(f'  Force_Target_N:    {df["Strain"].corr(df["Force_Target_N"]):.4f}')
print(f'  Force_Actual_N:    {df["Strain"].corr(df["Force_Actual_N"]):.4f}')
print(f'  Aspect_Ratio_a_b:  {df["Strain"].corr(df["Aspect_Ratio_a_b"]):.4f}')
print(f'  Volume_cm3:        {df["Strain"].corr(df["Volume_cm3"]):.4f}')
print(f'  Am:                {df["Strain"].corr(df["Am"]):.4f}')
print(f'  Rho:               {df["Strain"].corr(df["Rho"]):.4f}')
print()

print('=' * 80)
print('END OF ANALYSIS')
print('=' * 80)
