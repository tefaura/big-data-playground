"""Data ingestion and transformation pipeline."""

import argparse
from pathlib import Path
import pandas as pd


def ingest_raw_csv(source: str, raw_path: Path) -> None:
    """Download/read CSV and save to raw layer unchanged.
    
    Args:
        source: Data source (URL, local path, or S3 path).
        raw_path: Output path for raw CSV file.
    """
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    
    df = pd.read_csv(source)
    df.to_csv(raw_path, index=False)
    
    print(f"[raw] saved -> {raw_path} rows={len(df)} cols={len(df.columns)}")


def build_curated_parquet(raw_path: Path, curated_path: Path) -> None:
    """Transform raw CSV to Parquet and save to curated layer.
    
    Args:
        raw_path: Path to raw CSV file.
        curated_path: Output path for curated Parquet file.
    """
    curated_path.parent.mkdir(parents=True, exist_ok=True)
    
    df = pd.read_csv(raw_path)
    df.to_parquet(curated_path, index=False, engine="pyarrow")
    
    print(f"[curated] saved -> {curated_path} rows={len(df)} cols={len(df.columns)}")


def main():
    """Main entry point. Parses arguments and runs the pipeline."""
    parser = argparse.ArgumentParser(description="Ingest raw CSV and build curated Parquet")
    parser.add_argument("--source", required=True, help="CSV source: https://... or local")
    parser.add_argument("--raw-out", default="data/raw/dataset.csv", help="Where to store raw CSV")
    parser.add_argument("--curated-out", default="data/curated/dataset.parquet", help="Where to store curated Parquet")
    
    args = parser.parse_args()
    
    raw_out = Path(args.raw_out)
    curated_out = Path(args.curated_out)
    
    # Pipeline: ingest raw -> build curated
    ingest_raw_csv(args.source, raw_out)
    build_curated_parquet(raw_out, curated_out)


if __name__ == "__main__":
    main()


