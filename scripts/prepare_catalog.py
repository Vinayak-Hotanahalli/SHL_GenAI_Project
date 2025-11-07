import pandas as pd

df = pd.read_csv("data/shl_catalog_raw.csv")
df.drop_duplicates(subset=["name"], inplace=True)
df["description"] = df["description"].fillna("")

def infer_type(desc):
    text = desc.lower()
    if "personality" in text or "behaviour" in text:
        return "P"
    elif "technical" in text or "skills" in text:
        return "K"
    else:
        return "U"

df["test_type"] = df["description"].apply(infer_type)
df.to_csv("data/shl_catalog_clean.csv", index=False)
print("Saved data/shl_catalog_clean.csv")
