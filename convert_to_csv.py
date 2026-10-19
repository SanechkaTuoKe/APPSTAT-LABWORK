import sys, pickle as pkl, gc
import numpy as np
import pandas as pd
import pandas.core.indexes

sys.modules['pandas.indexes'] = pandas.core.indexes

with open("LSWMD.pkl", "rb") as f:
    obj = pkl.load(f, encoding="latin1")

old = obj if isinstance(obj, pd.DataFrame) else pd.DataFrame(obj)
del obj

def flat(x):
    try:
        while hasattr(x, "__len__") and not isinstance(x, str) and len(x) > 0:
            x = x[0]
        return None if hasattr(x, "__len__") and not isinstance(x, str) else x
    except Exception:
        return None

cols = [c for c in old.columns if c != "waferMap"]
df = pd.DataFrame({c: old[c].tolist() for c in cols})

if "waferMap" in old.columns:
    maps = old["waferMap"].tolist()
    with open("LSWMD_wafermaps.pkl", "wb") as f:
        pkl.dump(maps, f, protocol=4)
    del maps

del old
gc.collect()

for c in ["trianTestLabel", "failureType"]:
    if c in df.columns:
        df[c] = df[c].map(flat)

df.to_csv("LSWMD_meta.csv", index=False)
print(df.shape)
print(df.head())