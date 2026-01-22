from pathlib import Path
import pandas as pd

URL = "https://raw.githubusercontent.com/nbchambers95/data-science-projects/refs/heads/main/milkshake-forecasting/Weather%20Data.csv"
OUT = Path("data/raw/synthetic-dataset.csv")

OUT.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(URL)
df.to_csv(OUT, index=False)

print(f"Saved raw CSV: {OUT} rows={len(df)} cols={len(df.columns)}")
