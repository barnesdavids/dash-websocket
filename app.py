from dash import html, dcc, Output, Input, Dash, State, callback
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import time
import math


update_frequency = 1000 ### in milliseconds


default_fig = dict(
    data=[{'x':[], 'y':[]}],
    layout=dict(
        xaxis=dict(range=[-1,1]),
        yaxis=dict(range=[0,8000]),
    ),
)

app = Dash(__name__)


app.layout = html.Div([
    html.H1(id='price-ticker'),
    dcc.Graph(id='graph', figure = default_fig),
    dcc.Interval(id='update', interval = update_frequency),])

@app.callback(
        Output('graph', 'extenData'),
        Output('price-ticker', 'children'),
        Input('update', 'n_intervals'),
        )

def update_data(intervals):

    connection = sqlite3.connect("./data.db")
    cursor = connection.cursor()

    time_from = math.floor((time.time() - 60 ) * 1000)

    data = cursor.execute(f"SELECT * FROM trades WHERE time > {time_from} ORDER BY time DESC").fetchall()

    print(data)
    current_price = data[0][3]
    total_trades = len(data)

    # return data[0][3]

    return (dict(x=[[time.time()]], y=[[total_trades]]),[0],100),current_price

if __name__ == '__main__':
    app.run_server(debug=True)





