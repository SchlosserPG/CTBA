from dash import Dash, html

app = Dash()

#2 main components for dash app, layout and callbacks

#app.layout = html.Div("My Dashboard")

#adjust the layout to include a title and a paragraph
app.title = "My First Dash App"
app.layout = html.Div([
    html.H1("Hello Dash", style={'color': '#381D5C', 'fontSize': '20px', "backgroundColor": '#E898AA'}),
    html.P("This is a simple dashboard.", style={'border': '1px solid black', 'padding': '20px', "margin": '50px'}),
    html.Br(),
    html.A("Click here", href="https://example.com"),
])


#then run the server
#check whether we are running the script directly
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)  # use_reloader=False to avoid double callbacks during development
##when putting the apps to production, set debug=False
##debug=True enables hot reloading, so you can see changes without restarting the server
##When you run the code, it will start a local server and you can access the app in your web browser because debug is set to TRUE
#You will see a debug menu on the browser. 


##Loaded on the http://localhost:8050/
#Notice that it says that Dash is running on http://127.0.0.1:8050/ below when you run the code. 

##Push control + C to stop the server when you are done testing the app.


