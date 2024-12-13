from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


# ===============================
# Histograma
# ===============================
fig = go.Figure()

# Configuração do histograma
fig.update_layout(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)'
)

# Adicionar o histograma
hist = dbc.Row([ # Linha do histograma
    dcc.Graph( # Componente de gráfico
        id='hist-graph', # ID do histograma
        figure=fig, # Figura do histograma
    )
], style={'height': '20vh'}) # Altura do histograma
