"""
Shark Attack Dataset — Exploratory Data Analysis
Covers all analyses requested in report.md
"""

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats

warnings.filterwarnings("ignore")

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "preprocessed.csv")
PLOTS = os.path.join(BASE, "plots")
os.makedirs(PLOTS, exist_ok=True)

# ── Style ──────────────────────────────────────────────────────────────────────
plt.rcParams.update(
    {
        "figure.dpi": 150,
        "figure.facecolor": "white",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.size": 11,
    }
)
PALETTE = sns.color_palette("tab10")

# ── Helpers ────────────────────────────────────────────────────────────────────

def save(name: str, tight: bool = True) -> None:
    if tight:
        plt.tight_layout()
    path = os.path.join(PLOTS, f"{name}.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  saved → plots/{name}.png")


def section(title: str) -> None:
    bar = "=" * 60
    print(f"\n{bar}\n  {title}\n{bar}")


# ══════════════════════════════════════════════════════════════════════════════
# 1. Load & lightweight prep
# ══════════════════════════════════════════════════════════════════════════════
section("Loading data")
df = pd.read_csv(DATA, low_memory=False)
print(f"Shape: {df.shape}")

# Parse time → hour
def parse_hour(t):
    try:
        s = str(t).strip().upper()
        if s in ("?", "NAN", "NOT STATED", "UNKNOWN", ""):
            return np.nan
        # "0830hrs" / "0830h" / "08:30"
        s = s.replace("HRS", "").replace("H", "").replace(":", "").strip()
        if s.isdigit() and len(s) in (3, 4):
            return int(s) // 100
    except Exception:
        pass
    return np.nan

df["hour"] = df["time"].apply(parse_hour)

# Parse month from date
df["date_dt"] = pd.to_datetime(df["date"], errors="coerce")
df["month"] = df["date_dt"].dt.month
df["season"] = df["month"].map(
    {12: "Winter", 1: "Winter", 2: "Winter",
     3: "Spring", 4: "Spring", 5: "Spring",
     6: "Summer", 7: "Summer", 8: "Summer",
     9: "Fall",   10: "Fall", 11: "Fall"}
)

# Re-slice after derived columns are added
df_mf = df[df["sex"].isin(["M", "F"])].copy()
df_yn = df[df["fatal_y_n"].isin(["Y", "N"])].copy()
df_mf_yn = df_mf[df_mf["fatal_y_n"].isin(["Y", "N"])].copy()

# ══════════════════════════════════════════════════════════════════════════════
# 2. UNIVARIATE — Basic counts
# ══════════════════════════════════════════════════════════════════════════════
section("Univariate — sex, type, fatal, age, country, year")

# 2.1 Sex distribution
fig, ax = plt.subplots(figsize=(5, 4))
counts = df_mf["sex"].value_counts()
bars = ax.bar(["Male", "Female"], [counts["M"], counts["F"]], color=PALETTE[:2], width=0.5)
ax.bar_label(bars, fmt="%d")
ax.set_title("Reported attacks by sex")
ax.set_ylabel("Count")
save("01_sex_distribution")

# 2.2 Attack type distribution
fig, ax = plt.subplots(figsize=(7, 4))
tc = df["type"].value_counts()
bars = ax.barh(tc.index, tc.values, color=PALETTE)
ax.bar_label(bars, fmt="%d", padding=3)
ax.set_title("Attack type distribution")
ax.set_xlabel("Count")
save("02_type_distribution")

# 2.3 Fatality distribution
fig, ax = plt.subplots(figsize=(5, 4))
fc = df["fatal_y_n"].value_counts()
ax.pie(fc.values, labels=fc.index, autopct="%1.1f%%", colors=PALETTE[:3], startangle=90)
ax.set_title("Fatality outcome distribution")
save("03_fatal_distribution")

# 2.4 Age distribution
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(df["age"].dropna(), bins=30, color=PALETTE[0], edgecolor="white")
ax.set_title("Age distribution of victims")
ax.set_xlabel("Age")
ax.set_ylabel("Count")
ax.axvline(df["age"].median(), color="red", linestyle="--", label=f"Median {df['age'].median():.0f}")
ax.legend()
save("04_age_distribution")

# 2.5 Top 10 ages
fig, ax = plt.subplots(figsize=(8, 4))
top_ages = df["age"].value_counts().head(10)
bars = ax.bar(top_ages.index.astype(int), top_ages.values, color=PALETTE[1])
ax.bar_label(bars, fmt="%d")
ax.set_title("Top 10 most frequently reported victim ages")
ax.set_xlabel("Age")
ax.set_ylabel("Count")
save("05_top10_ages")

# 2.6 Top 15 countries by reported cases
fig, ax = plt.subplots(figsize=(9, 5))
cc = df["country"].value_counts().head(15)
bars = ax.barh(cc.index[::-1], cc.values[::-1], color=PALETTE[2])
ax.bar_label(bars, fmt="%d", padding=3)
ax.set_title("Top 15 countries — total reported cases")
ax.set_xlabel("Count")
save("06_top15_countries_cases")

# 2.7 Top 15 countries — invalid attacks
fig, ax = plt.subplots(figsize=(9, 5))
inv = df[df["type"] == "invalid"]["country"].value_counts().head(15)
bars = ax.barh(inv.index[::-1], inv.values[::-1], color=PALETTE[3])
ax.bar_label(bars, fmt="%d", padding=3)
ax.set_title("Top 15 countries — invalid attacks")
ax.set_xlabel("Count")
save("07_top15_countries_invalid")

# 2.8 Reports per year (post-1900)
fig, ax = plt.subplots(figsize=(12, 4))
yr = df[df["year"] >= 1900]["year"].value_counts().sort_index()
ax.plot(yr.index, yr.values, color=PALETTE[0], linewidth=1.2)
ax.fill_between(yr.index, yr.values, alpha=0.2, color=PALETTE[0])
ax.set_title("Reported shark attacks per year (1900–2026)")
ax.set_xlabel("Year")
ax.set_ylabel("Count")
save("08_reports_per_year")

# 2.9 Most frequent reported hour
fig, ax = plt.subplots(figsize=(9, 4))
hc = df["hour"].dropna().value_counts().sort_index()
ax.bar(hc.index, hc.values, color=PALETTE[4])
ax.set_title("Attack frequency by hour of day")
ax.set_xlabel("Hour (24 h)")
ax.set_ylabel("Count")
ax.set_xticks(range(0, 25))
save("09_attacks_by_hour")

# ══════════════════════════════════════════════════════════════════════════════
# 3. BIVARIATE — Categorical vs Categorical
# ══════════════════════════════════════════════════════════════════════════════
section("Bivariate — categorical × categorical")

# 3.1 Sex vs Fatal — stacked bar
fig, ax = plt.subplots(figsize=(6, 4))
ct = pd.crosstab(df_mf_yn["sex"], df_mf_yn["fatal_y_n"], normalize="index") * 100
ct = ct.rename(index={"M": "Male", "F": "Female"})
ct.plot(kind="bar", ax=ax, color=["#e74c3c", "#2ecc71"], rot=0)
ax.set_title("Fatality rate by sex (% within sex)")
ax.set_ylabel("% of cases")
ax.legend(title="Fatal", labels=["Fatal (Y)", "Non-fatal (N)"])
save("10_sex_vs_fatal")

print("\n[3.1] Fatality rate by sex:")
raw = pd.crosstab(df_mf_yn["sex"], df_mf_yn["fatal_y_n"])
raw.index = ["Female", "Male"]
raw["fatal_%"] = (raw["Y"] / (raw["Y"] + raw["N"]) * 100).round(1)
print(raw)

# 3.2 Type vs Fatal — heatmap
fig, ax = plt.subplots(figsize=(7, 4))
ct2 = pd.crosstab(df_yn["type"], df_yn["fatal_y_n"], normalize="index") * 100
sns.heatmap(ct2, annot=True, fmt=".1f", cmap="YlOrRd", ax=ax, linewidths=0.5)
ax.set_title("Fatality rate % by attack type")
ax.set_xlabel("Fatal")
ax.set_ylabel("Type")
save("11_type_vs_fatal_heatmap")

print("\n[3.2] Fatality % by type:")
print(ct2.round(1))

# 3.3 Type vs Sex — stacked bar
fig, ax = plt.subplots(figsize=(8, 4))
ct3 = pd.crosstab(df_mf["type"], df_mf["sex"], normalize="index") * 100
ct3.rename(columns={"M": "Male", "F": "Female"}, inplace=True)
ct3.plot(kind="bar", ax=ax, rot=30, color=PALETTE[:2])
ax.set_title("Sex distribution within each attack type (%)")
ax.set_ylabel("% within type")
ax.legend(title="Sex")
save("12_type_vs_sex")

# 3.4 Who provokes more — sex vs provoked
fig, ax = plt.subplots(figsize=(5, 4))
prov = df_mf[df_mf["type"] == "provoked"]["sex"].value_counts()
total = df_mf["sex"].value_counts()
prov_rate = (prov / total * 100).rename(index={"M": "Male", "F": "Female"})
bars = ax.bar(prov_rate.index, prov_rate.values, color=PALETTE[:2], width=0.5)
ax.bar_label(bars, fmt="%.1f%%")
ax.set_title("Provoked attack rate by sex (% within sex)")
ax.set_ylabel("% of cases that were provoked")
save("13_provoked_by_sex")

print("\n[3.4] Provoked attack rate by sex:")
print(prov_rate.round(2))

# 3.5 Provoked vs Fatal
fig, ax = plt.subplots(figsize=(7, 4))
ct5 = pd.crosstab(df_yn["type"], df_yn["fatal_y_n"])
ct5_pct = ct5.div(ct5.sum(axis=1), axis=0) * 100
ct5_pct.plot(kind="bar", ax=ax, rot=30, color=["#e74c3c", "#2ecc71"])
ax.set_title("Fatality split by attack type")
ax.set_ylabel("% of cases")
ax.legend(title="Fatal")
save("14_type_fatal_stacked")

# 3.6 Type vs Country (top 5 countries, top 3 types)
top5c = df["country"].value_counts().head(5).index
top3t = ["unprovoked", "provoked", "invalid"]
sub = df[df["country"].isin(top5c) & df["type"].isin(top3t)]
fig, ax = plt.subplots(figsize=(9, 5))
ct6 = pd.crosstab(sub["country"], sub["type"])
ct6.plot(kind="bar", ax=ax, rot=30, color=PALETTE[:3])
ax.set_title("Attack type distribution — top 5 countries")
ax.set_ylabel("Count")
ax.legend(title="Type")
save("15_type_vs_country")

# ══════════════════════════════════════════════════════════════════════════════
# 4. BIVARIATE — Categorical vs Numerical (Age)
# ══════════════════════════════════════════════════════════════════════════════
section("Bivariate — age × categorical")

# 4.1 Age by fatality
fig, ax = plt.subplots(figsize=(7, 4))
for label, grp in df_yn.groupby("fatal_y_n"):
    ax.hist(grp["age"].dropna(), bins=25, alpha=0.55, label=label, density=True)
ax.set_title("Age distribution by fatality outcome")
ax.set_xlabel("Age")
ax.set_ylabel("Density")
ax.legend(title="Fatal")
save("16_age_by_fatal")

print("\n[4.1] Mean age by fatality:")
print(df_yn.groupby("fatal_y_n")["age"].agg(["mean", "median", "count"]).round(1))

# 4.2 Children vs Adults fatality
df_yn["age_group"] = pd.cut(df_yn["age"], bins=[0, 17, 64, 200],
                             labels=["Child (0-17)", "Adult (18-64)", "Senior (65+)"])
ct7 = pd.crosstab(df_yn["age_group"], df_yn["fatal_y_n"], normalize="index") * 100
fig, ax = plt.subplots(figsize=(7, 4))
ct7.plot(kind="bar", ax=ax, rot=0, color=["#e74c3c", "#2ecc71"])
ax.set_title("Fatality rate by age group (%)")
ax.set_ylabel("% within age group")
ax.legend(title="Fatal")
save("17_agegroup_vs_fatal")

print("\n[4.2] Fatality rate by age group:")
print(ct7.round(1))

# 4.3 Age distribution by sex
fig, ax = plt.subplots(figsize=(7, 4))
for label, grp in df_mf.groupby("sex"):
    ax.hist(grp["age"].dropna(), bins=25, alpha=0.55,
            label="Male" if label == "M" else "Female", density=True)
ax.set_title("Age distribution by sex")
ax.set_xlabel("Age")
ax.set_ylabel("Density")
ax.legend()
save("18_age_by_sex")

# 4.4 Age boxplot by type
fig, ax = plt.subplots(figsize=(8, 4))
order = df["type"].value_counts().index.tolist()
df.boxplot(column="age", by="type", ax=ax, showfliers=False,
           vert=True, patch_artist=True)
plt.suptitle("")
ax.set_title("Age distribution by attack type")
ax.set_xlabel("Type")
ax.set_ylabel("Age")
plt.xticks(rotation=30)
save("19_age_by_type")

# 4.5 Age by sex — violin
fig, ax = plt.subplots(figsize=(6, 5))
data_v = [df_mf[df_mf["sex"] == s]["age"].dropna().values for s in ["M", "F"]]
parts = ax.violinplot(data_v, positions=[1, 2], showmedians=True)
for i, pc in enumerate(parts["bodies"]):
    pc.set_facecolor(PALETTE[i])
    pc.set_alpha(0.7)
ax.set_xticks([1, 2])
ax.set_xticklabels(["Male", "Female"])
ax.set_title("Age distribution by sex (violin)")
ax.set_ylabel("Age")
save("20_age_sex_violin")

# ══════════════════════════════════════════════════════════════════════════════
# 5. SEASON / MONTH / TIME ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
section("Temporal — season, month, year")

# 5.1 Monthly case count
fig, ax = plt.subplots(figsize=(9, 4))
mc = df.groupby("month").size().reindex(range(1, 13), fill_value=0)
month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
ax.bar(mc.index, mc.values, color=PALETTE[5])
ax.set_xticks(range(1, 13))
ax.set_xticklabels(month_names)
ax.set_title("Shark attacks by month")
ax.set_ylabel("Count")
save("21_attacks_by_month")

# 5.2 Monthly fatality rate
fig, ax = plt.subplots(figsize=(9, 4))
m_fatal = df_yn[df_yn["fatal_y_n"] == "Y"].groupby("month").size()
m_total = df_yn.groupby("month").size()
m_rate = (m_fatal / m_total * 100).reindex(range(1, 13), fill_value=np.nan)
ax.plot(m_rate.index, m_rate.values, marker="o", color=PALETTE[3])
ax.set_xticks(range(1, 13))
ax.set_xticklabels(month_names)
ax.set_title("Fatality rate by month (%)")
ax.set_ylabel("Fatal %")
save("22_fatal_rate_by_month")

# 5.3 Season — cases and fatality rate
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
season_order = ["Spring", "Summer", "Fall", "Winter"]
sc = df.groupby("season").size().reindex(season_order)
axes[0].bar(sc.index, sc.values, color=PALETTE[6])
axes[0].set_title("Cases by season")
axes[0].set_ylabel("Count")

sf = df_yn[df_yn["fatal_y_n"] == "Y"].groupby("season").size()
st = df_yn.groupby("season").size()
sr = (sf / st * 100).reindex(season_order)
axes[1].bar(sr.index, sr.values, color=PALETTE[7])
axes[1].set_title("Fatality rate by season (%)")
axes[1].set_ylabel("Fatal %")
save("23_season_analysis")

print("\n[5.3] Season — cases & fatality rate:")
s_df = pd.DataFrame({"Cases": sc, "Fatal_rate_%": sr.round(1)})
print(s_df)

# ══════════════════════════════════════════════════════════════════════════════
# 6. TIME SERIES — Yearly trends, rolling averages, anomaly detection
# ══════════════════════════════════════════════════════════════════════════════
section("Time series — yearly trends")

df_ts = df[(df["year"] >= 1900) & (df["year"] <= 2025)].copy()

# 6.1 Yearly trend by type with rolling average
fig, ax = plt.subplots(figsize=(13, 5))
main_types = ["unprovoked", "provoked", "watercraft", "sea disaster"]
for t, col in zip(main_types, PALETTE[:4]):
    yr_t = df_ts[df_ts["type"] == t].groupby("year").size()
    yr_t = yr_t.reindex(range(1900, 2026), fill_value=0)
    roll = yr_t.rolling(10, center=True).mean()
    ax.plot(yr_t.index, yr_t.values, alpha=0.25, color=col)
    ax.plot(roll.index, roll.values, color=col, linewidth=2, label=t)
ax.set_title("Yearly attacks by type — 10-year rolling mean")
ax.set_xlabel("Year")
ax.set_ylabel("Count")
ax.legend()
save("24_yearly_trend_by_type")

# 6.2 Total cases rolling + anomaly detection
yr_all = df_ts.groupby("year").size().reindex(range(1900, 2026), fill_value=0)
roll5 = yr_all.rolling(5, center=True).mean()
std5 = yr_all.rolling(5, center=True).std()
upper = roll5 + 2 * std5
lower = (roll5 - 2 * std5).clip(lower=0)
anomalies = yr_all[(yr_all > upper) | (yr_all < lower)]

fig, ax = plt.subplots(figsize=(13, 5))
ax.plot(yr_all.index, yr_all.values, alpha=0.4, color=PALETTE[0], label="Annual count")
ax.plot(roll5.index, roll5.values, color=PALETTE[0], linewidth=2, label="5-yr rolling mean")
ax.fill_between(roll5.index, lower, upper, alpha=0.15, color=PALETTE[0], label="±2σ band")
ax.scatter(anomalies.index, anomalies.values, color="red", zorder=5, label="Anomaly (±2σ)")
ax.set_title("Total shark attacks per year — anomaly detection")
ax.set_xlabel("Year")
ax.set_ylabel("Count")
ax.legend()
save("25_anomaly_detection")

print("\n[6.2] Anomaly years:")
print(anomalies.to_frame("count"))

# 6.3 Yearly trend — top 5 countries
fig, ax = plt.subplots(figsize=(13, 5))
top5 = df_ts["country"].value_counts().head(5).index
for country, col in zip(top5, PALETTE[:5]):
    yr_c = df_ts[df_ts["country"] == country].groupby("year").size()
    yr_c = yr_c.reindex(range(1900, 2026), fill_value=0).rolling(10, center=True).mean()
    ax.plot(yr_c.index, yr_c.values, color=col, linewidth=1.8, label=country)
ax.set_title("10-yr rolling mean — top 5 countries")
ax.set_xlabel("Year")
ax.set_ylabel("Count")
ax.legend()
save("26_yearly_trend_by_country")

# 6.4 Fatality rate per year — rolling
yr_fatal = df_ts[df_ts["fatal_y_n"] == "Y"].groupby("year").size().reindex(range(1900, 2026), fill_value=0)
yr_total_yn = df_ts[df_ts["fatal_y_n"].isin(["Y", "N"])].groupby("year").size().reindex(range(1900, 2026), fill_value=0)
fatal_rate = (yr_fatal / yr_total_yn.replace(0, np.nan) * 100)
roll_fr = fatal_rate.rolling(10, center=True).mean()

fig, ax = plt.subplots(figsize=(13, 4))
ax.plot(fatal_rate.index, fatal_rate.values, alpha=0.3, color=PALETTE[3])
ax.plot(roll_fr.index, roll_fr.values, color=PALETTE[3], linewidth=2, label="10-yr rolling fatality %")
ax.set_title("Fatality rate over time (%) — 10-yr rolling mean")
ax.set_xlabel("Year")
ax.set_ylabel("Fatal %")
ax.legend()
save("27_fatality_rate_over_time")

# ══════════════════════════════════════════════════════════════════════════════
# 7. MULTIVARIATE / CORRELATION
# ══════════════════════════════════════════════════════════════════════════════
section("Multivariate — correlation matrix & pairplot")

# 7.1 Correlation matrix — numeric + encoded categoricals
df_corr = df.copy()
df_corr["fatal_bin"] = (df_corr["fatal_y_n"] == "Y").astype(float)
df_corr["sex_bin"] = (df_corr["sex"] == "M").astype(float)
df_corr["provoked_bin"] = (df_corr["type"] == "provoked").astype(float)
df_corr["unprovoked_bin"] = (df_corr["type"] == "unprovoked").astype(float)

numeric_cols = ["year", "age", "lat", "lon", "hour",
                "fatal_bin", "sex_bin", "provoked_bin", "unprovoked_bin", "month"]
corr_mat = df_corr[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8))
mask = np.triu(np.ones_like(corr_mat, dtype=bool))
sns.heatmap(corr_mat, annot=True, fmt=".2f", cmap="coolwarm", center=0,
            mask=mask, ax=ax, linewidths=0.5, vmin=-1, vmax=1)
ax.set_title("Correlation matrix — key numeric & encoded variables")
save("28_correlation_matrix")

print("\n[7.1] Correlation with fatality (binary):")
print(corr_mat["fatal_bin"].drop("fatal_bin").sort_values(key=abs, ascending=False).round(3))

# 7.2 Pairplot (small subset)
pp_cols = ["age", "year", "lat", "lon", "fatal_bin", "sex_bin"]
pp_df = df_corr[pp_cols].dropna()
fig = sns.pairplot(pp_df, hue="fatal_bin", vars=["age", "year", "lat", "lon"],
                   palette={0.0: PALETTE[2], 1.0: PALETTE[3]},
                   plot_kws={"alpha": 0.3, "s": 10})
fig.figure.suptitle("Pairplot: age, year, lat, lon (red = fatal)", y=1.01)
fig.figure.savefig(os.path.join(PLOTS, "29_pairplot.png"), bbox_inches="tight", dpi=150)
plt.close("all")
print("  saved → plots/29_pairplot.png")

# ══════════════════════════════════════════════════════════════════════════════
# 8. GEOGRAPHIC — coordinates vs fatality
# ══════════════════════════════════════════════════════════════════════════════
section("Geographic — coordinates vs fatality")

# 8.1 World scatter: fatal vs non-fatal
geo = df_yn.dropna(subset=["lat", "lon"])
fig, ax = plt.subplots(figsize=(14, 7))
nf = geo[geo["fatal_y_n"] == "N"]
fa = geo[geo["fatal_y_n"] == "Y"]
ax.scatter(nf["lon"], nf["lat"], s=6, alpha=0.3, color=PALETTE[2], label="Non-fatal")
ax.scatter(fa["lon"], fa["lat"], s=8, alpha=0.5, color=PALETTE[3], label="Fatal")
ax.set_title("World map of shark attacks (geo-tagged cases)")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.legend(markerscale=2)
ax.axhline(0, color="grey", linewidth=0.5, linestyle="--")
save("30_geo_fatal_map")

# 8.2 Hemisphere / region fatality rate
geo2 = geo.copy()
geo2["hemisphere"] = geo2["lat"].apply(lambda x: "Northern" if x >= 0 else "Southern")
geo2["ocean_zone"] = geo2["lon"].apply(
    lambda x: "Atlantic" if -80 <= x <= 20
    else ("Pacific" if (x > 140 or x < -60) else "Indian/Other")
)
ct_h = pd.crosstab(geo2["hemisphere"], geo2["fatal_y_n"], normalize="index") * 100
ct_o = pd.crosstab(geo2["ocean_zone"], geo2["fatal_y_n"], normalize="index") * 100

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
ct_h.plot(kind="bar", ax=axes[0], rot=0, color=["#e74c3c", "#2ecc71"])
axes[0].set_title("Fatality rate by hemisphere (%)")
axes[0].set_ylabel("%")
axes[0].legend(title="Fatal")
ct_o.plot(kind="bar", ax=axes[1], rot=15, color=["#e74c3c", "#2ecc71"])
axes[1].set_title("Fatality rate by ocean zone (%)")
axes[1].set_ylabel("%")
axes[1].legend(title="Fatal")
save("31_geo_hemisphere_ocean")

print("\n[8.2] Fatality rate by hemisphere:")
print(ct_h.round(1))
print("\nFatality rate by ocean zone:")
print(ct_o.round(1))

# ══════════════════════════════════════════════════════════════════════════════
# 9. SPECIES — top species by count & fatality
# ══════════════════════════════════════════════════════════════════════════════
section("Species — counts & fatality")

# Clean up species: take first 35 chars, lowercase, strip; group small ones
df["species_clean"] = (
    df["species"]
    .fillna("Unknown")
    .str.lower()
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

# Top species mentions
species_kw = {
    "White shark": r"white shark|great white",
    "Tiger shark": r"tiger shark",
    "Bull shark": r"bull shark",
    "Reef shark": r"reef shark",
    "Nurse shark": r"nurse shark",
    "Hammerhead": r"hammerhead",
    "Lemon shark": r"lemon shark",
    "Mako shark": r"mako",
    "Unknown": r"^unknown$|not identified|not confirmed|not determined",
}
for name, pat in species_kw.items():
    df.loc[df["species_clean"].str.contains(pat, na=False), "species_group"] = name
df["species_group"] = df["species_group"].fillna("Other/unspecified")

fig, ax = plt.subplots(figsize=(10, 5))
sp_c = df["species_group"].value_counts()
bars = ax.barh(sp_c.index[::-1], sp_c.values[::-1], color=PALETTE[:len(sp_c)])
ax.bar_label(bars, fmt="%d", padding=3)
ax.set_title("Cases by identified species group")
ax.set_xlabel("Count")
save("32_species_count")

# Fatality rate by species
df_sp_yn = df[df["fatal_y_n"].isin(["Y", "N"])]
ct_sp = pd.crosstab(df_sp_yn["species_group"], df_sp_yn["fatal_y_n"], normalize="index") * 100
fig, ax = plt.subplots(figsize=(10, 5))
ct_sp_sorted = ct_sp.sort_values("Y", ascending=True)
ct_sp_sorted.plot(kind="barh", ax=ax, color=["#e74c3c", "#2ecc71"])
ax.set_title("Fatality rate by species group (%)")
ax.set_xlabel("% within species")
ax.legend(title="Fatal")
save("33_species_fatality")

print("\n[9] Fatality rate by species group:")
print(ct_sp.round(1))

# ══════════════════════════════════════════════════════════════════════════════
# 10. ACTIVITY — top activities, fatality by activity
# ══════════════════════════════════════════════════════════════════════════════
section("Activity — counts & fatality")

df["activity_clean"] = df["activity"].str.lower().str.strip()

# Group activities
act_map = {
    "Swimming": r"swim",
    "Surfing": r"surf",
    "Diving": r"div|scuba|snorkel",
    "Fishing": r"fish|spearfish",
    "Wading/Standing": r"wad|stand",
    "Kayaking/Canoeing": r"kayak|canoe|paddle",
    "Bathing": r"bath",
    "Boating": r"boat|rowing",
}
df["activity_group"] = "Other"
for label, pat in act_map.items():
    df.loc[df["activity_clean"].str.contains(pat, na=False, regex=True), "activity_group"] = label

fig, ax = plt.subplots(figsize=(10, 5))
ac = df["activity_group"].value_counts()
bars = ax.barh(ac.index[::-1], ac.values[::-1], color=PALETTE[:len(ac)])
ax.bar_label(bars, fmt="%d", padding=3)
ax.set_title("Cases by activity group")
ax.set_xlabel("Count")
save("34_activity_count")

df_act_yn = df[df["fatal_y_n"].isin(["Y", "N"])]
ct_act = pd.crosstab(df_act_yn["activity_group"], df_act_yn["fatal_y_n"], normalize="index") * 100
fig, ax = plt.subplots(figsize=(10, 5))
ct_act_sorted = ct_act.sort_values("Y", ascending=True)
ct_act_sorted.plot(kind="barh", ax=ax, color=["#e74c3c", "#2ecc71"])
ax.set_title("Fatality rate by activity (%)")
ax.set_xlabel("% within activity")
ax.legend(title="Fatal")
save("35_activity_fatality")

print("\n[10] Fatality rate by activity:")
print(ct_act.round(1))

# ══════════════════════════════════════════════════════════════════════════════
# 11. SUMMARY STATISTICS
# ══════════════════════════════════════════════════════════════════════════════
section("Summary statistics")

total = len(df)
fatal_n = (df["fatal_y_n"] == "Y").sum()
fatal_pct = fatal_n / len(df_yn) * 100

print(f"\nTotal records:              {total:,}")
print(f"Fatal cases (Y):            {fatal_n:,}  ({fatal_pct:.1f}% of known outcomes)")
print(f"Male victims:               {(df['sex']=='M').sum():,}")
print(f"Female victims:             {(df['sex']=='F').sum():,}")
print(f"Median victim age:          {df['age'].median():.0f}")
print(f"Most common attack type:    {df['type'].mode()[0]}")
print(f"Top country:                {df['country'].value_counts().index[0]}")
print(f"Peak year (post-1900):      {yr_all.idxmax()} ({yr_all.max()} cases)")
print(f"\nAll plots saved to: {PLOTS}/")
print(f"Total plots generated:       35")
