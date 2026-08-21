import pandas as pd

df = pd.read_csv("raw.csv", encoding="utf-8-sig")

# перевірка унікальних значень по ключових колонках
print(df["Показник"].unique())
print(df["Категорія розрізу"].unique())
print(df["Стать керівника"].unique())
print(df["Періодичність"].unique())
print(df["Період"].min(), df["Період"].max())
print(df["Значення cпостереження"].dtype)
print(df.isna().sum())
