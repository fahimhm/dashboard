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

# dash & plotly for plotting
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# call dataset
file_name = ['Performance_Teknisi_Tracker', 'Performance_WO_Tracker', 'Data_Mentah_Maintenance', 'Data_Mentah']
url_report = "http://maula.fahim:welcometoparadise21@reportportal/Reports/Pages/Folder.aspx?ItemPath=%2f99.+Aplikasi+lain-lain%2f04.Aplikasi+Manufacturing%2fPortal+Engineering%2fWork+Order&ViewMode=List"
set_dataset(url_report, file_name)

# read data into dataframes
data_rpmt = pd.read_csv(join(os.getcwd(), 'datasets', 'Data_Mentah_Maintenance.csv'))
data_raw = pd.read_csv(join(os.getcwd(), 'datasets', 'Data_Mentah.csv'))
data_tek = pd.read_csv(join(os.getcwd(), 'datasets', 'Performance_Teknisi_Tracker.csv'))
data_wo = pd.read_csv(join(os.getcwd(), 'datasets', 'Performance_WO_Tracker.csv'), dayfirst=True, parse_dates=[0])
data_shft = pd.read_csv(join(os.getcwd(), 'datasets', 'data_shift.csv'), sep=';')
data_msn = pd.read_csv(join(os.getcwd(), 'datasets', 'Database Mesin PEA 2019.csv'), sep=';')
data_nwo = pd.read_csv(join(os.getcwd(), 'datasets', 'info_non_wo.csv'), sep=';', dayfirst=True, parse_dates=[0])

# merging dataset & produce new dataset to correction
df = actransform(data_tek, data_wo, data_msn, data_shft, data_nwo)
mh, wo_pmt, wo_rep = prep4chart(df=df, rpmtdata=data_rpmt, rpairdata=data_raw)

# dataframe: overlap & shift_kosong
overlap = pd.read_excel(join(os.getcwd(), 'data_output', 'data_overlap.xlsx'), index_col=0)
shift_kosong = pd.read_excel(join(os.getcwd(), 'data_output', 'shift_kosong.xlsx'), index_col=0)

# start plot
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

available_year = mh['year'].unique()
available_woc = mh['workcenter'].unique()

app.layout = html.Div([
    html.Div([
        html.H1('VALIDASI DATA'),

        html.Div('''
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
    ], className = 'row-one'),
    
    html.Div([
        html.H1('Productivity vs Realisasi WO'),

        html.Div('''
            %_Productivity vs %_WO-PJOL vs %_WO-PMT
        '''),

        html.Div([
            dcc.Dropdown(
                id = 'year-selected',
                options = [{'label': i, 'value': i} for i in available_year],
                value = 2019
            ),
            dcc.Dropdown(
                id = 'workcenter-selected',
                options = [{'label': i, 'value': i} for i in available_woc],
                value = 'Utility'
            )
        ], style={'width':'48%', 'float':'right', 'display':'inline-block'}),

        dcc.Graph(id='graphic')
    ])   
])

@app.callback(
    Output('graphic', 'figure'),
    [Input('year-selected', 'value')])
def update_graph(year_value, woc_value, mh, wo_pmt, wo_rep):
    data = mh.merge(wo_pmt, on=['workcenter', 'year', 'month'])
    data = data.merge(wo_rep, on=['workcenter', 'year', 'month'])
    data = data[(data['workcenter'] == woc_value) & (data['year'] == year_value)].copy()

    return {
        'data': [go.Bar(
            x = data['month'],
            y = data['%_mhreal']
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Month',
                'type': 'linear'
            },
            yaxis={
                'title': 'realization',
                'type': 'linear'
            },
            margin={'l': 40, 'b': 40, 't':10, 'r': 0},
            hovermode='closest'
        )
    }

# if __name__ == 'app':
app.run_server(debug=False, use_reloader=False)