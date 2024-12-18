# Imports
import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Load Data
df = pd.read_csv("C:/VS code/world happiness index/assets/WHR2024.csv")

# App Initialization
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App Layout
app.layout = dbc.Container([
    # Header
    html.Div(className='app-header', children=[
        html.H1("World Happiness Index Dashboard", className='display-3')
    ]),

    # Dropdown Menu
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="metric-dropdown",
                options=[
                    {'label': 'Ladder Score', 'value': 'Ladder score'},
                    {'label': 'Log GDP per capita', 'value': 'Explained by: Log GDP per capita'},
                    {'label': 'Social Support', 'value': 'Explained by: Social support'},
                    {'label': 'Healthy Life Expectancy', 'value': 'Explained by: Healthy life expectancy'},
                    {'label': 'Freedom to Make Life Choices', 'value': 'Explained by: Freedom to make life choices'},
                    {'label': 'Generosity', 'value': 'Explained by: Generosity'},
                    {'label': 'Perceptions of Corruption', 'value': 'Explained by: Perceptions of corruption'},
                ],
                value='Ladder score',
                style={'width': '100%'}
            )
        ], width={'size': 6, 'offset': 3}, className='dropdown-container')
    ]),

    # World Map Section
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='World-map')
        ], width=12)
    ], className='mt-4'),

    # Bottom Section: Top/Bottom Countries and Country Details
    dbc.Row([
        # Left: Top and Bottom Countries
        dbc.Col([
            html.Div(id='top-bottom-countries', className='top-bottom-container')
        ], width=6),

        # Right: Country Details (Placed Bottom Right)
        dbc.Col([
            html.Div(id='country-details', className='country-details-section',
                     style={'border': '1px solid #ddd', 'padding': '15px', 'border-radius': '10px', 'background-color': '#f9f9f9'})
        ], width=6, className="text-right")
    ], className="mt-4")
], fluid=True)

# Callbacks
# Update World Map
@app.callback(
    Output('World-map', 'figure'),
    Input("metric-dropdown", 'value')
)
def update_map(selected_metric):
    fig = px.choropleth(
        df,
        locations="Country name",
        locationmode='country names',
        color=selected_metric,
        hover_name="Country name",
        color_continuous_scale=px.colors.sequential.Blues,
        title=f"World Happiness Index: {selected_metric}"
    )
    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 40})
    return fig

# Update Top and Bottom Countries
@app.callback(
    Output('top-bottom-countries', 'children'),
    Input('metric-dropdown', 'value')
)
def update_top_bottom(selected_metric):
    top_countries = df.nlargest(5, selected_metric)
    bottom_countries = df.nsmallest(5, selected_metric)

    top_list = html.Ul([html.Li(f"{row['Country name']}: {row[selected_metric]}") for _, row in top_countries.iterrows()])
    bottom_list = html.Ul([html.Li(f"{row['Country name']}: {row[selected_metric]}") for _, row in bottom_countries.iterrows()])

    return html.Div([
        html.Div([html.H3("Top 5 Countries"), top_list], className="top-bottom-section"),
        html.Div([html.H3("Bottom 5 Countries"), bottom_list], className="top-bottom-section")
    ])

# Update Country Details when Clicking on Map
@app.callback(
    Output('country-details', 'children'),
    Input('World-map', 'clickData')
)
def display_country_details(clickData):
    if clickData:
        country_name = clickData['points'][0]['location'].lower()
        country_data = df[df["Country name"].str.lower() == country_name]

        if not country_data.empty:
            country = country_data.iloc[0]
            details = [
                html.H3(f"Details for {country_name.capitalize()}"),
                html.P(f"Overall Rank: {country.get('Overall rank', 'N/A')}"),
                html.P(f"Ladder Score: {country.get('Ladder score', 'N/A')}"),
                html.P(f"GDP per Capita: {country.get('Explained by: Log GDP per capita', 'N/A')}"),
                html.P(f"Social Support: {country.get('Explained by: Social support', 'N/A')}"),
                html.P(f"Healthy Life Expectancy: {country.get('Explained by: Healthy life expectancy', 'N/A')}"),
                html.P(f"Freedom to Make Life Choices: {country.get('Explained by: Freedom to make life choices', 'N/A')}"),
                html.P(f"Generosity: {country.get('Explained by: Generosity', 'N/A')}"),
                html.P(f"Perceptions of Corruption: {country.get('Explained by: Perceptions of corruption', 'N/A')}")
            ]
            return html.Div(details)
    return html.Div("Click on a country to see details.")

# Run Server
if __name__ == "__main__":
    app.run_server(debug=True)
