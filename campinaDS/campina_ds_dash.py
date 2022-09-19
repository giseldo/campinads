from msilib.schema import Component
from xml.dom.minidom import Childless
from dash import Dash, html, dcc, Input, Output, State, dash_table
import plotly.express as px
import pandas as pd
from PIL import Image
import numpy as np
import os
import pysd
import io
import base64
import datetime
from urllib.parse import quote as urlquote
from docx2python import docx2python

app = Dash(__name__)

img_name = app.get_asset_url("ds.png")

os.chdir(os.path.dirname(os.path.abspath(__file__)))

model = pysd.read_vensim('v1.mdl')
#model = pysd.load("v1.py")

stocks = model.run()
fig_development = px.scatter(stocks, y="development software")
#fig_requirements = px.scatter(stocks, y="requirements")


#def new_soft_dev_rate():
#    return 2

#model.set_components({'software development rate': new_soft_dev_rate})

app.layout = html.Div(children=[
    
    html.H1("CampinaDS - Um sistema de apoio à decisão baseado em modelagem e simulação"),
    html.Div('''Um sistema de apoio à decisão baseado em modelagem e simulação (SADMS) são modelos
    formais, ou micromundos, em que os tomadores de decisão podem simular e testar as
    consequências decisões complexas, arriscadas ou onerosas no mundo real.'''),
    html.Br(),
    html.Div('''O CampinaDS é um SADMS para auxiliar o gerente de projeto na tomada de decisão
    analisando o impacto de suas decisões no esforço (estiva de prazo/cronograma/data de entrega) de projetos de software. 
    ''' ),
    html.Br(),
    html.Div('''O CampinaDS utiliza Dinâmica de Sistemas (DS), Machine Learning(ML) e Processamento de Linguagem Natural (PLN)) 
    para esse objetivo (reduzir custo, poupar tempo, de forma interpretável).'''),
    html.Br(),
    html.Div('''O CampinaDS também utiliza o PySD que é uma biblioteca para executar modelos de DS em python
    com o propósito de facilitar a integração com Big Data e ML no workflow do SD. O PySD traduz modelos 
    Vensim ou XMILE para arquivos com código fonte em python, e disponibiliza métodos para modificar, 
    simular e observar a execução dos modelos. '''),

    html.Br(),
    html.Hr(),
    
    html.H2(children="Diagrama DS"),
   
    html.Img(src=img_name, alt="Uma Imagem"),
    html.Hr(),

    #html.H2(children="Cenários"),
    #html.P("Escolha um cenário (obs: os cenários carregam parâmetros pré definidos)"), 
    #html.Div([
    #dcc.Dropdown(['Pressionar a equipe para entregar na metade do prazo', 'Evitar o burnout', 'Economizar o máximo possível'], 'Pressionar a equipe para entregar na metade do prazo', id='demo-dropdown'),
    #html.Div(id='dd-output-container')
    #]),
    #html.Br(),
    #html.Button("Carregar cenários", id="carregar", n_clicks=0),
    #html.Hr(),

    html.H2(children="Documentação"),
    html.P("Carregue aqui toda  documentação do projeto. Exemplo: termo de abertura, descrição dos casos de uso. A documentação auxilia no ajuste dos parâmetros"), 
    
    html.Div(
    [
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag and drop or click to select a file to upload."]
            ),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=True,
        ),
        html.H4("Lista de arquivos"),
        html.Ul(id="file-list"),
    ],
    style={"max-width": "500px"},
    ),
    

    html.Br(),
    html.Button("Carregar documentação", id="carregar_doc", n_clicks=0),
    html.Hr(),

    html.H2(children="Parametrização"),
    # nominal productivity
    html.P("Informe a produtividade nominal (nominal productivity):"),
    dcc.Input(
        id="nominal-productivity-input", 
        type="text",
        value=3),
    html.Br(),
    # quantidade de telas
    html.P("Informe a quantidade de telas:"),
    dcc.Input(
        id="quantidade-telas-input", 
        type="text",
        value=100),
    html.Br(),

    html.Br(),
    html.Button("Simular", id="submit-val", n_clicks=0),   

    html.Br(),
    
    html.Hr(),
    html.H2(children="Conclusões - Narrativas"),
    html.P("Quantidade de dias previsto para a finalização do projeto:"),
    html.Div(id="data-entrega-input"),

    html.Hr(),
    html.H2(children="Conclusões - Gráficos"),
    html.Div([
        dcc.Graph(id='graf-development-software', figure=fig_development)
    ]),
    
    #html.Div([
    #    dcc.Graph(id='graf-development-requirements', figure=fig_requirements)
    #]),

    
    #html.P("Custo do Projeto: R$ 200.000"),

    #html.H6("Change the value in the text box to see callbacks in action!"),
    #html.Div([
    #    "Input: ",
    #    dcc.Input(id='my-input', value='initial value', type='text')
    #]),
    #html.Br(),
    #html.Div(id='my-output'),
])

@app.callback(
    Output(component_id="graf-development-software", component_property="figure"),
    Output(component_id="data-entrega-input", component_property="children"),
    Input(component_id="submit-val", component_property="n_clicks"),
    State('nominal-productivity-input', 'value'),
    State('quantidade-telas-input', 'value')
)
def update_graph(n_clicks, input1, input2):
    stocks = model.run(params={
        'nominal productivity':int(input1),
        'quantidade de telas':int(input2)
        })
    qtd_dias = 0
    count = 0
    for i in stocks["requirements"]:
        count = count + 1
        if i<0: 
            break
    qtd_dias = count
    fig_development = px.scatter(stocks, y="development software")
    return fig_development, qtd_dias

UPLOAD_DIRECTORY = "docs"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files

def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)


@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]

if __name__ == '__main__':
    app.run_server(debug=True)
