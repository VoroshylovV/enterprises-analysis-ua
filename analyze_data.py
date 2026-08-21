import pandas as pd
import matplotlib.pyplot as plt

# Налаштування відображення
plt.style.use("default")

# 1. Завантаження очищених даних
df = pd.read_csv("data_processed/enterprises_clean.csv", encoding="utf-8-sig")

# 2. Беремо останній доступний рік
last_year = df["year"].max()
df_last = df[df["year"] == last_year].copy()

# -----------------------------
# A. ТОП РЕГІОНИ
# -----------------------------
top_regions = (
    df_last.groupby("region")["enterprises_count"]
    .sum()
    .sort_values(ascending=False)
)

top_regions.to_csv("data_processed/top_regions.csv", encoding="utf-8-sig")

plt.figure(figsize=(10, 6))
top_regions.head(10).sort_values().plot(kind="barh", color="steelblue")
plt.xlabel("Кількість активних підприємств")
plt.ylabel("Регіон")
plt.title(f"Топ-10 регіонів за кількістю активних підприємств, {last_year}")
plt.tight_layout()
plt.savefig("data_processed/top_regions.png")
plt.close()

# -----------------------------
# B. ТОП ГАЛУЗІ
# -----------------------------
top_activities = (
    df_last.groupby("activity")["enterprises_count"]
    .sum()
    .sort_values(ascending=False)
)

top_activities.to_csv("data_processed/top_activities.csv", encoding="utf-8-sig")

plt.figure(figsize=(10, 8))
top_activities.head(10).sort_values().plot(kind="barh", color="darkorange")
plt.xlabel("Кількість активних підприємств")
plt.ylabel("Галузь")
plt.title(f"Топ-10 галузей за кількістю активних підприємств, {last_year}")
plt.tight_layout()
plt.savefig("data_processed/activities.png")
plt.close()

# -----------------------------
# C. ГЕНДЕРНИЙ РОЗПОДІЛ ПО ТОП-10 РЕГІОНАХ
# -----------------------------
top10_region_names = top_regions.head(10).index.tolist()

sex_by_region = (
    df_last[df_last["region"].isin(top10_region_names)]
    .groupby(["region", "sex"])["enterprises_count"]
    .sum()
    .unstack(fill_value=0)
)

sex_by_region = sex_by_region.loc[top10_region_names]

sex_by_region.to_csv("data_processed/sex_by_region.csv", encoding="utf-8-sig")

plt.figure(figsize=(10, 6))
sex_by_region[["Жінки", "Чоловіки"]].sort_values(by="Жінки").plot(
    kind="barh",
    stacked=True,
    color=["#d95f8d", "#4c78a8"]
)
plt.xlabel("Кількість активних підприємств")
plt.ylabel("Регіон")
plt.title(f"Розподіл за статтю керівника у топ-10 регіонах, {last_year}")
plt.tight_layout()
plt.savefig("data_processed/sex_by_region.png")
plt.close()

# -----------------------------
# D. ЧАСТКА ЖІНОК ПО РЕГІОНАХ
# -----------------------------
women_share_by_region = (
    df_last.groupby(["region", "sex"])["enterprises_count"]
    .sum()
    .unstack(fill_value=0)
    .reset_index()
)

women_share_by_region["total"] = (
    women_share_by_region["Жінки"] + women_share_by_region["Чоловіки"]
)
women_share_by_region["women_share"] = (
    women_share_by_region["Жінки"] / women_share_by_region["total"]
)

women_share_by_region = women_share_by_region.sort_values(
    by="women_share", ascending=False
)

women_share_by_region.to_csv(
    "data_processed/women_share_by_region.csv",
    index=False,
    encoding="utf-8-sig"
)

plt.figure(figsize=(10, 8))
plot_df = women_share_by_region.head(10).sort_values(by="women_share")
plt.barh(plot_df["region"], plot_df["women_share"] * 100, color="#d95f8d")
plt.xlabel("Частка жінок-керівниць, %")
plt.ylabel("Регіон")
plt.title(f"Топ-10 регіонів за часткою жінок-керівниць, {last_year}")
plt.tight_layout()
plt.savefig("data_processed/women_share_top_regions.png")
plt.close()

# -----------------------------
# E. ЧАСТКА ЖІНОК ПО ГАЛУЗЯХ
# -----------------------------
women_share_by_activity = (
    df_last.groupby(["activity", "sex"])["enterprises_count"]
    .sum()
    .unstack(fill_value=0)
    .reset_index()
)

women_share_by_activity["total"] = (
    women_share_by_activity["Жінки"] + women_share_by_activity["Чоловіки"]
)
women_share_by_activity["women_share"] = (
    women_share_by_activity["Жінки"] / women_share_by_activity["total"]
)

women_share_by_activity = women_share_by_activity.sort_values(
    by="women_share", ascending=False
)

women_share_by_activity.to_csv(
    "data_processed/women_share_by_activity.csv",
    index=False,
    encoding="utf-8-sig"
)

plt.figure(figsize=(10, 8))
plot_df = women_share_by_activity.head(10).sort_values(by="women_share")
plt.barh(plot_df["activity"], plot_df["women_share"] * 100, color="#d95f8d")
plt.xlabel("Частка жінок-керівниць, %")
plt.ylabel("Галузь")
plt.title(f"Топ-10 галузей за часткою жінок-керівниць, {last_year}")
plt.tight_layout()
plt.savefig("data_processed/women_share_top_activities.png")
plt.close()

plt.figure(figsize=(10, 8))
plot_df = women_share_by_activity.tail(10).sort_values(by="women_share")
plt.barh(plot_df["activity"], plot_df["women_share"] * 100, color="#4c78a8")
plt.xlabel("Частка жінок-керівниць, %")
plt.ylabel("Галузь")
plt.title(f"Топ-10 галузей з найнижчою часткою жінок-керівниць, {last_year}")
plt.tight_layout()
plt.savefig("data_processed/women_share_bottom_activities.png")
plt.close()

# -----------------------------
# F. ВІДХИЛЕННЯ ВІД ЗАГАЛЬНОЇ СЕРЕДНЬОЇ
# -----------------------------
overall_women = df_last[df_last["sex"] == "Жінки"]["enterprises_count"].sum()
overall_men = df_last[df_last["sex"] == "Чоловіки"]["enterprises_count"].sum()
overall_total = overall_women + overall_men
overall_women_share = overall_women / overall_total

women_share_by_activity["gap_from_overall"] = (
    women_share_by_activity["women_share"] - overall_women_share
)

women_share_by_activity.to_csv(
    "data_processed/gender_gap_by_activity.csv",
    index=False,
    encoding="utf-8-sig"
)

plt.figure(figsize=(10, 8))
plot_df = women_share_by_activity.sort_values(by="gap_from_overall")
colors = ["#4c78a8" if x < 0 else "#d95f8d" for x in plot_df["gap_from_overall"]]
plt.barh(plot_df["activity"], plot_df["gap_from_overall"] * 100, color=colors)
plt.xlabel("Відхилення від середньої частки жінок, в.п.")
plt.ylabel("Галузь")
plt.title(f"Відхилення частки жінок-керівниць від загального середнього, {last_year}")
plt.tight_layout()
plt.savefig("data_processed/gender_gap_activities.png")
plt.close()

# -----------------------------
# G. КОРОТКІ ПІДСУМКОВІ МЕТРИКИ
# -----------------------------
summary = pd.DataFrame({
    "metric": [
        "overall_women_share",
        "overall_men_share",
        "regions_count",
        "activities_count",
        "records_count"
    ],
    "value": [
        round(overall_women_share, 4),
        round(overall_men / overall_total, 4),
        df_last["region"].nunique(),
        df_last["activity"].nunique(),
        len(df_last)
    ]
})

summary.to_csv("data_processed/summary_metrics.csv", index=False, encoding="utf-8-sig")

print("Analysis completed.")
print("Overall women share:", round(overall_women_share * 100, 2), "%")

