# 🌍 World Happiness Report Analysis (2011–2025)

An interactive analytics dashboard exploring global happiness trends across 168 countries from 2011 to 2025, built with Python, Panel, and hvPlot.

## 📊 Dashboard Features

- **KPI Cards** — Countries tracked, happiest country, top score & global average
- **Top 10 Bar Chart** — Happiest countries for any selected year
- **Happiness Leaderboard** — Sortable, paginated data table
- **GDP vs Happiness Scatter** — Correlation between wealth and well-being
- **Social Support vs Life Expectancy** — Key drivers of happiness
- **Factor Impact Analysis** — Average weight of each happiness factor
- **Correlation Heatmap** — Relationships between all key variables
- **Long-term Trends** — Year-over-year happiness trends for top 5 countries
- **Biggest Movers** — Countries with the largest happiness changes (2011→2025)

All charts are interactive and update dynamically with a **Year Slider**.

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/sidhant-here/World-Happiness-Report-Analysis.git
cd World-Happiness-Report-Analysis
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add the dataset
Download the **World Happiness Report** dataset (Excel format) and place it in the project folder as:
```
python clean final.xlsx
```
> The dataset is not included in this repo. You can get it from [World Happiness Report](https://worldhappiness.report/).

### 4. Generate and run the notebook
```bash
python create_notebook.py
```
Then open `World_Happiness_Analysis.ipynb` in **Jupyter Lab** and run all cells.  
The last cell will launch the dashboard in a **new browser tab** automatically.

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| [Panel](https://panel.holoviz.org/) | Dashboard layout & interactivity |
| [hvPlot](https://hvplot.holoviz.org/) | Interactive bar & scatter charts |
| [Matplotlib](https://matplotlib.org/) | Static factor & heatmap charts |
| [Seaborn](https://seaborn.pydata.org/) | Correlation heatmap styling |
| [Pandas](https://pandas.pydata.org/) | Data manipulation |
| [nbformat](https://nbformat.readthedocs.io/) | Programmatic notebook generation |

## 📁 Project Structure

```
├── create_notebook.py          # Script to generate the full notebook
├── World_Happiness_Analysis.ipynb  # Main analysis + dashboard notebook
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## 🎨 Dashboard Preview

> Launch the dashboard to see the full interactive experience with a premium cyan-accented dark UI, glassmorphism cards, and a custom theme toggle.

## 📄 License

This project is licensed under the MIT License.
