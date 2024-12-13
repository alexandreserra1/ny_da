import dash
import dash_bootstrap_components as dbc

# App 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
# Server
server = app
# Serve locally
app.scripts.config.serve_locally = True
# Run app
server = app.server
