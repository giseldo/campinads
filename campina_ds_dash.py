from dash import Dash, html, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os
import pysd
import io
import base64
import datetime
from urllib.parse import quote as urlquote
from docx2python import docx2python
import docx2txt

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

EXTERNAL_STYLESHEETS = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
img_name = app.get_asset_url("ds.png")
os.chdir(os.path.dirname(os.path.abspath(__file__)))
model =  pysd.read_xmile("modelo/brook_law.xmile")
#model = pysd.load("modelo/brook_law.xmile.py")
stocks = model.run()

fig_development = px.scatter(stocks, y="developed software", labels={'x':'dias', 'y':'developed software'})
fig_software_developement_rate = px.scatter(stocks, y="software development rate", labels={'x':'dias', 'y':'software development rate'})

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

NAVBAR = dbc.Navbar(
    children=[
        
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(
                        dbc.NavbarBrand("Campina DS", className="ml-2")
                    ),
                    dbc.Col(
                        dbc.NavItem(dbc.NavLink("Sobre", href="")),
                    )
                ],
                align="center",
                
            ),
            href="https://plot.ly"
        ), 
        
    ],
    color="dark",
    dark=True,
    sticky="top"
)

TOP_DS = [
    dbc.CardHeader(html.H5("Modelo DS com Brooks law Effect")),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col([html.Img(src=img_name)]),
                ]
            )
        ]
    )
]

PARAMETROS = [
    dbc.CardHeader(html.H5("Parâmetros")),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H6("Informe a produtividade nominal (nominal productivity):"),
                            dcc.Input(id="nominal-productivity-input", type="text", value=0.1), 
                            html.H6("Informe a quantidade de novos funcionários caso o projeto atrase (personnel new hire): "),
                            dcc.Input(id="quantidade-new-personnel-input", type="text", value=0),
                            html.H6("Dica: Teste  os valores ""0"", ""5"" e ""10"" para ""personnel new hire"" e acompanhe o gráfico do ""software development rate"" "),
                            html.Button("Simular", id="submit-val", n_clicks=0),   
                            html.Br(),
                        ]
                    ),
                ]
            )
        ]
    )
]

TEXTOS = [
    dbc.CardHeader(html.H5("Resumo")),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H6("Quantidade de dias previsto para a finalização do projeto:"),
                            html.Div(id="data-entrega-output"), 
                            html.H6("produtividade nominal:"),
                            html.Div(id="nominal-productivity-output"), 
                            html.H6("quantidade de novos funcionários caso o projeto atrase:"),
                            html.Div(id="quantidade-new-personnel-output"), 
                        ]
                    ),
                ]
            )
        ]
    )
]

GRAFICOS = [
    dbc.CardHeader(html.H5("Gráficos")),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H2(children="Conclusões - Gráficos"),
                            dcc.Tabs(
                                id="tabs-with-classes",
                                children=[
                                    dcc.Tab(label='Developed software', children=[dcc.Graph(id='graf-development-software'),]),
                                    dcc.Tab(label='software development rate', children=[dcc.Graph(id='graf-software-development-rate'),])
                                ]),
                        ]
                    ),
                ]
            )
        ]
    )
]

BODY = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card(TOP_DS)),], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(PARAMETROS)),], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(TEXTOS)),], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(GRAFICOS)),], style={"marginTop": 30}),
    ]
)

app.layout = html.Div(children=[NAVBAR, BODY])

    #html.H1("CampinaDS - Um sistema de apoio à decisão baseado em modelagem e simulação"),
    #html.Div('''Um sistema de apoio à decisão baseado em modelagem e simulação (SADMS) são modelos
    #formais, ou micromundos, em que os tomadores de decisão podem simular e testar as
    #consequências decisões complexas, arriscadas ou onerosas no mundo real.'''),
    #html.Br(),
    #html.Div('''O CampinaDS é um SADMS para auxiliar o gerente de projeto na tomada de decisão
    #analisando o impacto de suas decisões no esforço (estiva de prazo/cronograma/data de entrega) de projetos de software. 
    #''' ),
    #html.Br(),
    #html.Div('''O CampinaDS utiliza Dinâmica de Sistemas (DS), Machine Learning(ML) e Processamento de Linguagem Natural (PLN)) 
    #para esse objetivo (reduzir custo, poupar tempo, de forma interpretável).'''),
    #html.Br(),
    #html.Div('''by Giseldo'''),

    
    
    #html.H2("Documentação"),
    #html.P('''Carregue aqui toda  documentação do projeto. Exemplo: termo de abertura, 
    #descrição dos casos de uso. A documentação auxilia no ajuste dos parâmetros'''), 
    #html.P('''obs: somente o documento do tipo "prototipo de telas" está sendo compreendido e processado, ele conta 
    #quantas imagens tem o documento e atualiza o parâmetro "quantidade de telas" (carregue um documento com várias imagens para teste)'''), 
    #html.Div([dcc.Upload(id="upload-data",children=html.Div(["Drag and drop or click to select a file to upload."]),
    #        style={"width": "100%", "height": "60px","lineHeight": "60px","borderWidth": "1px","borderStyle": "dashed",
    #            "borderRadius": "5px", "textAlign": "center", "margin": "10px",}, multiple=True,
    #    ), html.H4("Lista de arquivos"), html.Ul(id="file-list"),],style={"max-width": "500px"},),
    #html.Br(),
    #html.Button("Carregar documentação", id="submit-doc", n_clicks=0),  html.Hr(),
    
    #html.H2(children="Parametrização"),
    # nominal productivity
    #html.P("Informe a produtividade nominal (nominal productivity):"),
    #dcc.Input(id="nominal-productivity-input", type="text", value=0.1), html.Br(),
    # quantidade de telas
    #html.P("Informe a quantidade de novos funcionários caso o projeto atrase:"),
    #dcc.Input(id="quantidade-new-personnel-input", type="text", value=0),
    # submit
    #html.Br(), html.Br(),
    #html.Button("Simular", id="submit-val", n_clicks=0),   
    #html.Br(), html.Hr(),
    # graficos e textos
    #html.H2(children="Conclusões - Narrativas"),
    #html.P("Quantidade de dias previsto para a finalização do projeto:"),
    #html.Div(id="data-entrega-output"), 
    #html.P("produtividade nominal:"),
    #html.Div(id="nominal-productivity-output"), 
    #html.P("quantidade de novos funcionários caso o projeto atrase:"),
    #html.Div(id="quantidade-new-personnel-output"), 

    #html.H2(children="Conclusões - Gráficos"),
    
    #dcc.Tabs(
    #    id="tabs-with-classes",
    #    children=[
    #        dcc.Tab(label='Developed software', children=[dcc.Graph(id='graf-development-software'),]),
    #        dcc.Tab(label='software development rate', children=[dcc.Graph(id='graf-software-development-rate'),])
    #    ])
    
#])

#@app.callback(
#    Output(component_id="quantidade-telas-input", component_property="value"),
#    Input(component_id='submit-doc', component_property="n_clicks")
#)
#def update_quantidade_tela(n_clicks):
#    if n_clicks>0:
#        files = []
#        for filename in os.listdir(UPLOAD_DIRECTORY):
#            path = os.path.join(UPLOAD_DIRECTORY, filename)
#            doc_result = docx2python(path)
#            count = 0
#            for key, value in doc_result.images.items():
#                count = count + 1
#        return count
#    else:
#        return 150

@app.callback(
    Output(component_id="tabs-with-classes", component_property="children"),
    Output(component_id="data-entrega-output", component_property="children"),
    Output(component_id="nominal-productivity-output", component_property="children"),
    Output(component_id="quantidade-new-personnel-output", component_property="children"),
    Input(component_id="submit-val", component_property="n_clicks"),
    State('nominal-productivity-input', 'value'),
    State('quantidade-new-personnel-input', 'value')
)

def update_graph(n_clicks, input1, input2):
    stocks = model.run(params={
        "nominal productivity":float(input1),
        "personnel new hire":int(input2)        
        })
    qtd_dias = 0
    count = 0
    for req in stocks["requirements"]:
        count = count + 1
        if req<0: 
            break
    qtd_dias = count
    fig_development = px.scatter(stocks, y="developed software", labels={'x':'dias', 'y':'developed software'})
    fig_software_developement_rate = px.scatter(stocks, y="software development rate", labels={'x':'dias', 'y':'software development rate'})
    
    Output(component_id="tabs-with-classes", component_property="children"),
    tab_retorno = [
            dcc.Tab(label='Developed software', children=[dcc.Graph(id='graf-development-software', figure=fig_development),]),
            dcc.Tab(label='software development rate', children=[dcc.Graph(id='graf-software-development-rate', figure=fig_software_developement_rate),])
        ]
    
    return tab_retorno, qtd_dias, float(input1), int(input2)   

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
    return html.Div([
        html.A(filename, href=location),
        html.P("Documento identificado como um Protótipo de Tela")
    ])

#@app.callback(
#    Output("file-list", "children"),
#    [Input("upload-data", "filename"), Input("upload-data", "contents")],
#)
#def update_output(uploaded_filenames, uploaded_file_contents):
#    """Save uploaded files and regenerate the file list."""
#    if uploaded_filenames is not None and uploaded_file_contents is not None:
#        for name, data in zip(uploaded_filenames, uploaded_file_contents):
#           save_file(name, data)
#    files = uploaded_files()
#    if len(files) == 0:
#        return [html.Li("Sem arquivos carregados!")]
#    else:
#        return [html.Li(file_download_link(filename)) for filename in files]

if __name__ == '__main__':
    app.run_server(debug=True)
