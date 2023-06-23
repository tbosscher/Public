# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                    ],
                                    value='ALL',
                                    placeholder='Select a Launch Site here',
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                            ])


@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Calculate total success launches for all sites
        total_success = len(spacex_df[spacex_df['class'] == 1])
        total_failed = len(spacex_df[spacex_df['class'] == 0])

        # Create a pie chart figure
        labels = ['Success', 'Failed']
        values = [total_success, total_failed]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

        # Set chart title and return the figure
        fig.update_layout(title='Total Success Launches for All Sites')
        return fig
    else:
        # Filter the dataframe for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]

        # Calculate success and failed launches for the selected site
        site_success = len(filtered_df[filtered_df['class'] == 1])
        site_failed = len(filtered_df[filtered_df['class'] == 0])

        # Create a pie chart figure
        labels = ['Success', 'Failed']
        values = [site_success, site_failed]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

        # Set chart title and return the figure
        fig.update_layout(title=f'Success vs. Failed Launches for {selected_site}')
        return fig


@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        filtered_df = spacex_df[
            (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
            (spacex_df['Payload Mass (kg)'] <= payload_range[1])
        ]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        fig.update_layout(title='Payload vs. Launch Outcome for All Sites')
        return fig
    else:
        filtered_df = spacex_df[
            (spacex_df['Launch Site'] == selected_site) &
            (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
            (spacex_df['Payload Mass (kg)'] <= payload_range[1])
        ]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        fig.update_layout(title=f'Payload vs. Launch Outcome for {selected_site}')
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
