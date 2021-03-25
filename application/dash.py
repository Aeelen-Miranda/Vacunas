import dash
import matplotlib.pyplot as plt 
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
import numpy as np
import dash_table
import sidetable as stb
import datetime
from datetime import datetime, timedelta
from datetime import date
import geopandas as gpd
import flask
import os

yesterday = datetime.now() - timedelta(1)
yea = datetime.strftime(yesterday, '%Y%m%d')

today = date.today()
d2 = today.strftime("Fecha de actualización : %d-%m-%Y")

###############################
# DATABASES
############################### Abre archivos


#os.chdir(r"C:\Users\PRIME\AnacondaProjects\Project_curso\\")

vacunas = pd.read_csv("https://raw.githubusercontent.com/fdealbam/Vacunas/main/Arribo%20250321.csv", encoding= "Latin-1")
vacunas.rename(columns={'FarmacÃ©utica': 'Farmacéutica' },inplace=True,
                                   errors='ignore')
df = vacunas
Farmacéuticas = df.Farmacéutica.unique()

server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes. LUX], server=server)

body = html.Div([
# Cintillo 000
        dbc.Row(
           [
               dbc.Col(dbc.CardImg(src="https://github.com/fdealbam/Vacunas/blob/main/SALUD.JPG?raw=true"),
                        width=2, lg={'size': 3,  "offset": 1})]),
    dbc.Row(
        [    dbc.Col(html.H2("ARRIBO DE VACUNAS"),
                        lg={'offset' : 3 }),
              dbc.Col(html.H3("DIRECCIÓN GENERAL DE COMUNICACIÓN SOCIAL"),
                  width={'size' : 7,
                         'offset' : 3, 
                         'color' : 'danger'
                        }), 
                

            ],justify="start"),
        
# Top Banner

       html.Hr(),
    dbc.Row(
           [
               dbc.Col(html.H4(d2),           #Fecha de actualización
               width={'size' : "auto",
                      'offset' : 4}), 
           ]),
#Cintillo 00    
    dbc.Row(
           [dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x} for x in Farmacéuticas],
        value=Farmacéuticas[0],
        clearable=False,
               #width={'size' : 6,'offset' : 1 },
                  style={'width': '100%', 'display': 'inline-block','text-size': 28}),

   
    dcc.Graph(id="bar-chart", figure={},
              className="top_metrics",
                      style={'width': '100%', 'display': 'inline-block',
                            'align': 'center'}),
]),
    dbc.Row(
    [dbc.Toast([html.P("Este jueves México recibió el quinto embarque de vacunas "
           "contra COVID-19 producidas por la farmacéutica Sinovac Life Sciences Co., Ltd."
           "Se trata de un millón de dosis envasadas que, sumadas a las 200 mil que llegaron "
               " el 20 de febrero, 800 mil el 27 febrero, un millón del 13 de marzo y otro el"
               "18 de marzo, hacen un total de cuatro millones provenientes del laboratorio con"
               "sede en China. El biológico salió del Aeropuerto Internacional de Beijing, China;"
               "hizo escala en Hong Kong, después en Anchorage, Alaska, para ser enviado a México "
               "en el vuelo CX86 de la aerolínea Cathay Pacific. El vuelo arribó a las 4.34 h a "
               " la terminal 1 del Aeropuerto Internacional de la Ciudad de México (AICM) "
               "“Benito Juárez”. La Comisión Federal para la Protección de Riesgos Sanitarios "
               "(Cofepris) el pasado 9 de febrero emitió la autorización de para el uso de "
               "emergencia. México ha recibido 9 millones 818 mil 375 dosis de vacunas "
               "envasadas de las farmacéuticas: Pfizer-BioNTech, AstraZeneca, Sinovac y del"
               "Centro Nacional de Investigación de Epidemiología y Microbiología Gamaleya;"
               " asimismo, en nuestro país, el laboratorio Drugmex ha envasado 940 mil 470 "
               "dosis de la vacuna CanSino Biologics, lo que hace un total de 10 millones 758 "
               "mil 845 biológicos.Hasta hoy se han recibido 21 embarques -35 vuelos"
                       , className="lead")],
    header= "FICHA TÉCNICA ",
               style={"position": "static",# "top": 66, "right": 10,
                     'width': '100%',
                     },
              )])
    
])

@app.callback(
    Output("bar-chart", "figure"), 
    [Input("dropdown", "value")])
def update_bar_chart(Farmacéutica):
    mask = df["Farmacéutica"] == Farmacéutica
    fig = px.bar(df[mask], x="Fecha", y="Cantidad", 
                 color="Arribo", barmode="group",
                 color_continuous_scale=px.colors.sequential.Inferno)
    return fig
    
    
app.layout = html.Div([body])

from application.dash import app
from settings import config

if __name__ == "__main__":
    app.run_server()
