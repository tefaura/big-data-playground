import pandas as pd

# Configure pandas to display all columns
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

url = "https://raw.githubusercontent.com/nbchambers95/data-science-projects/refs/heads/main/milkshake-forecasting/Weather%20Data.csv"
df = pd.read_csv(url)

print("Dataset shape (rows, columns):", df.shape)
print("\nFirst 5 rows (all columns):")
print(df.head())
print("\nNumber of missing values per column:")
print(df.isna().sum())
print("\nTotal rows in dataset:", len(df))