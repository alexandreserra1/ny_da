from dash import html, dcc
import dash_bootstrap_components as dbc
from app import app


list_of_locations = {
    "Todos": 0,
    "Manhattan": 1,
    "Bronx": 2,
    "Brooklyn": 3,
    "Queens": 4,
    "Staten Island": 5,
}

slider_size = [100, 500, 1000, 10000, 10000000]

controllers = dbc.Row([
                dcc.Store(id='store-global'),
                html.Img(
                    id="logo",
                    src=app.get_asset_url("Calcifer c_.jpg"),
                    style={
                        'width': '300px',
                        'height': 'auto',
                        'margin': '20px 0',
                        'display': 'block',
                        'border-radius': '10px',
                        'box-shadow': '0 4px 8px rgba(0,0,0,0.3)',
                        'opacity': '0.7',
                        'background-color': '#111111',
                        'object-fit': 'cover'
                    }
                ),
                html.H3("Vendas de imóveis - NYC", style={"margin-top": "20px"}),
                html.P(
                """Utilize este dashboard para analisar vendas ocorridas na 
                cidade de New York no período de 1 ano. """
                ),

                html.H4("""Distrito""", style={"margin-top": "50px", "margin-bottom": "20px"}),
                dcc.Dropdown(
                    id="location-dropdown",
                    options=[{"label": i, "value": j} for i, j in list_of_locations.items()],
                    value=0,
                    placeholder="Selecione um bairro"),

                html.P("""Metragem (m2)""", style={"margin-top": "20px"}),

                dcc.Slider(min=0, max=4, id='slider-square-size', value=4,
                marks = {i: str(j)for i, j in enumerate(slider_size)}),

                html.P("""Variável de análise""", style={"margin-top": "20px"}),
                
                dcc.Dropdown(
                    options=[
                        {'label': 'Ano de Construção', 'value': 'YEAR BUILT'},
                        {'label': 'Total de Unidades', 'value': 'TOTAL UNITS'},
                        {'label': 'Preço de Venda', 'value': 'SALE PRICE'},
                    ],
                    value='SALE PRICE',
                    id="dropdown-color")
    ])

    





