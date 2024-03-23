import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta
import plotly.express as px

df = pd.read_csv("Final.csv")

df['EVENT_DATE2'] = pd.to_datetime(df['EVENT_DATE'], format='%d-%B-%Y')
df_last_three_months = df[df['EVENT_DATE2'] >= (datetime.now() - timedelta(days=90))]
events_per_week = df_last_three_months.resample('W-Mon', on='EVENT_DATE2').size()
average_activities_per_day = events_per_week / 7  

fig = go.Figure()

fig.add_trace(go.Bar(
    x=[date.strftime('%Y-%m-%d') for date in events_per_week.index],
    y=events_per_week,
    marker_color='skyblue',
    text=[date.strftime('%Y-%m-%d') for date in events_per_week.index],
    textposition='outside',
    textangle=-45,
    name=''
))

fig.update_layout(
    title='Number of Events per Week in the Last Three Months',
    xaxis=dict(title='Date'),
    yaxis=dict(title='Number of Events', range=[0, events_per_week.max() * 1.1]),
    height=400, 
    plot_bgcolor='rgba(0, 0, 0, 0)'  
)

small_df = pd.read_csv("DataFrame.csv")

small_df['Percent_Change'] = small_df['Percent_Change'].replace('null', '+inf')

#Making widgets for table
def create_widget(val):
    return str(val) + "%"  

fig2 = go.Figure(data=[go.Table(
    header=dict(values=list(small_df.columns),
                fill_color = 'paleturquoise',
                align='left'),
    cells=dict(values=[small_df.Country, small_df.Events_One_Year_Ago_to_Now, small_df.Percent_Change],
               fill_color='lavender',
               align='left'))
])


fig3 = px.scatter_mapbox(df, lat="LATITUDE", lon ='LONGITUDE', hover_name="COUNTRY", hover_data=["DISORDER_TYPE", 'EVENT_TYPE', "SUB_EVENT_TYPE"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300 )
fig3.update_layout(mapbox_style="open-street-map")
fig3.update_layout(margin={"r":0, "t":0, "l":0, "b":0})  

# Initialize the Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div(style={'backgroundColor': '#000000', 'color': 'white'}, children=[
    html.Div(style={'backgroundColor': 'black', 'padding': '15px', 'position': 'relative', 'zIndex': '1'}, children=[
        html.H1(children='ACLED WAGNER', style={'color': 'white', 'textAlign': 'center', 'margin': '0'})
    ]),
    html.Div(className='grid-container', children=[
        html.Div(className='map-container', children=[
            dcc.Graph(figure=fig3)
        ], style={'position': 'absolute', 'top': '50px', 'left': '10px', 'width': '100%', 'height': '50%'}),
        html.Div(className='bottom-container', children=[
            html.Div(className='graph-container', children=[
                dcc.Graph(figure=fig)
            ], style={'width': '50%', 'height': '100%', 'float': 'left'}),
            html.Div(className='small-df-container', children=[
                dcc.Graph(figure=fig2)
            ], style={'width': '50%', 'height': '100%', 'float': 'right'})
        ], style={'position': 'absolute', 'bottom': '0px', 'width': '100%', 'height': '50%'})
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)
