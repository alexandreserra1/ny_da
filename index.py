from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

# Componentes
from app import app
from _map import *
from _histogram import *
from _controllers import *
import os
from pathlib import Path
import dotenv

# =======================================
# Data Ingestion 
# =================================================================
# Primeiro carregamos os dados
df_data = pd.read_csv("dataset/cleaned_data.csv", index_col=0)

# Depois fazemos o processamento inicial
mean_lat = df_data["LATITUDE"].mean()
mean_long = df_data["LONGITUDE"].mean()

df_data["size_m2"] = df_data["GROSS SQUARE FEET"] / 10.764
df_data = df_data[df_data["YEAR BUILT"] > 0]
df_data["SALE DATE"] = pd.to_datetime(df_data["SALE DATE"])

# Tratamento dos dados
df_data.loc[df_data["size_m2"] > 10000, "size_m2"] = 10000
df_data.loc[df_data["SALE PRICE"] > 50000000, "SALE PRICE"] = 50000000
df_data.loc[df_data["SALE PRICE"] < 100000, "SALE PRICE"] = 100000

# Agora sim definimos o slider_size
slider_size = {
    100: df_data["GROSS SQUARE FEET"].quantile(0.1),
    500: df_data["GROSS SQUARE FEET"].quantile(0.25),
    1000: df_data["GROSS SQUARE FEET"].quantile(0.5),
    10000: df_data["GROSS SQUARE FEET"].quantile(0.75),
    'max': df_data["GROSS SQUARE FEET"].max()
}

# Print para debug
print("\nValores dos quartis em pés quadrados:")
for key, value in slider_size.items():
    print(f"Marca {key}: {value:.2f} ft² ({value/10.764:.2f} m²)")

# Constantes no início do arquivo
MAX_SIZE_M2 = 10000
MAX_SALE_PRICE = 50000000

# Função para tratar outliers
def treat_outliers(df):
    df.loc[df['size_m2'] > MAX_SIZE_M2, 'size_m2'] = MAX_SIZE_M2
    df.loc[df['SALE PRICE'] > MAX_SALE_PRICE, 'SALE PRICE'] = MAX_SALE_PRICE
    return df

# Carregar as variáveis de ambiente de forma explícita
dotenv_path = Path('.env')
dotenv.load_dotenv(dotenv_path=dotenv_path)

# Função para mascarar a chave API
def mask_api_key(key):
    if key:
        return key[:8] + "..." + key[-4:]
    return None

# Debugar
print("Diretório atual:", os.getcwd())
print("Arquivos no diretório:", os.listdir())
print("Caminho do .env existe?", dotenv_path.exists())
print("Conteúdo do .env: [CHAVE API OCULTA]")
print("Valor da MAPBOX_API_KEY:", mask_api_key(os.getenv('MAPBOX_API_KEY')))

# Pegar a chave da api do Mapbox
mapbox_api_key = os.getenv('MAPBOX_API_KEY')

# Verificação da chave API
if not mapbox_api_key:
    raise ValueError("MAPBOX_API_KEY não encontrada nas variáveis de ambiente")

# Configuração única do token
px.set_mapbox_access_token(mapbox_api_key)

# ===============================
# Data injection
# ===============================

# Load data
df_data = pd.read_csv('dataset/cleaned_data.csv', index_col=0)

# Fazer a média das coordenadas de latitude e longitude
mean_lat = df_data['LATITUDE'].mean()
mean_long = df_data['LONGITUDE'].mean()

# Tratar os dados - Nos eua eles usam pé quadrado ao contrario do Brasil
# Precisa calcular para metros quadrados
df_data['size_m2'] = df_data['GROSS SQUARE FEET'] / 10.764

#Tirar fora os apts que nao tem o ano definido
df_data = df_data[df_data['YEAR BUILT'] > 0]

# pré processamento - transformar a data em datetime
df_data['SALE DATE'] = pd.to_datetime(df_data['SALE DATE'])

# Tratar os outliers
df_data = treat_outliers(df_data)

# Se você precisa filtrar datas muito antigas, use uma data específica:
data_minima = pd.to_datetime('2000-01-01')
df_data = df_data[df_data['SALE DATE'] >= data_minima]

# Print para debug - você pode remover depois
print("\nValores dos quartis em pés quadrados:")
for key, value in slider_size.items():
    print(f"Marca {key}: {value:.2f} ft² ({value/10.764:.2f} m²)")

# ===============================
# Layout
# ===============================
app.layout = dbc.Container(
        children=[
                dbc.Row([
                        dbc.Col([
                                controllers
                        ], md=3, style={
                                "padding-right": "25px",
                                "padding-left": "25px", 
                                "padding-top": "50px",
                                "background-color": "#111111",  # Fundo escuro
                                "min-height": "100vh"  # Altura total da viewport
                        }),
                        
                        dbc.Col([
                                map,
                                hist
                        ], md=9, style={
                                "background-color": "#111111",  # Fundo escuro
                                "min-height": "100vh"  # Altura total da viewport
                        }),
                ], className="g-0")  # Remove o gap entre colunas
        ], fluid=True, 
        style={
                "background-color": "#111111",  # Fundo escuro
                "min-height": "100vh",  # Altura total da viewport
                "padding": "0",  # Remove padding do container
                "color": "white"  # Texto em branco
        })


# ===============================
# Callbacks
# ===============================

# Callback para atualizar o histograma
@app.callback(
        [Output('hist-graph', 'figure'),
        Output('map-graph', 'figure')],
        [Input('location-dropdown', 'value'),
        Input('slider-square-size', 'value'),
        Input('dropdown-color', 'value')]
)
# Função para atualizar o histograma
def update_hist(location, square_size, color_map): # location tem que ser um numero
        # Inicializa com todos os dados
        df_intermediate = df_data.copy()
        
        # Aplica filtros apenas se eles existirem
        if location is not None and location != 0:
                df_intermediate = df_intermediate[df_intermediate["BOROUGH"] == location]
        
        if square_size is not None:
                # Mapeamento dos valores do slider para as chaves do slider_size
                slider_values = {
                        0: 100,    # 10%
                        1: 500,    # 25%
                        2: 1000,   # 50%
                        3: 10000,  # 75%
                        4: 'max'   # 100%
                }
                size_key = slider_values[square_size]
                size_limit = slider_size[size_key]
                df_intermediate = df_intermediate[df_intermediate["GROSS SQUARE FEET"] <= size_limit]

        # Plotar o histograma com estilo mais escuro
        hist_fig = px.histogram(df_intermediate, x=color_map, opacity=0.75)
        hist_layout = go.Layout(
            margin=go.layout.Margin(l=10, r=0, t=0, b=50),
            showlegend=False, 
            template="plotly_dark", 
            paper_bgcolor="rgba(0, 0, 0, 0)",
            plot_bgcolor="rgba(0, 10, 00, 0.1)",  # Cinza mais escuro
            xaxis_title="",
            yaxis_title="",
            xaxis=dict(
                showgrid=True,
                gridcolor="rgba(128, 128, 128, 0.2)",
                color="white"
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(128, 128, 128, 0.2)",
                color="white",
                rangemode='nonnegative',  # Isso remove o zero à esquerda
                showline=False,  # Remove a linha do eixo y
                zeroline=False   # Remove a linha do zero
            ),
            bargap=0.05,
            bargroupgap=0.1
        )
        
        # Atualiza as cores e estilo das barras
        hist_fig.update_traces(
            marker=dict(
                # Opção 1: Verde suave e transparente
                #color='rgba(102, 204, 153, 0.4)',  # Verde claro com 60% de transparência
                
                # OU Opção 2: Azul suave e transparente
                 #color='rgba(100, 149, 237, 0.4)',  # Azul cornflower com 60% de transparência
                
                # OU Opção 3: Verde-água transparente
                color='rgba(127, 255, 212, 0.4)',  # Aquamarine com 60% de transparência
                
                line=dict(
                    # Borda um pouco mais escura e menos transparente
                    color='rgba(102, 204, 153, 0.8)',  # Mesma cor, menos transparente
                    width=1
                )
            ),
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            )
        )
        
        hist_fig.layout = hist_layout
        
        # Recarregar a chave do Mapbox dentro do callback
        px.set_mapbox_access_token(mapbox_api_key)
        
        # Plotar o mapa
        map_fig = px.scatter_mapbox(df_intermediate, 
                               lat="LATITUDE", 
                               lon="LONGITUDE", 
                               color=color_map, 
                               size="size_m2", 
                               size_max=20, 
                               zoom=9,  # Reduzimos um pouco o zoom para ver área maior
                               opacity=0.4)
        
        map_fig.update_layout(
            mapbox=dict(
                center=go.layout.mapbox.Center(
                    lat=40.7128,  # Latitude central de NYC
                    lon=-74.0060  # Longitude central de NYC
                ),
                style='dark',
                zoom=9.5  # Ajuste fino do zoom
            ), 
            template="plotly_dark", 
            paper_bgcolor="rgba(0, 0, 0, 0)", 
            margin=go.layout.Margin(l=0, r=0, t=0, b=0),  # Removemos as margens
        )
        
        # variação quantis para o mapa - Os quantis são valores que dividem um conjunto de dados em partes iguais.
        # Aplicar a variação quantis para o mapa 
        color_scale = px.colors.sequential.GnBu
        df_quantiles = df_data[color_map].quantile(np.linspace(0, 1, len(color_scale))).to_frame()
        df_quantiles = round((df_quantiles - df_quantiles.min()) / (df_quantiles.max() - df_quantiles.min()) * 10000) / 10000
        df_quantiles.iloc[-1] = 1
        df_quantiles["colors"] = color_scale
        df_quantiles.set_index(color_map, inplace=True)
        color_scale = [[i, j] for i, j in df_quantiles["colors"].items()]
        
        map_fig.update_coloraxes(colorscale=color_scale)
        
        # Atualizar o histograma
        return hist_fig, map_fig

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(host='0.0.0.0', port=8050, debug=True)