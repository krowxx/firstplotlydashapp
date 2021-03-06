#using the dash and plotly library create a realtime candlestick plot of the data
from dash.dependencies import Input, Output
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

#read the data from the csv file
df = pd.read_csv('bitcoin15minute.csv')
#convert the open_time to datetime
df['open_time'] = pd.to_datetime(df['open_time'])
#set the index to open_time
df.set_index('open_time', inplace=True)

#create the dash app
app = dash.Dash()

#create the layout
app.layout = html.Div(children=[
    html.H1(children='Bitcoin Candlestick Chart'),
    dcc.Graph(id='graph'),
    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0)
])

#create the callback
@app.callback(Output('graph', 'figure'),
                [Input('interval-component', 'n_intervals')])
def update_graph(n):
    #read the data from the csv file
    df = pd.read_csv('bitcoin15minute.csv')
    #convert the open_time to datetime
    df['open_time'] = pd.to_datetime(df['open_time'])
    #set the index to open_time
    df.set_index('open_time', inplace=True)
    #create the candlestick plot
    candlestick = go.Candlestick(x=df.index,
                                    open=df['open'],
                                    high=df['high'],
                                    low=df['low'],
                                    close=df['close'])
    #create the layout
    layout = go.Layout(title='Bitcoin Candlestick Chart',
                        xaxis=dict(rangeslider=dict(visible=False)),
                        yaxis=dict(title='Price'))
    #create the figure
    fig = go.Figure(data=[candlestick], layout=layout)
    #return the figure
    return fig

#run the app
if __name__ == '__main__':
    app.run_server(debug=True)
