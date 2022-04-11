
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import time

#create the app
app = dash.Dash()

#read the data
df = pd.read_csv('bitcoin15minute.csv')

#create the layout
app.layout = html.Div([
    html.H1('Bitcoin Price'),
    dcc.Graph(id='graph'),
    dcc.Interval(id='interval-component', interval=15*1000, n_intervals=0)
])

#create the callback
@app.callback(Output('graph', 'figure'),
                [Input('interval-component', 'n_intervals')])
def update_graph(n):
    #read the data
    df = pd.read_csv('bitcoin15minute.csv')
    #create the plot
    trace = go.Scatter(x=df['open_time'], y=df['close'], mode='lines')
    return {'data': [trace],
            'layout': go.Layout(title='Bitcoin Price',
                                xaxis={'title': 'Time'},
                                yaxis={'title': 'Price'})}

#run the app
if __name__ == '__main__':
    app.run_server()