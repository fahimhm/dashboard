# pandas for data management
import pandas as pd

# os for manipulating path
import os
from os.path import join

# to download dataset
from scripts.download_dataset import set_dataset

# to produce: data_overlap & shift_kosong
from scripts.data_prep import actransform
from scripts.data_prep import prep4chart

# dash & plotly to plot
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# call dataset
file_name = ['Performance_Teknisi_Tracker', 'Performance_WO_Tracker', 'Data_Mentah_Maintenance', 'Data_Mentah']
url_report = "http://maula.fahim:welcometoparadise21@reportportal/Reports/Pages/Folder.aspx?ItemPath=%2f99.+Aplikasi+lain-lain%2f04.Aplikasi+Manufacturing%2fPortal+Engineering%2fWork+Order&ViewMode=List"
set_dataset(url_report, file_name)

# read data into dataframes
data_rpmt = pd.read_csv(join(os.getcwd(), 'datasets', 'Data_Mentah_Maintenance.csv'))
data_raw = pd.read_csv(join(os.getcwd(), 'datasets', 'Data_Mentah.csv'))
data_tek = pd.read_csv(join(os.getcwd(), 'datasets', 'Performance_Teknisi_Tracker.csv'))
data_wo = pd.read_csv(join(os.getcwd(), 'datasets', 'Performance_WO_Tracker.csv'))
data_shft = pd.read_csv(join(os.getcwd(), 'datasets', 'data_shift.csv'), sep=';')
data_msn = pd.read_csv(join(os.getcwd(), 'datasets', 'Database Mesin PEA 2019.csv'), sep=';')
data_nwo = pd.read_csv(join(os.getcwd(), 'datasets', 'info_non_wo.csv'), sep=';')

# merging dataset & produce new dataset to correction
df = actransform(data_tek, data_wo, data_msn, data_shft, data_nwo)
mh, wo_pmt, wo_rep = prep4chart(df=df, rpmtdata=data_rpmt, rpairdata=data_raw)

# dataframe: overlap & shift_kosong
overlap = pd.read_excel(join(os.getcwd(), 'data_output', 'data_overlap.xlsx'), index_col=0)
shift_kosong = pd.read_excel(join(os.getcwd(), 'data_output', 'data_overlap.xlsx'), index_col=0)

# start to plot
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
                {'x': overlap['workcenter'].unique().tolist(), 'y': overlap.groupby('workcenter')['name'].count().values.tolist(), 'type': 'bar', 'name': 'overlap'},
                {'x': shift_kosong['workcenter'].unique().tolist(), 'y': shift_kosong.groupby('workcenter')['name'].count().values.tolist(), 'type': 'bar', 'name': 'shift'}
            ],
            'layout': {
                'title': 'Jumlah Data Overlap & WO Tanpa Info Shift'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)