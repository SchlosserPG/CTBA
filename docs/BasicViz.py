import dash
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path



app = Dash(__name__)
server = app.server  

dash.register_page(__name__, path="/JobChanges", name="Live Job Changes", order=4)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "livedata-weekly-job-changes-2025-07-23.csv"

def load_data(path: Path) -> pd.DataFrame:
    print(f"Loading data from: {path}  Exists: {path.exists()}")
    if not path.exists():
        cols = [
            "arrival/departure",
            "previous_job.company.name",
            "previous_job.function",
            "current_job.started_at",
            "previous_job.ended_at",
        ]
        return pd.DataFrame(columns=cols)

    df = pd.read_csv(path)
    expected = {
        "arrival/departure": "arrival/departure",
        "previous_job.company.name": "previous_job.company.name",
        "previous_job.function": "previous_job.function",
        "current_job.started_at": "current_job.started_at",
        "previous_job.ended_at": "previous_job.ended_at",
    }
    missing = [c for c in expected if c not in df.columns]
    for c in missing:
        df[c] = pd.NA

    # Parse as UTC (tz-aware)
    df["current_job.started_at"] = pd.to_datetime(
        df["current_job.started_at"], errors="coerce", utc=True
    )
    df["previous_job.ended_at"] = pd.to_datetime(
        df["previous_job.ended_at"], errors="coerce", utc=True
    )

    # Vectorized pick: arrivals use started_at, departures use ended_at
    arrival_mask = df["arrival/departure"].eq("arrival")
    event_time = df["current_job.started_at"].where(arrival_mask, df["previous_job.ended_at"])

    # Drop tz before converting to period
    event_time_naive = event_time.dt.tz_localize(None)
    df["week"] = event_time_naive.dt.to_period("W").dt.start_time

    return df

df = load_data(DATA_PATH)
DEFAULT_TOP_N = 10



def fig_top_departure_companies(data: pd.DataFrame, top_n: int = DEFAULT_TOP_N):
    deps = data[data["arrival/departure"] == "departure"]
    vc = deps["previous_job.company.name"].dropna().value_counts().nlargest(top_n)
    plot_df = vc.rename_axis("Company").reset_index(name="Departures").sort_values("Departures")
    if plot_df.empty:
        return go.Figure().update_layout(
            title="Top Companies by Number of Departures",
            xaxis_title="Number of Departures",
            yaxis_title="Company",
            annotations=[dict(text="No data available", x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False)],
        )
    fig = px.bar(plot_df, x="Departures", y="Company", orientation="h")
    fig.update_layout(title=f"Top {top_n} Companies by Number of Departures", xaxis_title="Number of Departures", yaxis_title="Company", bargap=0.2)
    return fig

def fig_top_departure_functions(data: pd.DataFrame, top_n: int = DEFAULT_TOP_N):
    deps = data[data["arrival/departure"] == "departure"]
    vc = deps["previous_job.function"].dropna().value_counts().nlargest(top_n)
    plot_df = vc.rename_axis("Job Function").reset_index(name="Departures").sort_values("Departures")
    if plot_df.empty:
        return go.Figure().update_layout(
            title="Top Job Functions by Number of Departures",
            xaxis_title="Number of Departures",
            yaxis_title="Job Function",
            annotations=[dict(text="No data available", x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False)],
        )
    fig = px.bar(plot_df, x="Departures", y="Job Function", orientation="h")
    fig.update_layout(title=f"Top {top_n} Job Functions by Number of Departures", xaxis_title="Number of Departures", yaxis_title="Job Function", bargap=0.2)
    return fig

def fig_weekly_arrivals_vs_departures(data: pd.DataFrame):
    data_2025 = data[data["week"].dt.year == 2025]
    if data_2025.empty:
        return go.Figure().update_layout(
            title="Weekly Job Arrivals vs. Departures (2025)",
            xaxis_title="Week",
            yaxis_title="Count",
            annotations=[dict(text="No data available for 2025", x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False)],
        )
    wk = data_2025.groupby(["week", "arrival/departure"]).size().reset_index(name="count")
    pivot = wk.pivot(index="week", columns="arrival/departure", values="count").fillna(0).sort_index()
    tidy = pivot.reset_index().melt(id_vars=["week"], value_vars=list(pivot.columns), var_name="Type", value_name="Count")
    fig = px.line(tidy, x="week", y="Count", color="Type")
    fig.update_layout(title="Weekly Job Arrivals vs. Departures (2025)", xaxis_title="Week", yaxis_title="Number of Changes", legend_title="Type")
    return fig



top_n_options = [5, 10, 15, 20]

layout = html.Div(
    style={"padding": "20px", "maxWidth": "1100px", "margin": "0 auto"},
    children=[
        html.H1("Job Changes Dashboard", style={"textAlign": "center"}),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Top N"),
                        dcc.Dropdown(
                            id="top-n",
                            options=[{"label": str(n), "value": n} for n in top_n_options],
                            value=DEFAULT_TOP_N,
                            clearable=False
                        ),
                    ],
                    style={"flex": 1, "minWidth": 200},
                ),
                html.Div(
                    [html.Label("Data file"), html.Div(str(DATA_PATH), style={"opacity": 0.7})],
                    style={"flex": 2, "minWidth": 200, "paddingLeft": "16px"}
                ),
            ],
            style={
                "display": "flex",
                "flexWrap": "wrap",
                "gap": "12px",
                "alignItems": "end",
                "marginBottom": "16px",
            },
        ),
        dcc.Graph(id="companies-bar"),
        dcc.Graph(id="functions-bar"),
        dcc.Graph(id="weekly-line"),
        html.Div(id="data-warning", style={"marginTop": "8px", "color": "#8a6d3b"}),
    ],
)

@dash.callback(
    Output("companies-bar", "figure"),
    Output("functions-bar", "figure"),
    Output("weekly-line", "figure"),
    Output("data-warning", "children"),
    Input("top-n", "value"),
)
def update_figures(top_n):
    fig1 = fig_top_departure_companies(df, top_n)
    fig2 = fig_top_departure_functions(df, top_n)
    fig3 = fig_weekly_arrivals_vs_departures(df)
    warn = ("Data file not found — showing empty charts. Check the path: " + str(DATA_PATH)
            if df.empty else "")
    return fig1, fig2, fig3, warn
