# docs/MultiLayout.py
import dash
from dash import html, dcc, Output, Input, callback
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests
import math
import dash_bootstrap_components as dbc

# ---------- Public API helper (Open-Meteo) ----------
CITY_COORDS = {
    "Williamsburg": (37.2707, -76.7075),
    "Richmond": (37.5407, -77.4360),
    "Virginia Beach": (36.8529, -75.9780),
    "Roanoke": (37.27097, -79.94143),
    "Charlottesville": (38.0293, -78.4767),
}

dash.register_page(__name__, path="/weather", name="Open-Meteo Dashboard", order=6, external_stylesheets=[dbc.themes.BOOTSTRAP])


def fetch_hourly_temp(lat: float, lon: float) -> pd.DataFrame:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m&forecast_days=2&timezone=auto"
    )
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    data = r.json()["hourly"]
    df = pd.DataFrame({"time": data["time"], "temp_C": data["temperature_2m"]})
    df["time"] = pd.to_datetime(df["time"])
    return df

# ---------- Layout: Multi-column grid ----------
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("Open-Meteo Dashboard", className="ms-2"),
            html.Span("Public API • Multi-column layout", className="text-muted"),
        ]
    ),
    color="dark",
    className="mb-4",
)

controls = dbc.Card(
    [
        dbc.CardHeader("Controls"),
        dbc.CardBody(
            [
                dbc.Label("City"),
                dcc.Dropdown(
                    id="city-dd",
                    options=[{"label": k, "value": k} for k in CITY_COORDS.keys()],
                    value="Williamsburg",
                    clearable=False,
                ),
                html.Br(),
                dbc.Button("Refresh", id="refresh", n_clicks=0, className="w-100"),
                html.Hr(),
                html.Small("Data source: open-meteo.com (no API key required).", className="text-muted"),
            ]
        ),
    ],
    className="mb-3",
)

def kpi_card(title, id_):
    return dbc.Card(
        dbc.CardBody([html.H6(title, className="text-muted mb-1"), html.H3(id=id_, className="mb-0")]),
        className="h-100",
    )

kpi_row = dbc.Row(
    [
        dbc.Col(kpi_card("Current Temp (°C)", "kpi-now"), width=4, class_name="buttonsmb-4"),
        dbc.Col(kpi_card("Min (°C/48h)", "kpi-min"), width=4, class_name="buttonsmb-4"),
        dbc.Col(kpi_card("Max (°C/48h)", "kpi-max"), width=4, class_name="buttonsmb-4"),
    ],
    className="mb-5",
)

chart_card = dbc.Card(
    [
        dbc.CardHeader("Hourly Temperature (next 48h)"),
        dbc.CardBody(dcc.Graph(id="temp-chart", config={"displayModeBar": False}))
    ],
    className="mb-6"
)

table_card = dbc.Card([dbc.CardHeader("Summary Stats"), dbc.CardBody(html.Div(id="stats-table"))], className="g-3")

layout = dbc.Container(
    [
        navbar,
        dbc.Row(
            [
                dbc.Col(controls, md=3),
                dbc.Col([kpi_row, chart_card], md=6),
                dbc.Col(table_card, md=3),
            ],
            className="g-3",
        ),
        html.Footer(html.Small("Built with Dash + dash-bootstrap-components • Row/Col grid", className="text-muted"),
                    className="mt-4"),
    ],
    fluid=True,
)

# ---------- Callbacks (bind to the global app) ----------
@callback(
    Output("temp-chart", "figure"),
    Output("kpi-now", "children"),
    Output("kpi-min", "children"),
    Output("kpi-max", "children"),
    Output("stats-table", "children"),
    Input("city-dd", "value"),
    Input("refresh", "n_clicks"),
)
def update(city, _):
    lat, lon = CITY_COORDS[city]
    df = fetch_hourly_temp(lat, lon)

    now = df.iloc[0]["temp_C"]
    tmin = df["temp_C"].min()
    tmax = df["temp_C"].max()

    fig = px.line(df, x="time", y="temp_C", markers=True, title=None)
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10),
                      yaxis_title="°C", xaxis_title="Time")

    summary = (
        df.assign(Date=df["time"].dt.date)
        .groupby("Date")["temp_C"]
        .agg(["min", "max", "mean"])
        .round(1)
        .rename(columns={"min": "Min °C", "max": "Max °C", "mean": "Avg °C"})
        .reset_index()
    )
    table = dbc.Table.from_dataframe(summary, striped=True, bordered=False, hover=True)

    fmt = lambda x: f"{x:.1f}"
    return fig, fmt(now), fmt(tmin), fmt(tmax), table

