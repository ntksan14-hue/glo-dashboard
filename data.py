import pandas as pd
import os

FILE_PATH = "งบ68.csv"

if os.path.exists(FILE_PATH):
    df = pd.read_csv(FILE_PATH)
else:
    raise FileNotFoundError("❌ ไม่เจอไฟล์ งบ68.csv")

df['total_budget'] = df['budget(cost)'].fillna(0) + df['budget(inv)'].fillna(0)
df['ap_name_cleaned'] = df['ap_name'].str.replace(r'\s+', '', regex=True)

df_clean = df[df["sp"] == 0].copy()
df_unique = df.drop_duplicates(subset=['year','ap_name_cleaned','total_budget'])

# export
__all__ = ["df", "df_clean", "df_unique"]