# docs/electricity.py
import dash
from dash import html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
from pathlib import Path

dash.register_page(__name__, path="/electricity", name="Electricity", order=2)

# Robust path: project_root/data/electricity_prices.csv
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "electricity_prices.csv"
df = pd.read_csv(DATA_PATH)
df.columns = [c.strip() for c in df.columns]
df["year"] = pd.to_numeric(df["year"], errors="coerce").astype(int)

layout = html.Div(
    style={"backgroundColor": "#0c2d3e", "padding": "20px", "minHeight": "100vh"},
    children=[
        html.H1("Electricity Prices by US State",
                style={"color": "white", "textAlign": "center"}),

        dcc.Slider(
            id="year-slider",
            min=int(df["year"].min()),
            max=int(df["year"].max()),
            value=int(df["year"].min()),
            marks={str(y): str(y) for y in sorted(df["year"].unique())},
            step=None,
            tooltip={"placement": "bottom", "always_visible": True},
        ),

        html.Div(style={"height": "12px"}),
        dcc.Graph(id="choropleth-map"),
    ],
)

@callback(
    Output("choropleth-map", "figure"),
    Input("year-slider", "value"),
)
def update_map(selected_year):
    d = df[df["year"] == int(selected_year)]
    fig = px.choropleth(
        d,
        locations="state",              # two-letter codes
        locationmode="USA-states",
        color="price",
        scope="usa",
        color_continuous_scale="Reds",
        labels={"price": "Price (cents/kWh)"},
        title=f"Residential Electricity Prices — {selected_year}",
    )
    fig.update_layout(geo=dict(bgcolor="#0c2d3e"),
                      paper_bgcolor="#0c2d3e",
                      font_color="white",
                      margin=dict(l=10, r=10, t=50, b=10))
    return fig
