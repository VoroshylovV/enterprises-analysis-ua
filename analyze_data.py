import textwrap
import pandas as pd
import matplotlib.pyplot as plt

# Стиль
plt.style.use("default")
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["axes.labelsize"] = 11
plt.rcParams["xtick.labelsize"] = 10
plt.rcParams["ytick.labelsize"] = 10
plt.rcParams["legend.fontsize"] = 10

# 1. Завантаження очищених даних
df = pd.read_csv("data_processed/enterprises_clean.csv", encoding="utf-8-sig")

# 2. Беремо останній доступний рік
last_year = df["year"].max()
df_last = df[df["year"] == last_year].copy()

# Допоміжна функція для переносу довгих підписів
def wrap_labels(labels, width=35):
    return [textwrap.fill(str(label), width=width) for label in labels]


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
plot_data = top_regions.head(10).sort_values()
bars = plt.barh(plot_data.index, plot_data.values, color="#4c78a8")
plt.xlabel("Кількість активних підприємств")
plt.ylabel("Область")
plt.title(f"Топ-10 областей за кількістю активних підприємств, {last_year}")
plt.grid(axis="x", linestyle="--", alpha=0.35)

for bar, value in zip(bars, plot_data.values):
    plt.text(value + 1500, bar.get_y() + bar.get_height() / 2,
             f"{value:,.0f}".replace(",", " "), va="center", fontsize=9)

plt.tight_layout()
plt.savefig("data_processed/top_regions.png", bbox_inches="tight")
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

plt.figure(figsize=(12, 8))
plot_data = top_activities.head(10).sort_values()
labels = wrap_labels(plot_data.index, width=38)

bars = plt.barh(labels, plot_data.values, color="#f28e2b")
plt.xlabel("Кількість активних підприємств")
plt.ylabel("Галузь")
plt.title(f"Топ-10 галузей за кількістю активних підприємств, {last_year}")
plt.grid(axis="x", linestyle="--", alpha=0.35)

for bar, value in zip(bars, plot_data.values):
    plt.text(value + 1500, bar.get_y() + bar.get_height() / 2,
             f"{value:,.0f}".replace(",", " "), va="center", fontsize=9)

plt.tight_layout()
plt.savefig("data_processed/activities.png", bbox_inches="tight")
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

fig, ax = plt.subplots(figsize=(10, 6))
sex_by_region_sorted = sex_by_region.sort_values(by="Жінки")

sex_by_region_sorted[["Жінки", "Чоловіки"]].plot(
    kind="barh",
    stacked=True,
    color=["#d95f8d", "#4c78a8"],
    ax=ax
)

ax.set_xlabel("Кількість активних підприємств")
ax.set_ylabel("Область")
ax.set_title(f"Розподіл за статтю керівника у топ-10 областях, {last_year}")
ax.grid(axis="x", linestyle="--", alpha=0.35)

legend = ax.get_legend()
legend.set_title("Стать керівника")

plt.tight_layout()
plt.savefig("data_processed/sex_by_region.png", bbox_inches="tight")
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
bars = plt.barh(plot_df["region"], plot_df["women_share"] * 100, color="#d95f8d")
plt.xlabel("Частка жінок-керівниць, %")
plt.ylabel("Область")
plt.title(f"Топ-10 областей за часткою жінок-керівниць, {last_year}")
plt.grid(axis="x", linestyle="--", alpha=0.35)

for bar, value in zip(bars, plot_df["women_share"] * 100):
    plt.text(value + 0.4, bar.get_y() + bar.get_height() / 2,
             f"{value:.1f}%", va="center", fontsize=9)

plt.tight_layout()
plt.savefig("data_processed/women_share_top_regions.png", bbox_inches="tight")
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

plt.figure(figsize=(12, 8))
plot_df = women_share_by_activity.head(10).sort_values(by="women_share")
labels = wrap_labels(plot_df["activity"], width=38)
bars = plt.barh(labels, plot_df["women_share"] * 100, color="#d95f8d")
plt.xlabel("Частка жінок-керівниць, %")
plt.ylabel("Галузь")
plt.title(f"Топ-10 галузей за часткою жінок-керівниць, {last_year}")
plt.grid(axis="x", linestyle="--", alpha=0.35)

for bar, value in zip(bars, plot_df["women_share"] * 100):
    plt.text(value + 0.4, bar.get_y() + bar.get_height() / 2,
             f"{value:.1f}%", va="center", fontsize=9)

plt.tight_layout()
plt.savefig("data_processed/women_share_top_activities.png", bbox_inches="tight")
plt.close()


plt.figure(figsize=(12, 8))
plot_df = women_share_by_activity.tail(10).sort_values(by="women_share")
labels = wrap_labels(plot_df["activity"], width=38)
bars = plt.barh(labels, plot_df["women_share"] * 100, color="#4c78a8")
plt.xlabel("Частка жінок-керівниць, %")
plt.ylabel("Галузь")
plt.title(f"Топ-10 галузей з найнижчою часткою жінок-керівниць, {last_year}")
plt.grid(axis="x", linestyle="--", alpha=0.35)

for bar, value in zip(bars, plot_df["women_share"] * 100):
    plt.text(value + 0.4, bar.get_y() + bar.get_height() / 2,
             f"{value:.1f}%", va="center", fontsize=9)

plt.tight_layout()
plt.savefig("data_processed/women_share_bottom_activities.png", bbox_inches="tight")
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

plt.figure(figsize=(12, 8))
plot_df = women_share_by_activity.sort_values(by="gap_from_overall")
labels = wrap_labels(plot_df["activity"], width=38)
colors = ["#4c78a8" if x < 0 else "#d95f8d" for x in plot_df["gap_from_overall"]]
bars = plt.barh(labels, plot_df["gap_from_overall"] * 100, color=colors)
plt.xlabel("Відхилення від середньої частки жінок, в.п.")
plt.ylabel("Галузь")
plt.title(f"Відхилення частки жінок-керівниць від загального середнього, {last_year}")
plt.grid(axis="x", linestyle="--", alpha=0.35)

for bar, value in zip(bars, plot_df["gap_from_overall"] * 100):
    shift = 0.25 if value >= 0 else -1.2
    plt.text(value + shift, bar.get_y() + bar.get_height() / 2,
             f"{value:.1f}", va="center", fontsize=9)

plt.tight_layout()
plt.savefig("data_processed/gender_gap_activities.png", bbox_inches="tight")
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
