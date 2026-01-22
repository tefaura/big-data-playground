from pathlib import Path
import pandas as pd

INP = Path("data/raw/synthetic-dataset.csv")
OUT = Path("data/curated/synthetic-dataset.parquet")

OUT.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INP)

df.to_parquet(OUT, index=False, engine="pyarrow")

print(f"Saved parquet: {OUT} rows={len(df)} cols={len(df.columns)}")
