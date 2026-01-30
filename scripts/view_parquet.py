"""Parquet file viewer and inspector."""

import argparse
from pathlib import Path
import pandas as pd


def view_parquet(parquet_path: Path, num_rows: int = 5) -> None:
    """Display information about a Parquet file.
    
    Args:
        parquet_path: Path to the Parquet file.
        num_rows: Number of rows to display (default: 5).
    """
    # Configure pandas to display all columns
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    # Read the parquet file
    df = pd.read_parquet(parquet_path)

    print(f"Dataset: {parquet_path}")
    print(f"Shape (rows, columns): {df.shape}")
    print(f"\nFirst {num_rows} rows (all columns):")
    print(df.head(num_rows))
    print("\nNumber of missing values per column:")
    print(df.isna().sum())
    print(f"\nTotal rows in dataset: {len(df)}")
    print("\nColumn names:")
    print(df.columns.tolist())


def main():
    """Main entry point. Parses arguments and displays Parquet file info."""
    parser = argparse.ArgumentParser(description="View and inspect a Parquet file")
    parser.add_argument("parquet_file", help="Path to the Parquet file to view")
    parser.add_argument("--rows", type=int, default=5, help="Number of rows to display (default: 5)")
    
    args = parser.parse_args()
    
    parquet_path = Path(args.parquet_file)
    
    if not parquet_path.exists():
        print(f"Error: File not found: {parquet_path}")
        return
    
    view_parquet(parquet_path, args.rows)


if __name__ == "__main__":
    main()

