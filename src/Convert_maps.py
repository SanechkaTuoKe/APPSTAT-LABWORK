import pickle
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("LSWMD_meta.csv")
maps = pickle.load(open("LSWMD_wafermaps.pkl", "rb"))

i = 0
m = maps[i]
print(df.iloc[i])
print(m.shape)

plt.imshow(m)
plt.title(df.loc[i, "failureType"])
plt.show()