#!/usr/bin/env python3
"""
Script to compare and visualize ROM results for 4x4 vs 8x8 mesh configurations.
Analyzes whether the ROM values are proportional across different mesh sizes.
"""

import re
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


def read_rom_from_file(file_path):
    """
    Read ROM value from range_of_motion.txt file.
    
    Args:
        file_path: Path to the range_of_motion.txt file
        
    Returns:
        dict with z_max, z_min, rom values or None if file doesn't exist
    """
    if not file_path.exists():
        print(f"⚠️  File not found: {file_path}")
        return None
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extract values using regex
        z_max_match = re.search(r'Maximum muscle length \(z_max\):\s+([\d.]+)', content)
        z_min_match = re.search(r'Minimum muscle length \(z_min\):\s+([\d.]+)', content)
        rom_match = re.search(r'Range of Motion \(ROM\):\s+([\d.]+)', content)
        
        if z_max_match and z_min_match and rom_match:
            return {
                'z_max': float(z_max_match.group(1)),
                'z_min': float(z_min_match.group(1)),
                'rom': float(rom_match.group(1))
            }
        else:
            print(f"⚠️  Could not parse values from: {file_path}")
            return None
            
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return None


def main():
    """Main function to compare and plot ROM values."""
    
    # Define paths
    base_dir = Path(__file__).parent
    
    configs = {
        '4x4_0N': base_dir / '4x4' / '4x4_0N' / 'build_release' / 'range_of_motion.txt',
        '4x4_31N': base_dir / '4x4' / '4x4_31N' / 'build_release' / 'range_of_motion.txt',
        '8x8_0N': base_dir / '8x8' / '8x8_0N' / 'build_release' / 'range_of_motion.txt',
        '8x8_31N': base_dir / '8x8' / '8x8_31N' / 'build_release' / 'range_of_motion.txt',
    }
    
    print("=" * 70)
    print("ROM Comparison: 4x4 vs 8x8 Mesh")
    print("=" * 70)
    
    # Read all ROM values
    data = {}
    for name, path in configs.items():
        print(f"\nReading {name}...")
        result = read_rom_from_file(path)
        if result:
            data[name] = result
            print(f"  ROM = {result['rom']:.8f} cm")
            print(f"  z_max = {result['z_max']:.8f} cm")
            print(f"  z_min = {result['z_min']:.8f} cm")
    
    if len(data) != 4:
        print("\n❌ Error: Could not read all ROM files!")
        return
    
    # Calculate ratios
    print("\n" + "=" * 70)
    print("ROM Ratios (4x4 / 8x8)")
    print("=" * 70)
    
    ratio_0N = data['4x4_0N']['rom'] / data['8x8_0N']['rom']
    ratio_31N = data['4x4_31N']['rom'] / data['8x8_31N']['rom']
    
    print(f"\n0N Prestretch:")
    print(f"  4x4 ROM: {data['4x4_0N']['rom']:.8f} cm")
    print(f"  8x8 ROM: {data['8x8_0N']['rom']:.8f} cm")
    print(f"  Ratio (4x4/8x8): {ratio_0N:.4f}")
    
    print(f"\n31N Prestretch:")
    print(f"  4x4 ROM: {data['4x4_31N']['rom']:.8f} cm")
    print(f"  8x8 ROM: {data['8x8_31N']['rom']:.8f} cm")
    print(f"  Ratio (4x4/8x8): {ratio_31N:.4f}")
    
    print(f"\nRatio difference: {abs(ratio_0N - ratio_31N):.4f}")
    print(f"Average ratio: {(ratio_0N + ratio_31N) / 2:.4f}")
    
    # Create comprehensive visualization
    fig = plt.figure(figsize=(16, 10))
    
    # Plot 1: ROM Comparison Bar Chart
    ax1 = plt.subplot(2, 3, 1)
    x = np.arange(2)
    width = 0.35
    
    rom_4x4 = [data['4x4_0N']['rom'], data['4x4_31N']['rom']]
    rom_8x8 = [data['8x8_0N']['rom'], data['8x8_31N']['rom']]
    
    bars1 = ax1.bar(x - width/2, rom_4x4, width, label='4x4 Mesh', color='steelblue', alpha=0.8)
    bars2 = ax1.bar(x + width/2, rom_8x8, width, label='8x8 Mesh', color='coral', alpha=0.8)
    
    ax1.set_ylabel('ROM (cm)', fontsize=11, fontweight='bold')
    ax1.set_title('ROM Comparison: 4x4 vs 8x8 Mesh', fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(['0N Prestretch', '31N Prestretch'])
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom', fontsize=9)
    
    # Plot 2: Ratio Comparison
    ax2 = plt.subplot(2, 3, 2)
    ratios = [ratio_0N, ratio_31N]
    colors = ['steelblue', 'coral']
    bars = ax2.bar(['0N', '31N'], ratios, color=colors, alpha=0.8)
    ax2.axhline(y=np.mean(ratios), color='green', linestyle='--', 
                label=f'Mean: {np.mean(ratios):.3f}', linewidth=2)
    ax2.set_ylabel('Ratio (4x4/8x8)', fontsize=11, fontweight='bold')
    ax2.set_title('ROM Ratio: 4x4 / 8x8', fontsize=12, fontweight='bold')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Plot 3: Absolute ROM Values
    ax3 = plt.subplot(2, 3, 3)
    mesh_sizes = ['4x4\n0N', '4x4\n31N', '8x8\n0N', '8x8\n31N']
    rom_values = [data['4x4_0N']['rom'], data['4x4_31N']['rom'], 
                  data['8x8_0N']['rom'], data['8x8_31N']['rom']]
    colors = ['steelblue', 'steelblue', 'coral', 'coral']
    
    bars = ax3.bar(mesh_sizes, rom_values, color=colors, alpha=0.8)
    ax3.set_ylabel('ROM (cm)', fontsize=11, fontweight='bold')
    ax3.set_title('ROM for All Configurations', fontsize=12, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontsize=9)
    
    # Plot 4: z_max comparison
    ax4 = plt.subplot(2, 3, 4)
    z_max_4x4 = [data['4x4_0N']['z_max'], data['4x4_31N']['z_max']]
    z_max_8x8 = [data['8x8_0N']['z_max'], data['8x8_31N']['z_max']]
    
    x = np.arange(2)
    bars1 = ax4.bar(x - width/2, z_max_4x4, width, label='4x4 Mesh', color='steelblue', alpha=0.8)
    bars2 = ax4.bar(x + width/2, z_max_8x8, width, label='8x8 Mesh', color='coral', alpha=0.8)
    
    ax4.set_ylabel('z_max (cm)', fontsize=11, fontweight='bold')
    ax4.set_title('Maximum Muscle Length (z_max)', fontsize=12, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(['0N', '31N'])
    ax4.legend()
    ax4.grid(axis='y', alpha=0.3)
    
    # Plot 5: z_min comparison
    ax5 = plt.subplot(2, 3, 5)
    z_min_4x4 = [data['4x4_0N']['z_min'], data['4x4_31N']['z_min']]
    z_min_8x8 = [data['8x8_0N']['z_min'], data['8x8_31N']['z_min']]
    
    bars1 = ax5.bar(x - width/2, z_min_4x4, width, label='4x4 Mesh', color='steelblue', alpha=0.8)
    bars2 = ax5.bar(x + width/2, z_min_8x8, width, label='8x8 Mesh', color='coral', alpha=0.8)
    
    ax5.set_ylabel('z_min (cm)', fontsize=11, fontweight='bold')
    ax5.set_title('Minimum Muscle Length (z_min)', fontsize=12, fontweight='bold')
    ax5.set_xticks(x)
    ax5.set_xticklabels(['0N', '31N'])
    ax5.legend()
    ax5.grid(axis='y', alpha=0.3)
    
    # Plot 6: Scatter plot to check proportionality
    ax6 = plt.subplot(2, 3, 6)
    rom_4x4_all = [data['4x4_0N']['rom'], data['4x4_31N']['rom']]
    rom_8x8_all = [data['8x8_0N']['rom'], data['8x8_31N']['rom']]
    
    ax6.scatter(rom_8x8_all, rom_4x4_all, s=100, alpha=0.7, edgecolors='black', linewidth=2)
    ax6.plot([0, max(rom_8x8_all)*1.1], [0, max(rom_8x8_all)*1.1 * np.mean(ratios)], 
             'r--', label=f'y = {np.mean(ratios):.3f}x', linewidth=2)
    
    # Annotate points
    ax6.annotate('0N', (rom_8x8_all[0], rom_4x4_all[0]), 
                xytext=(5, 5), textcoords='offset points', fontsize=10, fontweight='bold')
    ax6.annotate('31N', (rom_8x8_all[1], rom_4x4_all[1]), 
                xytext=(5, 5), textcoords='offset points', fontsize=10, fontweight='bold')
    
    ax6.set_xlabel('8x8 ROM (cm)', fontsize=11, fontweight='bold')
    ax6.set_ylabel('4x4 ROM (cm)', fontsize=11, fontweight='bold')
    ax6.set_title('Proportionality Check: 4x4 vs 8x8', fontsize=12, fontweight='bold')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    output_file = base_dir / 'rom_comparison_4x4_vs_8x8.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✅ Plot saved to: {output_file}")
    
    # Show plot
    plt.show()
    
    # Print summary
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"\n📊 Key Findings:")
    print(f"  • 4x4 mesh produces {ratio_0N:.2f}x larger ROM than 8x8 mesh (0N)")
    print(f"  • 4x4 mesh produces {ratio_31N:.2f}x larger ROM than 8x8 mesh (31N)")
    print(f"  • Ratio consistency: {abs(ratio_0N - ratio_31N):.4f} (smaller = more proportional)")
    
    if abs(ratio_0N - ratio_31N) < 0.1:
        print(f"\n✅ The meshes show CONSISTENT proportionality across prestretch conditions!")
    else:
        print(f"\n⚠️  The meshes show DIFFERENT proportionality across prestretch conditions!")
    
    print(f"\n📈 ROM increases with prestretch:")
    print(f"  • 4x4: {data['4x4_0N']['rom']:.2f} → {data['4x4_31N']['rom']:.2f} cm (+{((data['4x4_31N']['rom']/data['4x4_0N']['rom']-1)*100):.1f}%)")
    print(f"  • 8x8: {data['8x8_0N']['rom']:.2f} → {data['8x8_31N']['rom']:.2f} cm (+{((data['8x8_31N']['rom']/data['8x8_0N']['rom']-1)*100):.1f}%)")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
