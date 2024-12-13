# 🏢 Dashboard de Análise Imobiliária de Nova York

## 📋 Descrição
Este projeto é um dashboard interativo desenvolvido com Dash e Plotly que permite visualizar e analisar dados do mercado imobiliário de Nova York. O dashboard apresenta um mapa interativo e histogramas que mostram diferentes aspectos das propriedades, como preço de venda, tamanho e localização.

## ✨ Funcionalidades
- 🗺️ Mapa interativo com visualização geográfica das propriedades
- 📊 Histograma dinâmico para análise de distribuição
- 🎯 Filtros por:
  - Localização (Borough)
  - Tamanho do imóvel
  - Diferentes métricas de visualização

## 🛠️ Tecnologias Utilizadas
- Python 3.x
- Dash
- Plotly
- Pandas
- NumPy
- Dash Bootstrap Components
- Mapbox API

## 📦 Dependências
dash
dash-bootstrap-components
pandas
numpy
plotly
python-dotenv

## 🚀 Como Executar
bash
git clone [https://github.com/alexandreserra1/ny_da.git]
cd [NOME_DO_DIRETORIO]

### 1. Clone o repositório
```bash
git clone [URL_DO_SEU_REPOSITORIO]
cd [NOME_DO_DIRETORIO]
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto e adicione sua chave API do Mapbox:
```
MAPBOX_API_KEY=sua_chave_api_aqui
```

### 4. Execute a aplicação
```bash
python index.py
```

## 📊 Estrutura de Dados
O projeto utiliza um arquivo CSV (`cleaned_data.csv`) com as seguintes colunas principais:
- BOROUGH
- LATITUDE
- LONGITUDE
- GROSS SQUARE FEET
- SALE PRICE
- YEAR BUILT
- SALE DATE

## 🎨 Interface
- Design moderno com tema escuro
- Layout responsivo
- Visualizações interativas
- Controles intuitivos para filtros

## 🔧 Configurações Personalizáveis
- Limites de tamanho máximo: 10.000 m²
- Preço máximo de venda: $50.000.000
- Zoom do mapa centralizado em Nova York
- Esquemas de cores personalizáveis

## 📈 Recursos de Visualização
- Mapa de calor por diferentes métricas
- Histogramas interativos
- Filtros dinâmicos
- Tooltips informativos


## 🙏 Agradecimentos
- Mapbox pela API de mapas
- Fonte de dados imobiliários de Nova York