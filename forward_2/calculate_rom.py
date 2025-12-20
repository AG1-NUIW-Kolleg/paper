#!/usr/bin/env python3
"""
Calculate Range of Motion (ROM) from muscle_length_contraction.csv files
ROM = z_max - z_min (maximum - minimum muscle length during simulation)
"""

import os
import csv
import numpy as np
from pathlib import Path

def calculate_rom_from_csv(csv_file_path):
    """
    Read muscle lengths from CSV and calculate ROM
    
    Args:
        csv_file_path: Path to muscle_length_contraction.csv file
        
    Returns:
        tuple: (z_max, z_min, rom, num_values)
    """
    if not os.path.exists(csv_file_path):
        print(f"  ❌ File not found: {csv_file_path}")
        return None
    
    try:
        # Read CSV file (values are comma-separated in a single row)
        with open(csv_file_path, 'r') as f:
            content = f.read().strip()
            
        # Split by comma and convert to float, filtering out empty strings
        values = [float(x) for x in content.split(',') if x.strip()]
        
        if len(values) == 0:
            print(f"  ❌ No values found in {csv_file_path}")
            return None
        
        # Calculate ROM
        z_max = max(values)
        z_min = min(values)
        rom = z_max - z_min
        
        return z_max, z_min, rom, len(values)
        
    except Exception as e:
        print(f"  ❌ Error reading {csv_file_path}: {e}")
        return None


def process_directory(base_dir, output_file="range_of_motion.txt"):
    """
    Process a simulation directory and calculate ROM
    
    Args:
        base_dir: Base directory containing build_release folder
        output_file: Name of the output file
    """
    csv_path = os.path.join(base_dir, "build_release", "muscle_length_contraction.csv")
    output_path = os.path.join(base_dir, "build_release", output_file)
    
    print(f"\n📁 Processing: {base_dir}")
    print(f"  Reading: {csv_path}")
    
    result = calculate_rom_from_csv(csv_path)
    
    if result is None:
        return False
    
    z_max, z_min, rom, num_values = result
    
    # Write results to file
    with open(output_path, 'w') as f:
        f.write(f"z_max: {z_max}\n")
        f.write(f"z_min: {z_min}\n")
        f.write(f"ROM: {rom}\n")
        f.write(f"num_timesteps: {num_values}\n")
    
    print(f"  ✅ Results written to: {output_path}")
    print(f"     z_max (maximum muscle length): {z_max:.8f} cm")
    print(f"     z_min (minimum muscle length): {z_min:.8f} cm")
    print(f"     ROM (z_max - z_min):           {rom:.8f} cm")
    print(f"     Number of timesteps:           {num_values}")
    
    return True


def main():
    """Main function to process all simulation directories"""
    
    # Base path
    script_dir = Path(__file__).parent
    
    # Define all directories to process
    directories = [
        script_dir / "4x4" / "4x4_0N",
        script_dir / "4x4" / "4x4_31N",
        script_dir / "8x8" / "8x8_0N",
        script_dir / "8x8" / "8x8_31N",
    ]
    
    print("=" * 80)
    print("Range of Motion (ROM) Calculation")
    print("=" * 80)
    print("\nFormula: ROM = z_max - z_min")
    print("  z_max = maximum muscle length during simulation")
    print("  z_min = minimum muscle length during simulation")
    
    success_count = 0
    failed_count = 0
    
    for directory in directories:
        if process_directory(directory):
            success_count += 1
        else:
            failed_count += 1
    
    print("\n" + "=" * 80)
    print(f"Summary: {success_count} successful, {failed_count} failed")
    print("=" * 80)
    
    if success_count > 0:
        print("\n✅ ROM calculations completed!")
        print("   Results saved in each build_release/range_of_motion.txt")
    

if __name__ == "__main__":
    main()
