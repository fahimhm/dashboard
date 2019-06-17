# pandas for data management
import pandas as pd

# os for manipulating path
import os
from os.path import join

# dash & plotly for plotting
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go


def plot(ol, sk, df, wo_pmt, wo_rep):
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    available_year = df['year'].unique()
    available_woc = df['workcenter'].unique()

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
                        {'x': ol['workcenter'].unique().tolist(), 'y': ol.groupby('workcenter')['name'].count().values.tolist(), 'type': 'bar', 'name': 'overlap'},
                        {'x': sk['workcenter'].unique().tolist(), 'y': sk.groupby('workcenter')['name'].count().values.tolist(), 'type': 'bar', 'name': 'shift'}
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