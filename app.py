import pandas as pd
import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ClientsideFunction
import plotly.graph_objs as go
import plotly.express as px

validation_df = pd.read_csv("./data/rnn_validation.csv")
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

slider_dict = {idx: value for idx, value in enumerate(validation_df.columns)}
slider_dict.pop(0)
slider_dict.pop(len(slider_dict))

app.layout = html.Div([
    html.Div([
        html.H1('Recurrent Neural Network implementation - example'),

    ], id='header-div'),
    html.Br(),
    html.Div([dcc.Graph(id='rnn-graph'),
              html.Div([dcc.Slider(
                  id='year-slider',
                  min=min(slider_dict.keys()),
                  max=max(slider_dict.keys()),
                  value=min(slider_dict.keys()),
                  marks=slider_dict,
                  step=None
              ),
              ],
                  id="slider-div",
              )
              ],
             id="plot-div")
    ,
    html.Br(),
], id='main-div')


@app.callback(
              Output("rnn-graph", "figure"),
            Input("year-slider", "value")
              )
def update_figure(value):
    fig = px.line(
        validation_df,
        x="index",
        y=slider_dict[value],
        color="type",
    )
    fig.update_layout(
        title=f"Comparison for {slider_dict[value]} variable",
        title_x=0.5,
        xaxis_title="Timestep",
        yaxis_title=f"{slider_dict[value]}"
    )
    return fig


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True)
