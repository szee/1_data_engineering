import pandas as pd
import requests
import json

import psycopg2

from sqlalchemy import create_engine

import plotly.express as px
import plotly.figure_factory as ff

import dash
from dash import dcc 
from dash import html
from dash import dash_table, Input, Output

from pipe_line_workers import get_data, transform_data, agregate_data


url = "https://randomuser.me/api/?results=300&nat=de,dk,fr,gb&inc=id,gender,name,location,email,dob,picture,nat&seed=flightright"
df = get_data()
df_transformed = transform_data(df)
df_out = agregate_data(df_transformed)

df_transformed.to_csv('out.csv', sep=';', index=False)

engine = create_engine('postgresql://postgres:postgres@pgsql:5432/postgres')
try: df.to_sql('person', engine, if_exists='append', index=False)
except Exception as e: print(e) 

ls_stats = list(df_out.columns)
ls_stats.remove('location_country')



app = dash.Dash()
app.layout = html.Div([
    dash_table.DataTable(df_out.to_dict('records'), [{"name": i, "id": i} for i in df_out.columns]),
    html.Br(),
    dcc.Dropdown(ls_stats, id='pandas-dropdown'),
    dcc.Graph(id='map-graph')
])

@app.callback(
    Output('map-graph', 'figure'),
    [Input('pandas-dropdown', 'value')
     ])
def updMap(stat_name):
    fig = px.choropleth(locations=df_out["location_country"], 
                    color=df_out[stat_name], 
                    scope="europe", 
                    locationmode='country names', 
                    #show_state_data=False,
                    #show_hover=True,
                    color_continuous_scale="Viridis") 

    return fig

if __name__ == '__main__':
  app.run_server(host='0.0.0.0', port=8080, debug=False)
