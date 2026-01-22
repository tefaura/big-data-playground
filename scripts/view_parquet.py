from pathlib import Path
import pandas as pd

# Configure pandas to display all columns
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Path to the parquet file
parquet_file = Path("data/curated/synthetic-dataset.parquet")

# Read the parquet file
df = pd.read_parquet(parquet_file)

print("Dataset shape (rows, columns):", df.shape)
print("\nFirst 5 rows (all columns):")
print(df.head())
print("\nNumber of missing values per column:")
print(df.isna().sum())
print("\nTotal rows in dataset:", len(df))
print("\nColumn names:")
print(df.columns.tolist())

