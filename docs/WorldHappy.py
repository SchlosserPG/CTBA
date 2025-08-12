# docs/world_happiness.py
import dash
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
from pathlib import Path

app = Dash(__name__)
server = app.server  

dash.register_page(__name__, path="/happy", name="World Happiness", order=3)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "world_happiness.csv"
df = pd.read_csv(DATA_PATH).rename(columns={
    "country": "Country",
    "year": "Year",
    "Life Ladder": "Happiness Score"
})
df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype(int)

layout = html.Div(
    style={'padding': '20px', 'backgroundColor': "#B9975B"},
    children=[
        html.H1("World Happiness Dashboard", style={'textAlign': 'center', 'color': '#0c2d3e'}),
        html.Div(
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': str(y), 'value': y} for y in sorted(df['Year'].unique())],
                value=int(df['Year'].max()),
                clearable=False,
                style={'width': '50%'}
            ),
            style={'textAlign': 'center', 'marginBottom': '30px'}
        ),
        dcc.Graph(id='happiness-map'),
        dcc.Graph(id='top-bottom-bar'),
    ]
)

@callback(
    Output('happiness-map', 'figure'),
    Output('top-bottom-bar', 'figure'),
    Input('year-dropdown', 'value')
)
def update_dashboard(selected_year):
    d = df[df['Year'] == int(selected_year)]
    map_fig = px.choropleth(
        d, locations="Country", locationmode="country names",
        color="Happiness Score", hover_name="Country",
        color_continuous_scale="viridis",
        title=f"Happiness Score by Country - {selected_year}"
    )
    top_bottom = pd.concat([d.nlargest(10, 'Happiness Score'),
                            d.nsmallest(10, 'Happiness Score')])
    bar_fig = px.bar(
        top_bottom.sort_values('Happiness Score'),
        x='Happiness Score', y='Country', orientation='h',
        color='Happiness Score',
        title=f"Top and Bottom 10 Countries - {selected_year}",
        color_continuous_scale='RdYlGn'
    )
    return map_fig, bar_fig
