import pandas as pd

df = pd.read_csv("data_processed/enterprises_clean.csv")

# перевір, що це справді константи на весь файл
print(df["Показник"].nunique(), df["Категорія розрізу"].nunique(),
      df["Періодичність"].nunique(), df["year"].nunique())

df_long = df.drop(columns=["Показник", "Категорія розрізу", "Періодичність", "year"])
df_long = df_long.rename(columns={
    "region": "region",
    "activity": "activity",
    "sex": "sex",
    "enterprises_count": "count"
})

df_long.to_csv("data_processed/enterprises_long.csv", index=False, encoding="utf-8-sig")
print(df_long.shape)
print(df_long.head())