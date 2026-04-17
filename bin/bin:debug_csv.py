import pandas as pd

path = "./bin/biwt_protype_rules.csv"

df = pd.read_csv(path)

print("Shape:", df.shape)
print("Columns:", df.columns)
print(df.head())