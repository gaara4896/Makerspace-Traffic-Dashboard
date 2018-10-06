# import datetime
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
import requests

# pip install pyorbital
# from pyorbital.orbital import Orbital
# satellite = Orbital('TERRA')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('Traffic of University Foyer'),
        # html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=5 * 1000,  # in milliseconds
            n_intervals=0
        )
    ])
)


# @app.callback(Output('live-update-text', 'children'),
#               [Input('interval-component', 'n_intervals')])
# def update_metrics(n):
#     lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
#     style = {'padding': '5px', 'fontSize': '16px'}
#     return [
#         html.Span('Longitude: {0:.2f}'.format(lon), style=style),
#         html.Span('Latitude: {0:.2f}'.format(lat), style=style),
#         html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
#     ]


# Multiple components can update everytime interval gets fired.


@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    # satellite = Orbital('TERRA')
    data = {
        'time': [],
        'traffic': [],
    }

    # Collect some data
    # for i in range(180):
    # time = datetime.datetime.now()
    response = requests.get("http://localhost:5000/")

    for traffic in response.json():
        data['traffic'].append(traffic['traffic'])
        data['time'].append(datetime.utcfromtimestamp(int(traffic['date'])))

    # data['traffic'].append(traffic.text)
    # data['time'].append(time)

    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x': data['time'],
        'y': data['traffic'],
        'name': 'Traffic',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)