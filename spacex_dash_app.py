import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

DATA='spacex_launch_dash.csv'
df=pd.read_csv(DATA)
app=Dash(__name__)
site_col='Launch Site'; payload_col='Payload Mass (kg)'; class_col='class'; booster_col='Booster Version Category'
sites=['ALL']+sorted(df[site_col].dropna().unique().tolist())
app.layout=html.Div([
    html.H1('SpaceX Launch Records Dashboard'),
    dcc.Dropdown(sites,'ALL',id='site'),
    dcc.RangeSlider(float(df[payload_col].min()),float(df[payload_col].max()),value=[float(df[payload_col].min()),float(df[payload_col].max())],id='payload'),
    dcc.Graph(id='pie'), dcc.Graph(id='scatter')
])
@app.callback(Output('pie','figure'),Output('scatter','figure'),Input('site','value'),Input('payload','value'))
def update(site,payload):
    d=df[(df[payload_col]>=payload[0])&(df[payload_col]<=payload[1])]
    if site!='ALL': d=d[d[site_col]==site]
    pie=px.pie(d,names=class_col,title='Landing outcomes')
    scatter=px.scatter(d,x=payload_col,y=class_col,color=booster_col,title='Payload vs. landing outcome')
    return pie,scatter
if __name__=='__main__': app.run(debug=True)
