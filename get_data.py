import pandas as pd

url = "https://raw.githubusercontent.com/atifrizwan91/Synthetic-Dataset/refs/heads/main/synthetic-dataset.csv"
df = pd.read_csv(url)
print(df.head())