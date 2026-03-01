#!/usr/bin/env python3
"""
generate_report.py — Shark Attack Interactive Portfolio Report
Run from the project directory: python generate_report.py
Output: index.html  (self-contained via Plotly CDN)
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# ─── 1. Load & prep ──────────────────────────────────────────────────────────
df = pd.read_csv("preprocessed.csv", index_col=0, low_memory=False)

df["year"]       = pd.to_numeric(df["year"],  errors="coerce")
df["age"]        = pd.to_numeric(df["age"],   errors="coerce")
df["normalized"] = pd.to_datetime(df["normalized"], errors="coerce")

VALID_TYPES   = ["unprovoked", "provoked", "watercraft", "sea disaster", "invalid"]
VALID_SEX     = ["M", "F", "O"]
VALID_FATAL   = ["Y", "N", "Unknown"]

df["type"]      = df["type"].str.lower().str.strip().fillna("invalid")
df["sex"]       = df["sex"].fillna("O").str.strip()
df["fatal_y_n"] = df["fatal_y_n"].fillna("Unknown").str.strip()

df.loc[~df["type"].isin(VALID_TYPES),  "type"]      = "invalid"
df.loc[~df["sex"].isin(VALID_SEX),     "sex"]       = "O"
df.loc[~df["fatal_y_n"].isin(VALID_FATAL), "fatal_y_n"] = "Unknown"

modern = df[(df["year"] >= 1900) & (df["year"] <= 2026)].copy()
modern["month"]  = modern["normalized"].dt.month
modern["decade"] = (modern["year"] // 10 * 10).astype("Int64")

# ─── 2. Colour palette ───────────────────────────────────────────────────────
BG    = "#070f1f"
CARD  = "#0d1f3c"
PAPER = "#0d1f3c"

OUTCOME_COLORS = {"Y": "#ef5350", "N": "#26a69a", "Unknown": "#546e7a"}
SEX_COLORS     = {"M": "#42a5f5", "F": "#ec407a", "O": "#78909c"}

_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor=PAPER,
    plot_bgcolor=PAPER,
    font=dict(family="Inter, system-ui, sans-serif", color="#c8d8f0", size=13),
    margin=dict(l=20, r=20, t=52, b=20),
    autosize=True,
)
PLOTLY_CFG = dict(responsive=True, displayModeBar=True, displaylogo=False)


def L(**kw):
    """Merge extra layout keys on top of the defaults."""
    return {**_LAYOUT, **kw}


def fig_html(fig):
    return pio.to_html(fig, full_html=False, include_plotlyjs=False, config=PLOTLY_CFG)


# ─── 3. Charts ───────────────────────────────────────────────────────────────

# ── 3.1  Incidents per year ──────────────────────────────────────────────────
yearly = (
    modern.groupby("year").size()
    .reset_index(name="incidents").sort_values("year")
)
yearly["roll10"] = yearly["incidents"].rolling(10, center=True, min_periods=5).mean()

c1 = go.Figure()
c1.add_trace(go.Scatter(
    x=yearly["year"], y=yearly["incidents"],
    mode="lines", name="Annual count",
    line=dict(color="#42a5f5", width=1.5), opacity=0.55,
    fill="tozeroy", fillcolor="rgba(66,165,245,0.07)",
    hovertemplate="<b>%{x}</b>  —  %{y} incidents<extra></extra>",
))
c1.add_trace(go.Scatter(
    x=yearly["year"], y=yearly["roll10"],
    mode="lines", name="10-yr rolling avg",
    line=dict(color="#64ffda", width=2.5),
    hovertemplate="<b>%{x}</b>  —  avg %.1f<extra></extra>",
))
c1.update_layout(**L(
    title_text="Shark Incidents per Year, 1900–2026",
    xaxis_title="Year", yaxis_title="Incidents",
    hovermode="x unified", height=380,
    legend=dict(x=0.02, y=0.97, bgcolor="rgba(0,0,0,0.4)"),
))

# ── 3.2  World choropleth ────────────────────────────────────────────────────
country_cnt = (
    modern[modern["country"].notna() & ~modern["country"].isin(["Unknown", ""])]
    .groupby("country").size().reset_index(name="incidents")
)
c2 = px.choropleth(
    country_cnt, locations="country", locationmode="country names",
    color="incidents", hover_name="country",
    color_continuous_scale=[[0, "#091c36"], [0.25, "#1565c0"],
                             [0.6, "#0288d1"], [1, "#00e5ff"]],
    title="Incidents by Country (1900–2026)",
)
c2.update_geos(
    bgcolor=BG, showcoastlines=True, coastlinecolor="#1e3a5f",
    showland=True, landcolor="#111f35",
    showocean=True, oceancolor="#050d18",
    showlakes=False, projection_type="natural earth",
)
c2.update_layout(**L(
    height=480,
    geo=dict(bgcolor=BG),
    coloraxis_colorbar=dict(title="Incidents", thicknessmode="pixels", thickness=14),
))

# ── 3.3  Top 15 countries ────────────────────────────────────────────────────
top15 = country_cnt.nlargest(15, "incidents").sort_values("incidents")
c3 = go.Figure(go.Bar(
    x=top15["incidents"], y=top15["country"],
    orientation="h",
    marker=dict(color=top15["incidents"],
                colorscale=[[0, "#0d3b5e"], [1, "#00e5ff"]]),
    text=top15["incidents"], textposition="outside",
    hovertemplate="<b>%{y}</b><br>%{x:,} incidents<extra></extra>",
))
c3.update_layout(**L(
    title_text="Top 15 Countries by Incidents",
    xaxis_title="Incidents", yaxis_title="",
    height=460, showlegend=False,
    margin=dict(l=130, r=60, t=52, b=20),
))

# ── 3.4  Gender × outcome stacked bar ────────────────────────────────────────
sex_out = (
    modern[modern["sex"].isin(["M", "F"])]
    .groupby(["sex", "fatal_y_n"]).size().reset_index(name="count")
)
c4 = px.bar(
    sex_out, x="sex", y="count", color="fatal_y_n",
    barmode="stack",
    color_discrete_map=OUTCOME_COLORS,
    title="Attacks by Gender & Outcome",
    category_orders={"fatal_y_n": ["Y", "N", "Unknown"]},
    labels={"sex": "", "count": "Incidents", "fatal_y_n": "Outcome"},
)
c4.update_xaxes(tickvals=["M", "F"], ticktext=["Male", "Female"])
c4.update_layout(**L(height=360, legend=dict(title="")))

# ── 3.5  Age histogram: fatal vs non-fatal ───────────────────────────────────
age_ok = modern[modern["age"].between(1, 100)].copy()
c5 = go.Figure()
for outcome, color, label in [("N", "#26a69a", "Non-fatal"), ("Y", "#ef5350", "Fatal")]:
    c5.add_trace(go.Histogram(
        x=age_ok[age_ok["fatal_y_n"] == outcome]["age"],
        nbinsx=25, name=label,
        marker_color=color, opacity=0.75,
        hovertemplate="Age %{x}  —  %{y} cases<extra></extra>",
    ))
c5.update_layout(**L(
    barmode="overlay",
    title_text="Age Distribution: Fatal vs Non-Fatal",
    xaxis_title="Age", yaxis_title="Incidents",
    height=360, legend=dict(x=0.78, y=0.95, bgcolor="rgba(0,0,0,0.4)"),
))

# ── 3.6  Attack type × outcome ───────────────────────────────────────────────
type_out = (
    modern[modern["type"].isin(["unprovoked", "provoked", "watercraft", "sea disaster"])]
    .groupby(["type", "fatal_y_n"]).size().reset_index(name="count")
)
c6 = px.bar(
    type_out, x="type", y="count", color="fatal_y_n",
    barmode="stack",
    color_discrete_map=OUTCOME_COLORS,
    title="Attack Type vs Outcome",
    category_orders={
        "type": ["unprovoked", "provoked", "watercraft", "sea disaster"],
        "fatal_y_n": ["Y", "N", "Unknown"],
    },
    labels={"type": "Attack Type", "count": "Incidents", "fatal_y_n": "Outcome"},
)
c6.update_layout(**L(height=360, legend=dict(title="")))

# ── 3.7  Monthly seasonality ─────────────────────────────────────────────────
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
month_cnt = modern.groupby("month").size().reset_index(name="incidents")
month_cnt["name"] = month_cnt["month"].apply(lambda m: MONTHS[int(m)-1] if pd.notna(m) and 1 <= int(m) <= 12 else "?")

c7 = go.Figure(go.Bar(
    x=month_cnt["name"], y=month_cnt["incidents"],
    marker=dict(color=month_cnt["incidents"],
                colorscale=[[0, "#0d3b5e"], [1, "#00e5ff"]]),
    text=month_cnt["incidents"], textposition="outside",
    hovertemplate="<b>%{x}</b>  —  %{y} incidents<extra></extra>",
))
c7.update_layout(**L(
    title_text="Incidents by Month",
    xaxis=dict(categoryorder="array", categoryarray=MONTHS),
    yaxis_title="Incidents", height=360, showlegend=False,
))

# ── 3.8  Top 15 activities ───────────────────────────────────────────────────
act_cnt = (
    modern[modern["activity"].notna() & (modern["activity"].str.strip() != "")]
    .groupby("activity").size().reset_index(name="count")
    .nlargest(15, "count").sort_values("count")
)
c8 = go.Figure(go.Bar(
    x=act_cnt["count"], y=act_cnt["activity"],
    orientation="h",
    marker=dict(color=act_cnt["count"],
                colorscale=[[0, "#2a0505"], [1, "#ef5350"]]),
    text=act_cnt["count"], textposition="outside",
    hovertemplate="<b>%{y}</b>  —  %{x} incidents<extra></extra>",
))
c8.update_layout(**L(
    title_text="Top 15 Activities at Time of Incident",
    xaxis_title="Incidents", yaxis_title="",
    height=500, showlegend=False,
    margin=dict(l=120, r=60, t=52, b=20),
))

# ── 3.9  Decade total + fatality rate (dual axis) ────────────────────────────
decade_ok = (
    modern[modern["fatal_y_n"].isin(["Y", "N"]) & modern["decade"].notna()]
    .copy()
)
decade_ok["decade"] = decade_ok["decade"].astype(int)
dg = decade_ok.groupby(["decade", "fatal_y_n"]).size().unstack(fill_value=0).reset_index()

c9 = go.Figure()
if "Y" in dg.columns and "N" in dg.columns:
    dg["total"] = dg["Y"] + dg["N"]
    dg["rate"]  = (dg["Y"] / dg["total"] * 100).round(1)
    decade_label = dg["decade"].astype(str) + "s"
    c9.add_trace(go.Bar(
        x=decade_label, y=dg["total"],
        name="Total incidents", marker_color="rgba(66,165,245,0.55)",
        hovertemplate="<b>%{x}</b><br>Total: %{y:,}<extra></extra>",
    ))
    c9.add_trace(go.Scatter(
        x=decade_label, y=dg["rate"],
        name="Fatality rate %", mode="lines+markers",
        line=dict(color="#ef5350", width=2.5), marker=dict(size=8),
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>Fatality: %{y:.1f}%<extra></extra>",
    ))
c9.update_layout(**L(
    title_text="Total Incidents & Fatality Rate by Decade",
    xaxis_title="Decade",
    yaxis=dict(title="Incidents"),
    yaxis2=dict(title="Fatality Rate (%)", overlaying="y", side="right",
                range=[0, 60], showgrid=False),
    hovermode="x unified", height=400,
    legend=dict(x=0.02, y=0.97, bgcolor="rgba(0,0,0,0.4)"),
))

# ── 3.10  Scatter map (lat/lon) ──────────────────────────────────────────────
map_df = modern[modern["lat"].notna() & modern["lon"].notna()].copy()
map_df["fatal_label"] = map_df["fatal_y_n"].map({"Y": "Fatal", "N": "Non-fatal", "Unknown": "Unknown"})

c10 = px.scatter_geo(
    map_df.sample(min(4000, len(map_df)), random_state=42),
    lat="lat", lon="lon",
    color="fatal_label",
    color_discrete_map={"Fatal": "#ef5350", "Non-fatal": "#26a69a", "Unknown": "#546e7a"},
    size_max=6,
    opacity=0.6,
    hover_data={"lat": False, "lon": False, "country": True,
                "activity": True, "year": True},
    title="Incident Locations (sample of 4 000)",
    labels={"fatal_label": "Outcome"},
    projection="natural earth",
)
c10.update_geos(
    bgcolor=BG, showcoastlines=True, coastlinecolor="#1e3a5f",
    showland=True, landcolor="#111f35",
    showocean=True, oceancolor="#050d18", showlakes=False,
)
c10.update_traces(marker=dict(size=5))
c10.update_layout(**L(
    height=480,
    geo=dict(bgcolor=BG),
    legend=dict(title="Outcome", bgcolor="rgba(0,0,0,0.4)"),
))

# ─── 4. Key stats ────────────────────────────────────────────────────────────
n_total    = len(modern)
n_countries = country_cnt["country"].nunique()
n_fatal    = (modern["fatal_y_n"] == "Y").sum()
n_nonfatal = (modern["fatal_y_n"] == "N").sum()
fatal_rate  = round(n_fatal / (n_fatal + n_nonfatal) * 100, 1) if (n_fatal + n_nonfatal) else 0
yr_min      = int(modern["year"].min())
yr_max      = int(modern["year"].max())


# ─── 5. Assemble HTML ────────────────────────────────────────────────────────
def section(title: str, description: str, *chart_divs: str, full: bool = False) -> str:
    card_class = "chart-card full" if full else "chart-card"
    inner = "".join(chart_divs)
    return f"""
    <section class="section">
      <div class="{card_class}">
        <h2 class="chart-title">{title}</h2>
        <p class="chart-desc">{description}</p>
        {inner}
      </div>
    </section>"""


def two_col(left_title: str, left_desc: str, left_div: str,
            right_title: str, right_desc: str, right_div: str) -> str:
    return f"""
    <section class="section two-col">
      <div class="chart-card">
        <h2 class="chart-title">{left_title}</h2>
        <p class="chart-desc">{left_desc}</p>
        {left_div}
      </div>
      <div class="chart-card">
        <h2 class="chart-title">{right_title}</h2>
        <p class="chart-desc">{right_desc}</p>
        {right_div}
      </div>
    </section>"""


HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Shark Attack Data Analysis</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :root {{
      --bg:      #070f1f;
      --card:    #0d1f3c;
      --border:  #1a3a6b;
      --accent:  #00e5ff;
      --red:     #ef5350;
      --teal:    #26a69a;
      --text:    #c8d8f0;
      --muted:   #617899;
      --radius:  12px;
    }}

    html {{ scroll-behavior: smooth; }}

    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'Inter', system-ui, sans-serif;
      line-height: 1.6;
      min-height: 100vh;
    }}

    /* ── Hero ───────────────────────────────────────────────── */
    .hero {{
      position: relative;
      overflow: hidden;
      padding: 5rem 2rem 4rem;
      text-align: center;
      background:
        radial-gradient(ellipse 120% 80% at 50% 110%, rgba(0,100,180,0.25) 0%, transparent 70%),
        radial-gradient(ellipse 60% 40% at 80% 20%, rgba(239,83,80,0.10) 0%, transparent 60%),
        var(--bg);
    }}
    .hero::before {{
      content: "";
      position: absolute; inset: 0;
      background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='600' height='120'%3E%3Cpath d='M0 60 Q150 20 300 60 T600 60 V120 H0Z' fill='rgba(0,100,180,0.06)'/%3E%3C/svg%3E") repeat-x bottom;
      background-size: 600px 120px;
      opacity: 0.6;
      pointer-events: none;
    }}
    .hero-label {{
      display: inline-block;
      font-size: 0.72rem;
      font-weight: 600;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--accent);
      background: rgba(0,229,255,0.10);
      border: 1px solid rgba(0,229,255,0.25);
      border-radius: 100px;
      padding: 0.25rem 0.9rem;
      margin-bottom: 1.2rem;
    }}
    .hero h1 {{
      font-size: clamp(2rem, 5vw, 3.6rem);
      font-weight: 700;
      line-height: 1.15;
      margin-bottom: 1rem;
      background: linear-gradient(135deg, #e8f4ff 30%, var(--accent));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }}
    .hero-sub {{
      max-width: 620px;
      margin: 0 auto 2.5rem;
      font-size: 1rem;
      color: var(--muted);
    }}

    /* ── Stats row ──────────────────────────────────────────── */
    .stats-row {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 1rem;
      max-width: 900px;
      margin: 0 auto;
    }}
    .stat-card {{
      flex: 1 1 160px;
      background: rgba(13,31,60,0.85);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.2rem 1.4rem;
      text-align: center;
      backdrop-filter: blur(6px);
    }}
    .stat-value {{
      font-size: 2rem;
      font-weight: 700;
      color: var(--accent);
      display: block;
      line-height: 1.1;
    }}
    .stat-label {{
      font-size: 0.78rem;
      font-weight: 500;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
      margin-top: 0.3rem;
      display: block;
    }}

    /* ── Layout ─────────────────────────────────────────────── */
    .container {{
      max-width: 1280px;
      margin: 0 auto;
      padding: 2rem 1.5rem 4rem;
      display: grid;
      gap: 1.5rem;
    }}

    .section {{
      display: grid;
      gap: 1.5rem;
    }}
    .two-col {{
      grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    }}

    .chart-card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.5rem;
      transition: border-color 0.2s;
      /* min-width:0 lets the grid cell shrink below its content size */
      min-width: 0;
    }}
    .chart-card:hover {{ border-color: rgba(0,229,255,0.35); }}
    .chart-card.full {{ grid-column: 1 / -1; }}

    .chart-title {{
      font-size: 1rem;
      font-weight: 600;
      color: #e8f0fe;
      margin-bottom: 0.35rem;
    }}
    .chart-desc {{
      font-size: 0.82rem;
      color: var(--muted);
      margin-bottom: 1rem;
      max-width: 680px;
    }}

    /* ── Section headings ───────────────────────────────────── */
    .section-heading {{
      grid-column: 1 / -1;
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 0.5rem 0 0.25rem;
      border-bottom: 1px solid var(--border);
    }}
    .section-heading h2 {{
      font-size: 1.3rem;
      font-weight: 600;
      color: #e8f0fe;
    }}
    .section-heading .dot {{
      width: 8px; height: 8px;
      border-radius: 50%;
      background: var(--accent);
      flex-shrink: 0;
    }}

    /* ── Footer ─────────────────────────────────────────────── */
    footer {{
      text-align: center;
      padding: 2rem 1rem 3rem;
      font-size: 0.8rem;
      color: var(--muted);
      border-top: 1px solid var(--border);
    }}
    footer a {{ color: var(--accent); text-decoration: none; }}

    @media (max-width: 600px) {{
      .two-col {{ grid-template-columns: 1fr; }}
      .hero {{ padding: 3rem 1rem 2.5rem; }}
    }}
  </style>
</head>
<body>

<!-- ── Hero ─────────────────────────────────────────────────────────────────── -->
<header class="hero">
  <div class="hero-label">Data Analysis · Portfolio Project</div>
  <h1>Shark Attack<br>Data Analysis</h1>
  <p class="hero-sub">
    Exploring {n_total:,} recorded incidents from {yr_min} to {yr_max} across
    {n_countries} countries — uncovering patterns in geography, seasonality,
    victim demographics, and fatality outcomes.
  </p>
  <div class="stats-row">
    <div class="stat-card">
      <span class="stat-value">{n_total:,}</span>
      <span class="stat-label">Total incidents</span>
    </div>
    <div class="stat-card">
      <span class="stat-value">{n_countries}</span>
      <span class="stat-label">Countries</span>
    </div>
    <div class="stat-card">
      <span class="stat-value">{fatal_rate}%</span>
      <span class="stat-label">Fatality rate</span>
    </div>
    <div class="stat-card">
      <span class="stat-value">{yr_max - yr_min}</span>
      <span class="stat-label">Years of data</span>
    </div>
  </div>
</header>

<!-- ── Main content ──────────────────────────────────────────────────────────── -->
<main class="container">

  <!-- heading: timeline -->
  <div class="section-heading">
    <span class="dot"></span><h2>Trends Over Time</h2>
  </div>

  <!-- chart 1: incidents per year -->
  {section("Incidents per Year",
           "Annual incident count since 1900, smoothed with a 10-year rolling average. "
           "The dramatic rise from the 1960s onward reflects growing ocean recreation — "
           "not necessarily more aggressive sharks.",
           fig_html(c1), full=True)}

  <!-- chart 9: decade summary -->
  {section("Total Incidents &amp; Fatality Rate by Decade",
           "Each bar shows the total incidents per decade; the red line tracks how the "
           "share of fatal attacks has evolved. Medical advances and faster rescue services "
           "have contributed to the declining fatality rate.",
           fig_html(c9), full=True)}

  <!-- heading: geography -->
  <div class="section-heading" style="margin-top:1rem;">
    <span class="dot"></span><h2>Geography</h2>
  </div>

  <!-- chart 2: choropleth -->
  {section("Global Distribution",
           "Countries shaded by total recorded incidents. The USA, Australia, and South Africa "
           "consistently top the rankings — reflecting both large coastlines and strong reporting cultures.",
           fig_html(c2), full=True)}

  <!-- chart 10: scatter map -->
  {section("Incident Locations (sample)",
           "Individual incident coordinates (where available) plotted on the globe. "
           "Fatal incidents are highlighted in red. Coastal hotspots are clearly visible "
           "around Florida, eastern Australia, and the Western Cape.",
           fig_html(c10), full=True)}

  <!-- chart 3 + 4: top countries + gender -->
  {two_col(
      "Top 15 Countries",
      "The United States alone accounts for more than a third of all global incidents. "
      "Australia and South Africa are distant second and third.",
      fig_html(c3),
      "Attacks by Gender &amp; Outcome",
      "Males vastly outnumber females in the dataset — partly because more men engage "
      "in high-risk water sports, and partly due to historical under-reporting of female incidents.",
      fig_html(c4),
  )}

  <!-- heading: victims -->
  <div class="section-heading" style="margin-top:1rem;">
    <span class="dot"></span><h2>Victim Demographics</h2>
  </div>

  <!-- chart 5 + 6: age + attack type -->
  {two_col(
      "Age Distribution",
      "Most victims are young adults (teens to mid-30s), reflecting who spends the most "
      "time in the ocean. Fatal attacks show a slightly older distribution.",
      fig_html(c5),
      "Attack Type vs Outcome",
      "Unprovoked attacks dominate the dataset and carry a higher fatality risk than "
      "provoked incidents. Sea disasters, while rarer, have the highest absolute fatal count.",
      fig_html(c6),
  )}

  <!-- heading: patterns -->
  <div class="section-heading" style="margin-top:1rem;">
    <span class="dot"></span><h2>Behavioural &amp; Seasonal Patterns</h2>
  </div>

  <!-- chart 7 + 8: seasonal + activities -->
  {two_col(
      "Incidents by Month",
      "January and February peak in the Southern Hemisphere summer (Australia, South Africa), "
      "while June–August reflect the Northern Hemisphere beach season.",
      fig_html(c7),
      "Top 15 Activities",
      "Surfing and swimming top the list by a large margin, followed by activities like "
      "body boarding, diving, and wading. Higher exposure time drives higher incident counts.",
      fig_html(c8),
  )}

</main>

<!-- ── Footer ────────────────────────────────────────────────────────────────── -->
<footer>
  <p>Data source: Global Shark Attack File (GSAF) — processed and analysed as part of a data-engineering portfolio project.</p>
  <p style="margin-top:0.5rem;">Built with Python · Pandas · Plotly</p>
</footer>

<script>
  /* After the page has fully rendered, fire a resize event so every
     Plotly chart recalculates its width to fit its grid-cell container. */
  window.addEventListener('load', function () {{
    setTimeout(function () {{
      window.dispatchEvent(new Event('resize'));
    }}, 100);
  }});
</script>

</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as fh:
    fh.write(HTML)

print("✓  index.html written")
print(f"   {len(HTML):,} characters  ·  ~{len(HTML.encode())//1024} KB")
