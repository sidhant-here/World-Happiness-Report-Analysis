import nbformat as nbf

nb = nbf.v4.new_notebook()

cells = []

# Cell 1: Markdown
cells.append(nbf.v4.new_markdown_cell("""# 🌍 World Happiness — Interactive Dashboard
*Using Panel, hvPlot, and the World Happiness Report Dataset (2011-2025)*"""))

# Cell 2: Imports and Data Prep
cells.append(nbf.v4.new_code_cell("""import pandas as pd
import panel as pn
import hvplot.pandas

pn.extension('tabulator')

# ── Load Data ─────────────────────────────────────────────────────────────────
df = pd.read_excel('python clean final.xlsx')

# Clean columns
df.rename(columns={
    'Explained by: Freedom to make life choices': 'Freedom',
    'Explained by: Generosity': 'Generosity',
    'Explained by: Perceptions of corruption': 'Corruption_Impact',
    'Explained by: Log GDP per capita': 'GDP_Impact',
    'Explained by: Social support': 'Social_Support',
    'Explained by: Healthy life expectancy': 'Life_Expectancy_Impact'
}, inplace=True)

df = df.dropna(subset=['GDP_Impact', 'Social_Support', 'Life_Expectancy_Impact'])

# Make DataFrame interactive
idf = df.interactive()
"""))

# Cell 3: Dashboard Components
cells.append(nbf.v4.new_code_cell("""# ── Settings ──────────────────────────────────────────────────────────────────
# Year slider for the interactive dashboard
year_slider = pn.widgets.IntSlider(name='Select Year', start=int(df.Year.min()), end=int(df.Year.max()), step=1, value=2025)

# ── Plots ─────────────────────────────────────────────────────────────────────

# 1. Top 10 Happiest Countries Bar Plot
top_10_bar_plot = (
    idf[idf.Year == year_slider]
    .sort_values('Happiness_Score', ascending=False)
    .head(10)
    .hvplot(x='Country', y='Happiness_Score', kind='bar', 
            title='Top 10 Happiest Countries',
            color='Happiness_Score', cmap='viridis', rot=45)
)

# 2. Top 10 Table
top_10_table = (
    idf[idf.Year == year_slider][['Rank', 'Country', 'Happiness_Score']]
    .sort_values('Rank')
    .head(10)
    .pipe(pn.widgets.Tabulator, pagination='remote', page_size=10, sizing_mode='stretch_width')
)

# 3. Happiness vs GDP Scatter
happiness_vs_gdp_scatterplot = (
    idf[idf.Year == year_slider]
    .hvplot(x='GDP_Impact', y='Happiness_Score', kind='scatter', 
            hover_cols=['Country', 'Rank'], 
            title='Happiness Score vs. GDP Impact', 
            color='Happiness_Score', cmap='viridis', size=100, alpha=0.8)
)

# 4. Social Support vs Life Expectancy Impact
social_vs_life_scatter = (
    idf[idf.Year == year_slider]
    .hvplot(x='Social_Support', y='Life_Expectancy_Impact', kind='scatter',
            hover_cols=['Country'], color='Happiness_Score', cmap='plasma', size=100, alpha=0.8,
            title='Social Support vs. Life Expectancy Impact')
)
"""))

# Cell 4: Layout Template
cells.append(nbf.v4.new_code_cell("""# ── Layout using Template ─────────────────────────────────────────────────────
template = pn.template.FastListTemplate(
    title='World Happiness Dashboard', 
    sidebar=[
        pn.pane.Markdown("# Global Happiness Analysis"), 
        pn.pane.Markdown("#### Explore how GDP, Social Support, and Life Expectancy contribute to the overall Happiness Score of countries worldwide. Adjust the year slider below to see how relationships evolve dynamically."), 
        pn.pane.Markdown("## Settings"),   
        year_slider
    ],
    main=[
        pn.Row(
            pn.Column(top_10_bar_plot.panel(width=700), margin=(0,25)), 
            top_10_table.panel(width=500)
        ), 
        pn.Row(
            pn.Column(happiness_vs_gdp_scatterplot.panel(width=600), margin=(0,25)), 
            pn.Column(social_vs_life_scatter.panel(width=600))
        )
    ],
    accent_base_color="#1f77b4",
    header_background="#1f77b4",
)

# Servable will display the template perfectly within Jupyter!
template.servable()
"""))

nb['cells'] = cells

with open('Interactive_Dashboard.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print("Interactive Dashboard Notebook generated successfully!")
