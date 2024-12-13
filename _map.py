from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


# ===============================
# Mapa
# ===============================
fig = go.Figure()

# Configuração do mapa
fig.update_layout(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)'
)

# Adicionar o mapa
map = dbc.Row([ # Linha do mapa
    dcc.Graph( # Componente de gráfico
        id='map-graph', # ID do mapa
        figure=fig, # Figura do mapa
    )
], style={'height': '80vh'}) # Altura do mapa
