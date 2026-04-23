import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

# Cell 1: Markdown
cells.append(nbf.v4.new_markdown_cell("""# 🌍 World Happiness Report — Comprehensive Data Analysis (2011–2025)
### Visualizations and relationships from `python clean final.xlsx`"""))

# Cell 2: Imports
cells.append(nbf.v4.new_code_cell("""# ── Imports ──────────────────────────────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style="whitegrid", palette="muted")

# ── Load Data ─────────────────────────────────────────────────────────────────
df = pd.read_excel('python clean final.xlsx')
df.rename(columns={
    'Explained by: Freedom to make life choices': 'Freedom',
    'Explained by: Generosity': 'Generosity',
    'Explained by: Perceptions of corruption': 'Corruption_Impact',
    'Explained by: Log GDP per capita': 'GDP_Impact',
    'Explained by: Social support': 'Social_Support',
    'Explained by: Healthy life expectancy': 'Life_Expectancy_Impact'
}, inplace=True)
"""))

# Static Charts (We keep the top 10, gdp, trends, factors, heatmap, bubble, changes)
# I'll include just a few markdown and summary stat cells, because the dashboard will have EVERYTHING.
# The user wants "all changes and dashboard in world_happiness_analysis.ipynb"
cells.append(nbf.v4.new_markdown_cell("""---
## Comprehensive Interactive Dashboard
*Run the cell below to launch the full Dashboard with ALL visualizations in a new tab.*"""))

cells.append(nbf.v4.new_code_cell("""import panel as pn
import hvplot.pandas
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

pn.extension('tabulator', design='material')

# Prepare data
df_clean = df.dropna(subset=['GDP_Impact', 'Social_Support', 'Life_Expectancy_Impact']).copy()
year_slider = pn.widgets.IntSlider(name='Select Year', start=int(df_clean.Year.min()), end=int(df_clean.Year.max()), step=1, value=2025, align='center', sizing_mode='stretch_width')

idf = df_clean.interactive()

# 1. Top 10 Bar (hvplot)
top_10_bar = (
    idf[idf.Year == year_slider]
    .sort_values('Happiness_Score', ascending=False)
    .head(10)
    .hvplot(x='Country', y='Happiness_Score', kind='bar', 
            color='Happiness_Score', cmap='GnBu', rot=45, height=350, responsive=True)
)

# 2. Table
top_10_table = (
    idf[idf.Year == year_slider][['Rank', 'Country', 'Happiness_Score']]
    .sort_values('Rank')
    .head(10)
    .pipe(pn.widgets.Tabulator, pagination='remote', page_size=10, theme='bootstrap4', height=350, sizing_mode='stretch_width')
)

# 3. Scatter 1 (hvplot)
gdp_scatter = (
    idf[idf.Year == year_slider]
    .hvplot(x='GDP_Impact', y='Happiness_Score', kind='scatter', 
            hover_cols=['Country', 'Rank'], 
            color='Happiness_Score', cmap='GnBu', size=150, alpha=0.8, height=350, responsive=True)
)

# 4. Scatter 2 (hvplot)
social_scatter = (
    idf[idf.Year == year_slider]
    .hvplot(x='Social_Support', y='Life_Expectancy_Impact', kind='scatter',
            hover_cols=['Country'], color='Happiness_Score', cmap='plasma', size=150, alpha=0.8, height=350, responsive=True)
)

# 5. Average Factors (Matplotlib bound function)
def plot_avg_factors(year):
    factors = ['GDP_Impact', 'Social_Support', 'Freedom', 'Life_Expectancy_Impact', 'Corruption_Impact', 'Generosity']
    avg_factors = df_clean[df_clean['Year'] == year][factors].mean().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(avg_factors.index, avg_factors.values, color=sns.color_palette("GnBu_r", len(avg_factors)), edgecolor='white')
    clean_labels = [f.replace('_Impact', '').replace('_', ' ') for f in avg_factors.index]
    ax.set_xticklabels(clean_labels, rotation=25, ha='right', fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.01, f'{h:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#333333')
        
    plt.tight_layout()
    plt.close(fig)
    return fig

# 6. Correlation Heatmap (Matplotlib bound function)
def plot_heatmap(year):
    cols = ['Happiness_Score', 'GDP_Impact', 'Social_Support', 'Life_Expectancy_Impact', 'Freedom', 'Generosity', 'Corruption_Impact']
    corr_df = df_clean[df_clean['Year'] == year][cols]
    corr_df.columns = [c.replace('_Impact', '').replace('_', ' ').replace('Happiness_Score', 'Happiness') for c in corr_df.columns]
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    mask = np.triu(np.ones_like(corr_df.corr(), dtype=bool))
    sns.heatmap(corr_df.corr(), mask=mask, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1, center=0, ax=ax, cbar_kws={"shrink": .8})
    plt.tight_layout()
    plt.close(fig)
    return fig

# 7. Trends (Static Matplotlib)
def plot_trends():
    top5 = ['Costa Rica', 'Denmark', 'Finland', 'Iceland', 'Sweden']
    trend = df_clean[df_clean['Country'].isin(top5)].pivot(index='Year', columns='Country', values='Happiness_Score')
    fig, ax = plt.subplots(figsize=(9, 4.5))
    
    palette = {'Costa Rica': '#1f77b4', 'Denmark': '#ff7f0e', 'Finland': '#2ca02c', 'Iceland': '#d62728', 'Sweden': '#9467bd'}
    for c in top5:
        ax.plot(trend.index, trend[c], marker='o', linewidth=2.5, label=c, color=palette[c])
        
    ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', frameon=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xticks(trend.index)
    plt.tight_layout()
    plt.close(fig)
    return fig

# 8. Biggest Changes (Static Matplotlib)
def plot_changes():
    d11 = df_clean[df_clean['Year'] == 2011].set_index('Country')['Happiness_Score']
    d25 = df_clean[df_clean['Year'] == 2025].set_index('Country')['Happiness_Score']
    change = (d25 - d11).dropna()
    plot_df = pd.concat([change.nlargest(5), change.nsmallest(5)]).sort_values()
    
    fig, ax = plt.subplots(figsize=(9, 4.5))
    colors = ['#e11d48' if v < 0 else '#10b981' for v in plot_df]
    bars = ax.barh(plot_df.index, plot_df.values, color=colors, edgecolor='none')
    ax.axvline(0, color='#333333', linewidth=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    for i, bar in enumerate(bars):
        val = bar.get_width()
        ax.text(val + (0.05 if val>0 else -0.05), bar.get_y() + bar.get_height()/2, 
                f'{val:+.2f}', va='center', ha=('left' if val>0 else 'right'), fontweight='bold', color=colors[i])

    plt.tight_layout()
    plt.close(fig)
    return fig

# Bind interactive functions
avg_factors_pane = pn.bind(plot_avg_factors, year_slider)
heatmap_pane = pn.bind(plot_heatmap, year_slider)

# ── KPI Indicators ────────────────────────────────────────────────────────────
df_latest = df_clean[df_clean['Year'] == df_clean['Year'].max()]
kpi_total   = str(df_latest['Country'].nunique())
kpi_best    = df_latest.loc[df_latest['Rank'] == df_latest['Rank'].min(), 'Country'].values[0]
kpi_avg     = f"{df_latest['Happiness_Score'].mean():.2f}"
kpi_best_sc = f"{df_latest['Happiness_Score'].max():.2f}"

def make_kpi(value, label, icon, accent):
    return pn.pane.HTML(f'''
    <div style="background:linear-gradient(135deg, {accent}18, {accent}08);
         backdrop-filter:blur(10px); border:1px solid {accent}33;
         border-radius:16px; padding:20px 16px; text-align:center;
         position:relative; overflow:hidden;">
        <div style="position:absolute;top:8px;right:12px;font-size:22px;opacity:0.25">{icon}</div>
        <div style="font-size:30px;font-weight:800;color:{accent};letter-spacing:-0.5px;
             text-shadow:0 0 20px {accent}33">{value}</div>
        <div style="font-size:10px;font-weight:700;color:#64748b;text-transform:uppercase;
             letter-spacing:1.5px;margin-top:6px">{label}</div>
    </div>''', sizing_mode='stretch_width')

kpi_row = pn.Row(
    make_kpi(kpi_total,   'Countries Tracked', '🌐', '#00d4ff'),
    make_kpi(kpi_best,    'Happiest Country',  '🏆', '#10b981'),
    make_kpi(kpi_best_sc, 'Highest Score',     '⭐', '#f59e0b'),
    make_kpi(kpi_avg,     'Global Average',    '📊', '#ef4444'),
    sizing_mode='stretch_width', margin=(0,8,12,8)
)

# ── Card wrapper ──────────────────────────────────────────────────────────────
def card(content, title):
    return pn.Card(
        content, title=title, collapsible=False,
        header_background='transparent', header_color='#0e7490',
        styles={
            'border-radius':'16px',
            'border':'1px solid #e0f2fe',
            'box-shadow':'0 1px 3px rgb(0 0 0 / 0.04), 0 1px 2px rgb(0 0 0 / 0.03)',
            'overflow':'hidden',
            'transition':'all 0.25s ease',
        },
        sizing_mode='stretch_width', margin=(8,8)
    )

# ── Custom CSS (cyan / aqua theme with dark-mode support) ─────────────────────
custom_css = '''
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap");

:root {
  --design-primary-color: #00d4ff !important;
  --design-primary-text-color: #ffffff !important;
  --design-background-color: #f0fdff !important;
}

/* ── Typography ─────────────────────────── */
body, .markdown, p, span, div { font-family: "Inter", "Segoe UI", system-ui, -apple-system, sans-serif !important; }

/* ── Header ─────────────────────────────── */
#header {
    background: linear-gradient(135deg, #0c4a6e 0%, #164e63 50%, #134e4a 100%) !important;
    box-shadow: 0 2px 12px rgb(0 0 0 / 0.15) !important;
}
#header .title { font-weight: 800 !important; letter-spacing: -0.5px !important; font-size: 18px !important; }

/* ── Sidebar ────────────────────────────── */
#sidebar {
    background: linear-gradient(180deg, #0c4a6e 0%, #164e63 60%, #0f172a 100%) !important;
    box-shadow: 2px 0 15px rgb(0 0 0 / 0.1) !important;
}

/* ── Main area ──────────────────────────── */
#main { background: linear-gradient(180deg, #f0fdff 0%, #ecfeff 30%, #f8fafc 100%) !important; }

/* ── Cards ──────────────────────────────── */
.card { background: rgba(255,255,255,0.85) !important; backdrop-filter: blur(8px) !important; }
.card:hover {
    box-shadow: 0 8px 25px rgb(0 212 255 / 0.08), 0 2px 8px rgb(0 0 0 / 0.04) !important;
    transform: translateY(-1px) !important;
    border-color: #67e8f9 !important;
}
.card-header {
    font-weight: 700 !important; font-size: 13px !important; padding: 14px 20px !important;
    border-bottom: 1px solid #e0f2fe !important; letter-spacing: -0.2px !important;
    color: #0e7490 !important;
}

/* ── Dark mode overrides ────────────────── */
body.dark #main { background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important; }
body.dark .card { background: rgba(30,41,59,0.9) !important; border-color: #334155 !important; }
body.dark .card:hover { border-color: #00d4ff55 !important; box-shadow: 0 8px 25px rgb(0 212 255 / 0.12) !important; }
body.dark .card-header { color: #67e8f9 !important; border-bottom-color: #334155 !important; }

/* ── Slider ─────────────────────────────── */
.noUi-connect { background: linear-gradient(90deg, #00d4ff, #06b6d4) !important; }
.noUi-handle { border-color: #00d4ff !important; }

/* ── Scrollbar ──────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #06b6d4; border-radius: 3px; }

/* ── Enhanced Theme Toggle (pill bar) ───── */
#header-items {
    display: flex !important;
    align-items: center !important;
    gap: 0 !important;
    background: rgba(0, 0, 0, 0.25) !important;
    backdrop-filter: blur(12px) !important;
    border-radius: 22px !important;
    padding: 4px 5px !important;
    border: 1px solid rgba(0, 212, 255, 0.2) !important;
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.08), inset 0 1px 2px rgba(255,255,255,0.05) !important;
}
#header-items button {
    border: none !important;
    border-radius: 18px !important;
    width: 36px !important;
    height: 36px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    transition: all 0.35s cubic-bezier(.4,0,.2,1) !important;
    background: transparent !important;
    color: rgba(255, 255, 255, 0.5) !important;
    font-size: 18px !important;
    margin: 0 1px !important;
    position: relative !important;
}
#header-items button:hover {
    background: rgba(0, 212, 255, 0.15) !important;
    color: #67e8f9 !important;
    transform: scale(1.1) !important;
}
#header-items button.active,
#header-items button[active] {
    background: linear-gradient(135deg, rgba(0,212,255,0.3), rgba(6,182,212,0.2)) !important;
    color: #00d4ff !important;
    box-shadow: 0 0 12px rgba(0, 212, 255, 0.35) !important;
    text-shadow: 0 0 8px rgba(0, 212, 255, 0.5) !important;
}
'''

# ── Sidebar ───────────────────────────────────────────────────────────────────
sidebar_content = [
    pn.pane.HTML('''
    <div style="text-align:center;padding:16px 0 6px">
        <div style="font-size:42px;filter:drop-shadow(0 0 8px rgba(0,212,255,0.4))">🌍</div>
    </div>'''),
    pn.pane.HTML('''
    <div style="text-align:center;margin-bottom:4px">
        <span style="color:#e0f2fe;font-size:16px;font-weight:800;letter-spacing:-0.5px">World Happiness</span><br>
        <span style="color:#67e8f9;font-size:13px;font-weight:600">Analytics Platform</span>
    </div>'''),
    pn.pane.HTML('<div style="text-align:center;color:#94a3b8;font-size:10px;letter-spacing:2px;text-transform:uppercase;margin-bottom:16px">2011 – 2025 · 168 Countries</div>'),
    pn.layout.Divider(),
    pn.pane.HTML('<div style="color:#67e8f9;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:2px;margin:10px 0 8px">⏱ Select Year</div>'),
    year_slider,
    pn.pane.HTML('<div style="text-align:center;color:#475569;font-size:10px;margin-top:4px">Drag to travel through time</div>'),
    pn.layout.Divider(),
    pn.pane.HTML('<div style="color:#67e8f9;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:2px;margin:10px 0 10px">📊 Sections</div>'),
    pn.pane.HTML('''<div style="font-size:12px;line-height:2.4">
        <div style="color:#e0f2fe">🏆 Top 10 Countries</div>
        <div style="color:#bae6fd">💰 GDP vs Happiness</div>
        <div style="color:#a5f3fc">🫂 Social vs Life Expectancy</div>
        <div style="color:#99f6e4">⚖️ Factor Impact</div>
        <div style="color:#a7f3d0">🔗 Correlation Map</div>
        <div style="color:#bfdbfe">📈 Multi-Year Trends</div>
        <div style="color:#c7d2fe">🚀 Biggest Movers</div>
    </div>'''),
    pn.layout.Divider(),
    pn.pane.HTML('''<div style="text-align:center;margin-top:8px">
        <div style="color:#334155;font-size:9px;letter-spacing:1px;text-transform:uppercase">Powered by</div>
        <div style="color:#67e8f9;font-size:11px;font-weight:700;margin-top:2px">Panel · hvPlot · Matplotlib</div>
    </div>''')
]

# ── Template ──────────────────────────────────────────────────────────────────
template = pn.template.FastListTemplate(
    title='🌍 World Happiness Analytics Platform',
    sidebar=sidebar_content,
    main=[
        kpi_row,
        pn.Row(
            card(top_10_bar.panel(), '🏆 Top 10 Happiest Countries'),
            card(top_10_table.panel(), '📋 Happiness Leaderboard'),
        ),
        pn.Row(
            card(gdp_scatter.panel(), '💰 Happiness Score vs. GDP Impact'),
            card(social_scatter.panel(), '🫂 Social Support vs. Life Expectancy'),
        ),
        pn.Row(
            card(pn.pane.Matplotlib(avg_factors_pane, sizing_mode='stretch_width', tight=True), '⚖️ Average Factor Impact on Happiness'),
            card(pn.pane.Matplotlib(heatmap_pane, sizing_mode='stretch_width', tight=True), '🔗 Feature Correlation Heatmap'),
        ),
        pn.Row(
            card(pn.pane.Matplotlib(plot_trends(), sizing_mode='stretch_width', tight=True), '📈 Happiness Trends – Top 5 Countries'),
            card(pn.pane.Matplotlib(plot_changes(), sizing_mode='stretch_width', tight=True), '🚀 Biggest Movers (2011 → 2025)'),
        ),
    ],
    accent_base_color='#00d4ff',
    header_background='#0c4a6e',
    sidebar_width=280,
    main_max_width='1500px',
    theme_toggle=True,
    raw_css=[custom_css],
)

template.show()
"""))

cells.append(nbf.v4.new_markdown_cell("""---
## Summary Statistics
*Key numbers from the 2025 report.*"""))

cells.append(nbf.v4.new_code_cell("""df25 = df[df['Year'] == 2025]

print('=' * 60)
print('  🌍 WORLD HAPPINESS REPORT — 2025 KEY INSIGHTS 🌍')
print('=' * 60)
print(f'  Total countries tracked : {df25["Country"].nunique()}')
print(f'  Happiest country        : {df25.loc[df25["Rank"]==1, "Country"].values[0]} (Score: {df25["Happiness_Score"].max():.3f})')
print(f'  Least happy country     : {df25.loc[df25["Rank"]==df25["Rank"].max(), "Country"].values[0]} (Score: {df25["Happiness_Score"].min():.3f})')
print(f'  Global average score    : {df25["Happiness_Score"].mean():.3f}')

valid_corr = df25.dropna(subset=['GDP_Impact', 'Happiness_Score'])
r_gdp = np.corrcoef(valid_corr['GDP_Impact'], valid_corr['Happiness_Score'])[0,1]
print(f'  GDP–Happiness Correl.   : r = {r_gdp:.4f}')

valid_corr_soc = df25.dropna(subset=['Social_Support', 'Happiness_Score'])
r_soc = np.corrcoef(valid_corr_soc['Social_Support'], valid_corr_soc['Happiness_Score'])[0,1]
print(f'  Social Sup.-Happiness   : r = {r_soc:.4f}')

print('=' * 60)"""))

nb['cells'] = cells

with open('World_Happiness_Analysis.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print("Notebook generated successfully with comprehensive dashboard!")
