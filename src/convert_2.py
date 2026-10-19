import pandas as pd
df = pd.read_csv("LSWMD_meta.csv")
labeled = df.dropna(subset=["failureType"])
print(labeled["failureType"].value_counts())