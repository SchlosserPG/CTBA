##at local host: http://localhost:8050/
##Control + C to stop the server


import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load your CSV from data folder
df = pd.read_csv('data/electricity_prices.csv')

# Ensure consistent column names
df.columns = [col.strip() for col in df.columns]
df['year'] = df['year'].astype(int)

# Dash app
app = dash.Dash(__name__)
app.title = "Electricity Prices by US State"

# App layout
app.layout = html.Div(style={'backgroundColor': '#0c2d3e', 'padding': '20px'}, children=[
    html.H1("Electricity Prices by US State", style={'color': 'white', 'textAlign': 'center'}),

    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in sorted(df['year'].unique())},
        step=None,
        tooltip={"placement": "bottom", "always_visible": True}
    ),

    dcc.Graph(id='choropleth-map')
])

# Callback
@app.callback(
    Output('choropleth-map', 'figure'),
    Input('year-slider', 'value')
)
def update_map(selected_year):
    filtered_df = df[df['year'] == selected_year]

    fig = px.choropleth(
        filtered_df,
        locations='state',  # Must match format used in your data
        locationmode='USA-states',  # assumes 2-letter state codes like 'CA', 'NY'
        color='price',  # Update this to your actual column name if different
        scope='usa',
        color_continuous_scale='Reds',
        labels={'price': 'Price (cents/kWh)'},
        title=f"Residential Electricity Prices - {selected_year}"
    )
    fig.update_layout(
        geo=dict(bgcolor='#0c2d3e'),
        paper_bgcolor='#0c2d3e',
        font_color='white'
    )
    return fig
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
