"""Data ingestion and transformation pipeline."""

import argparse
from io import BytesIO
from pathlib import Path

import boto3
import pandas as pd


def _parse_s3_path(s3_uri: str) -> tuple[str, str]:
    """Return (bucket, key) from s3://bucket/key."""
    if not s3_uri.startswith("s3://"):
        raise ValueError(f"Expected S3 URI s3://bucket/key, got {s3_uri!r}")
    path = s3_uri.removeprefix("s3://").split("/", 1)
    bucket, key = path[0], path[1] if len(path) > 1 else ""
    return bucket, key


def ingest_raw_csv(source: str, raw_path: str | Path) -> None:
    """Download/read CSV and upload to raw layer on S3 using boto3.
    
    Args:
        source: Data source (URL, local path, or S3 path).
        raw_path: S3 output path for raw CSV (s3://bucket/key).
    """
    df = pd.read_csv(source)
    raw_path_str = str(raw_path)
    bucket, key = _parse_s3_path(raw_path_str)

    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket, Key=key, Body=buffer.getvalue())
    print(f"[raw] saved -> {raw_path_str} rows={len(df)} cols={len(df.columns)}")


def build_curated_parquet(raw_path: str | Path, curated_path: str | Path) -> None:
    """Read raw CSV from S3, transform to Parquet and upload to curated layer on S3.
    
    Args:
        raw_path: S3 path to raw CSV file (s3://bucket/key).
        curated_path: S3 output path for curated Parquet (s3://bucket/key).
    """
    raw_path_str = str(raw_path)
    bucket, key = _parse_s3_path(raw_path_str)

    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=bucket, Key=key)
    body = response["Body"].read()
    df = pd.read_csv(BytesIO(body))

    curated_path_str = str(curated_path)
    out_bucket, out_key = _parse_s3_path(curated_path_str)
    buffer = BytesIO()
    df.to_parquet(buffer, index=False, engine="pyarrow")
    buffer.seek(0)
    s3.put_object(Bucket=out_bucket, Key=out_key, Body=buffer.getvalue())
    print(f"[curated] saved -> {curated_path_str} rows={len(df)} cols={len(df.columns)}")


def main():
    """Main entry point. Parses arguments and runs the pipeline."""
    parser = argparse.ArgumentParser(description="Ingest raw CSV and build curated Parquet")
    parser.add_argument("--source", required=True, help="CSV source: https://... or local")
    parser.add_argument("--raw-out", default="data/raw/dataset.csv", help="S3 path for raw CSV (s3://bucket/key)")
    parser.add_argument("--curated-out", default="data/curated/dataset.parquet", help="S3 path for curated Parquet (s3://bucket/key)")
    
    args = parser.parse_args()
    
    raw_out = args.raw_out
    curated_out = args.curated_out
    
    # Pipeline: ingest raw -> build curated
    ingest_raw_csv(args.source, raw_out)
    build_curated_parquet(raw_out, curated_out)


if __name__ == "__main__":
    main()


