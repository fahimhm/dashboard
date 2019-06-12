# pandas for data management
import pandas as pd

# os for manipulating path
import os
from os.path import join

# dash & plotly for plotting
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# dataframe: overlap & shift_kosong
overlap = pd.read_excel(join(os.getcwd(), 'data_output', 'data_overlap.xlsx'), index_col=0)
shift_kosong = pd.read_excel(join(os.getcwd(), 'data_output', 'shift_kosong.xlsx'), index_col=0)

def plot(ol=overlap, sk=shift_kosong):
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div(children=[
        html.H1(children='VALIDASI DATA'),

        html.Div(children='''
            Jumlah Data Yang Perlu Dikoreksi
        '''),

        dcc.Graph(
            id = 'validasi-overlap-shift',
            figure = {
                'data': [
                    {'x': ol['workcenter'].unique().tolist(), 'y': ol.groupby('workcenter')['name'].count().values.tolist(), 'type': 'bar', 'name': 'overlap'},
                    {'x': sk['workcenter'].unique().tolist(), 'y': sk.groupby('workcenter')['name'].count().values.tolist(), 'type': 'bar', 'name': 'shift'}
                ],
                'layout': {
                    'title': 'Jumlah Data Overlap & WO Tanpa Info Shift'
                }
            }
        )
    ])

    # if __name__ == 'app':
    app.run_server(debug=True)