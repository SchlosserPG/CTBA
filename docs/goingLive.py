from dash import Dash, html, register_page

app = Dash(__name__)
server = app.server  # Required for Gunicorn in production

# William & Mary green palette
wm_green = "#115740"
wm_gold = "#B9975B"

register_page(
    __name__,
    path="/index",
    name="Home",
    order=0
)

layout = html.Div([
    html.H1("How to Deploy a Dash App to Render.com", style={"color": wm_green, "textAlign": "center"}),
    html.H2("1. Prepare your Dash app", style={"color": wm_green}),
    html.Ul([
        html.Li("Ensure server = app.server exists in your main Python file."),
        html.Li("Filename can be anything, but the start command must match it exactly."),
    ], style={"marginBottom": "20px"}),

    html.H2("2. Add required files", style={"color": wm_green}),
    html.Ul([
        html.Li("requirements.txt — list dependencies (e.g., dash, gunicorn, plotly)."),
    ], style={"marginBottom": "20px"}),

    html.H2("3. Run locally", style={"color": wm_green}),
    html.Pre("""python -m venv .venv
.venv\\Scripts\\activate    # Windows
pip install -r requirements.txt
python your_filename.py  # dev mode
gunicorn your_filename:server  # production test""", style={"backgroundColor": wm_gold, "padding": "10px", "borderRadius": "5px", "color": "white"}),

    html.H2("4. Push to GitHub", style={"color": wm_green}),
    html.Pre("""git init
git add .
git commit -m \"Initial commit\"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main""", style={"backgroundColor": wm_gold, "padding": "10px", "borderRadius": "5px", "color": "white"}),

    html.H2("5. Deploy on Render", style={"color": wm_green}),
    html.Ul([
        html.Li("Create a new Web Service."),
        html.Li("Connect your GitHub repo."),
        html.Li("In Settings, set the Build command to: pip install -r requirements.txt"),
        html.Li("In Settings, set the Start command to: gunicorn your_filename:server"),
        html.Li(html.Span(["Deploy and open the provided URL, e.g. ", html.A("Example App", href="https://ctba-oror.onrender.com/", target="_blank", style={"color": wm_green, "textDecoration": "underline"})])),
    ], style={"marginBottom": "20px"}),

    html.H2("6. Troubleshooting", style={"color": wm_green}),
    html.Ul([
        html.Li("ModuleNotFoundError: Ensure start command matches your filename exactly."),
        html.Li("Clear build cache and redeploy if changes don't take effect."),
        html.Li("Confirm all dependencies are listed in requirements.txt."),
        html.Li(html.Span(["For Render docs, visit ", html.A("Render Help Center", href="https://render.com/docs", target="_blank", style={"color": wm_green, "textDecoration": "underline"})])),
    ], style={"marginBottom": "20px"})
], style={"maxWidth": "800px", "margin": "auto", "fontFamily": "Arial, sans-serif"})

# App layout
app.layout = layout 


if __name__ == "__main__":
    app.run(debug=True)