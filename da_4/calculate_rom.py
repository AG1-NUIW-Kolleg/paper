#!/usr/bin/env python3
"""
Script to calculate Range of Motion (ROM) from existing muscle_length_contraction.csv files
in the archived_results directory.

ROM is calculated as: ROM = z_max - z_min

The script processes all subdirectories in archived_results/ and creates a range_of_motion.txt
file in each directory.
"""

from pathlib import Path
import sys


def calculate_rom_from_csv(csv_file_path):
    """
    Calculate ROM from a muscle_length_contraction.csv file.
    
    Args:
        csv_file_path: Path to the CSV file
        
    Returns:
        tuple: (z_max, z_min, rom, count) or None if file doesn't exist/is empty
    """
    csv_path = Path(csv_file_path)
    
    if not csv_path.exists():
        print(f"  ⚠️  CSV file not found: {csv_path}")
        return None
    
    try:
        with open(csv_path, 'r') as f:
            content = f.read().strip()
            
        if not content:
            print(f"  ⚠️  CSV file is empty: {csv_path}")
            return None
            
        # Parse comma-separated values
        muscle_lengths = [float(x.strip()) for x in content.split(',') if x.strip()]
        
        if not muscle_lengths:
            print(f"  ⚠️  No valid data in CSV file: {csv_path}")
            return None
        
        z_max = max(muscle_lengths)
        z_min = min(muscle_lengths)
        rom = z_max - z_min
        
        return z_max, z_min, rom, len(muscle_lengths)
        
    except Exception as e:
        print(f"  ❌ Error reading {csv_path}: {e}")
        return None


def process_directory(sim_dir):
    """
    Process a single simulation directory.
    
    Args:
        sim_dir: Path to the simulation directory
        
    Returns:
        bool: True if successful, False otherwise
    """
    sim_path = Path(sim_dir)
    csv_file = sim_path / "muscle_length_contraction.csv"
    output_file = sim_path / "range_of_motion.txt"
    
    print(f"\n📁 Processing: {sim_path.name}")
    
    # Calculate ROM from CSV
    result = calculate_rom_from_csv(csv_file)
    
    if result is None:
        return False
    
    z_max, z_min, rom, count = result
    
    # Write results to file
    try:
        with open(output_file, 'w') as f:
            f.write(f"Range of Motion Analysis\n")
            f.write(f"=" * 50 + "\n\n")
            f.write(f"Source: muscle_length_contraction.csv\n")
            f.write(f"Number of timesteps: {count}\n\n")
            f.write(f"Maximum muscle length (z_max): {z_max:.8f} cm\n")
            f.write(f"Minimum muscle length (z_min): {z_min:.8f} cm\n")
            f.write(f"Range of Motion (ROM):          {rom:.8f} cm\n")
        
        print(f"  ✅ ROM = {rom:.8f} cm (z_max: {z_max:.8f}, z_min: {z_min:.8f})")
        print(f"  📝 Results written to: {output_file.name}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error writing output file: {e}")
        return False


def main():
    """Main function to process all directories in archived_results."""
    
    # Base directory
    base_dir = Path(__file__).parent / "archived_results"
    
    if not base_dir.exists():
        print(f"❌ Error: archived_results directory not found at {base_dir}")
        sys.exit(1)
    
    print("=" * 70)
    print("ROM Calculation for Data Augmentation Results")
    print("=" * 70)
    print(f"\nBase directory: {base_dir}")
    
    # Get all subdirectories
    subdirs = sorted([d for d in base_dir.iterdir() if d.is_dir()])
    
    if not subdirs:
        print(f"\n❌ No subdirectories found in {base_dir}")
        sys.exit(1)
    
    print(f"\nFound {len(subdirs)} simulation directories")
    
    # Process each directory
    success_count = 0
    failure_count = 0
    
    for sim_dir in subdirs:
        if process_directory(sim_dir):
            success_count += 1
        else:
            failure_count += 1
    
    # Print summary
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"Total directories processed: {len(subdirs)}")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {failure_count}")
    print("=" * 70)
    
    if failure_count > 0:
        print("\n⚠️  Some directories failed. Check the output above for details.")
        sys.exit(1)
    else:
        print("\n✅ All directories processed successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
