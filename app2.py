from dash import html, dcc, Output, Input, Dash, State, callback
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from dash_extensions import WebSocket


update_frequency = 200 ### in milliseconds


app = Dash(__name__)


app.layout = html.Div([
    html.H1(id="price-ticker"),
    dcc.Interval(id="update", interval = update_frequency),
    ])

@app.callback(
        Output("price-ticker", "children"),
        Input("update", "n_intervals"),
    )

def update_data(intervals):

    connection = sqlite3.connect("./data.db")
    cursor = connection.cursor()

    data = cursor.execute("SELECT * FROM trades ORDER BY time DESC LIMIT 10").fetchone()

    print(type(data))
 

    return data[0][3]


if __name__ == '__main__':
    app.run_server(debug=True)





