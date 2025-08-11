from dash import Dash, html

app= Dash()

# The layout can include a single component (string, number, or element) or a list of components
app.layout = html.Div([
    html.H1("World Happiness Dashboard"),
    html.P("This dashboard visualizes world happiness score."),
    html.Br(),
    html.A("World Happiness Report", 
       href="https://worldhappiness.report/", 
       target="_blank", 
       style={'color': "#6065a3", 'textDecoration': 'underline'})

])

# Run the server
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)  


