import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import ThemeSwitchAIO # Serve para mudar o tema do dash


# ========= App ============== #
FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"] # Para trazer os icones 
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css" # Auxiliar na troca de tema do dash 

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc_css])
app.scripts.config.serve_locally = True
server = app.server

print(FONT_AWESOME)
# ========== Styles ============ #

template_theme1 = "flatly"
template_theme2 = "vapor"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.VAPOR

tab_card={'height': '100%'}

# ===== Reading n cleaning File ====== #
df_main = pd.read_csv("data_gas.csv")

df_main.info()

df_main['DATA INICIAL'] = pd.to_datetime(df_main['DATA INICIAL'])
df_main['DATA FINAL'] = pd.to_datetime(df_main['DATA FINAL'])

df_main['DATA MEDIA'] = ((df_main['DATA INICIAL'] - df_main['DATA FINAL'])/2) + df_main['DATA INICIAL']
df_main = df_main.sort_values(by='DATA MEDIA', ascending=True) #Ordenando o dataframe pela data média da menor para maior 
df_main.rename(columns= {'DATA MEDIA': 'DATA'}, inplace=True) # O inplace serve para alterar o df_main original 
df_main.rename(columns={'PREÇO MÉDIO REVENDA': 'VALOR REVENDA R$/L'}, inplace=True)

df_main['ANO'] = df_main['DATA'].apply(lambda x: str(x.year)) # Criando uma coluna ano e com data no ano da coluna DATA

df_main = df_main[df_main.PRODUTO == 'GASOLINA COMUM'] # Selecionando na coluna produto apenas dos casos de GASOLINA COMUM
df_main = df_main.reset_index()

df_main.drop(['UNIDADE DE MEDIDA', 'COEF DE VARIAÇÃO REVENDA','COEF DE VARIAÇÃO DISTRIBUIÇÃO', 
              'NÚMERO DE POSTOS PESQUISADOS', 'DATA INICIAL', 'DATA FINAL', 'PREÇO MÁXIMO DISTRIBUIÇÃO',
              'DESVIO PADRÃO DISTRIBUIÇÃO', 'MARGEM MÉDIA REVENDA', 'PREÇO MÍNIMO REVENDA', 'PREÇO MÁXIMO REVENDA',
              'PRODUTO', 'PREÇO MÉDIO DISTRIBUIÇÃO', 'DESVIO PADRÃO REVENDA','PREÇO MÍNIMO DISTRIBUIÇÃO'], inplace=True, axis=1) #axis=1 signiifica que está sendo exluido na vertical e não na horizontal

df_store = df_main.to_dict() #Transformando o daframe em dicionario 

# =========  Layout  =========== #
#Todo o layout está envolvido por um container
app.layout = dbc.Container(children=[
    #Armazenar o dataset
    dcc.Store(id='dataset', data=df_store), 
    dcc.Store(id='dataset_fixed', data=df_store),
    #Layout
    #Row 1
    #Sempre é necessario especificar as linhas e dentros das linhas conter as colunas e dentro das colunas inserimos o conteúdo
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend("Gas Prices Analytics")
                        ], sm=8), #Significa que são ocupadas 8 posições dessas colunas 
                        dbc.Col([
                            html.I(className='fa-fa-filter', style={'font-size': '300%'})
                        ], sm=4, align="center")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
                            html.Legend("Davi Garcia")
                        ])
                    ], style={'margin-top':'10px'}),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Meu LinkedIn", href="https://www.linkedin.com/in/davi-nascimento-garcia/", target="_blank")
                        ])
                    ], style={'margin-top':'10px'})
                ])
            ], style=tab_card)
        ], sm=4, lg=2)

    ])
], fluid=True, style={'height': '100%'})


# ======== Callbacks ========== #


# Run server
if __name__ == '__main__':
    app.run_server(debug=True)
