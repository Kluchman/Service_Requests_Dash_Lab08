import pandas as pd
import dash
from dash import dcc, Dash, html, dash_table, callback, Output, Input
import plotly.express as px

# Load data
df = pd.read_csv('service_311.csv', encoding='ISO-8859-1')

app = Dash()

server=app.server

# Layout
app.layout = html.Div([
    html.Div(children='This is a dynamic table and chart showing service requests in Boston MA', style={'color': 'red'}),
    
    # ID to DataTable
    dash_table.DataTable(
        data=df.to_dict('records'), 
        page_size=10, 
        id='data_table'
    ),
    #h
    dcc.Graph(
        figure=px.histogram(
            df, 
            x='weekday', 
            barmode='relative', 
            histfunc='count', 
            color='reason'
        ), 
        id='graph_his'
    ),
    
    dcc.RadioItems(
        options=['daytime', 'nighttime', 'All'], 
        value='All', 
        id='radio_button'
    )
])

# Callback
@callback(
    Output(component_id='graph_his', component_property='figure'),
    Output(component_id='data_table', component_property='data'),  # Added Output for DataTable
    Input(component_id='radio_button', component_property='value')
)
def update_content(time):
    # Filter data based on selection
    if time == "All":
        filter_df = df
    else:
        filter_df = df[df['time_of_day'] == time]

    # Update figure
    fig = px.histogram(
        filter_df, 
        x='weekday', 
        barmode='relative', 
        histfunc='count', 
        color='reason'
    )
    
    # Update table data
    table_data = filter_df.to_dict('records')
    
    return fig, table_data  # Return both updated figure and table data

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
