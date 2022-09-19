from xml.dom.minidom import Childless
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from PIL import Image
import numpy as np
import os
import pysd

app = Dash(__name__)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

model = pysd.read_vensim('teacup.mdl')

stocks = model.run()

#df = pd.DataFrame({
#    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#    "Amount": [4, 1, 2, 2, 4, 5],
#    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
#})

fig = px.scatter(stocks, y="Teacup Temperature")

app.layout = html.Div(children=[
    html.H1(children="CampinaDS - Estimador de esforço para projetos de software"),
   
    html.Div(children='''CampinaDS: Um estimador de esforço para projetos de software com DS e PLN ''' ),
    html.Hr(),
    
    html.H2(children="Diagrama DS"),
   
    html.Img(src=app.get_asset_url("teacup.png"), alt="Uma Imagem"),
    html.Hr(),

    html.H2(children="Cenários"),
    html.P("Escolha um cenário (obs: os cenários carregam parâmetros pré definidos)"), 
    html.Div([
    dcc.Dropdown(['Pressionar a equipe para entregar na metade do prazo', 'Evitar o burnout', 'Economizar o máximo possível'], 'Pressionar a equipe para entregar na metade do prazo', id='demo-dropdown'),
    html.Div(id='dd-output-container')
    ]),
    html.Br(),
    html.Button("Carregar cenários", id="carregar", n_clicks=0),
    html.Hr(),

    html.H2(children="Documentação"),
    html.P("Carregue aqui toda  documentação do projeto. Exemplo: termo de abertura, descrição dos casos de uso. A documentação auxilia no ajuste dos parâmetros"), 
    html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    ]),
    html.Br(),
    html.Button("Carregar documentação", id="carregar_doc", n_clicks=0),
    html.Hr(),

    html.H2(children="Parametrização"),
    html.P("Informe a temperatura inicial da sala (Room Temperature)"),
    dcc.Input(id="1", type="text"),
    html.Br(),
    
    html.Br(),
    html.Button("Simular", id="submit-val", n_clicks=0),   

    html.Br(),
    
    html.Hr(),
    html.H2(children="Conclusões - Gráficos"),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    
    html.Hr(),
    html.H2(children="Conclusões - Narrativas"),
    html.P("Data Prevista de Entrega: Agosto 2024"),
    html.P("Custo do Projeto: R$ 200.000"),
])

if __name__ == '__main__':
    app.run_server(debug=True)
