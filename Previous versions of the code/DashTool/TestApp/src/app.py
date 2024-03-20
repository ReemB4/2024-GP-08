'''
# This app creates a simple sidebar layout using inline style arguments and the
# dbc.Nav component.
# dcc.Location is used to track the current location, and a callback uses the
# current location to render the appropriate page content. The active prop of
# each NavLink is set automatically according to the current pathname. To use
# this feature you must install dash-bootstrap-components >= 0.11.0.
# For more details on building multi-page Dash applications, check out the Dash
# documentation: https://dash.plot.ly/urls
# Source: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
# @ Create Time: 2024-03-13 04:49:09.174227
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
'''

import time
import dash
import numpy as np
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

app = dash.Dash(
    title="PDPrognosis",
    external_stylesheets=[dbc.themes.PULSE],
    #use_pages=True
    )

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

SIDEBAR_STYLE2 = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "19rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "19rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

LOGO_STYLE = {
    "width":"10rem",
    "margin":"0 3rem"

}

sidebar = html.Div(
    [
        html.Img(src="assets/PDPrognosis.png", style=LOGO_STYLE),
        html.H2("PDPrognosis"),#, className="display-4"
        html.Hr(),
        #html.P(
         #   "A simple sidebar layout with navigation links", className="lead"
        #),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Patients", href="/page-1", active="exact"),
                dbc.NavLink("Profile", href="/page-2", active="exact"),
                dbc.NavLink("Settings", href="/page-3", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(
    #[
        id="page-content",


    #],
    style=CONTENT_STYLE
)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the content of page 1. Yay!") 
    elif pathname == "/page-1":
        return patient_list(pathname)
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    elif pathname == "/page-3":
        return html.P("Oh cool, this is page 3!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

def patient_list(pathname):
    if pathname == "/page-1":
        
        content= dbc.Container([
            dcc.Store(id="store"),
            html.H1("patient name"),
            html.Hr(),
            dbc.Button(
                "Print information",
                color="primary",
                id="button",
                className="mb-3",
            ),
            dbc.Tabs(
                [
                    dbc.Tab(label="Protein", tab_id="Protein"),
                    dbc.Tab(label="Peptide", tab_id="Peptide"),
                ],
                id="tabs",
                active_tab="Protein",
            ),
            html.Div(id="tab-content", className="p-4"),])
    return content


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")],
)
def render_tab_content(active_tab, data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab is not None:
        if active_tab == "Protein":
            return html.P("This is the content of Protein") #dcc.Graph(figure=data["scatter"])
        elif active_tab == "Peptide":
            return html.P("This is the content of Peptide") 
        '''
        dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=data["hist_1"]), width=6),
                    dbc.Col(dcc.Graph(figure=data["hist_2"]), width=6),
                ]
            )
        '''
    return "No tab selected"


@app.callback(Output("store", "data"), [Input("button", "n_clicks")])
def generate_graphs(n):
    """
    This callback generates three simple graphs from random data.
    """
    if not n:
        # generate empty graphs when app loads
        return {k: go.Figure(data=[]) for k in ["scatter", "hist_1", "hist_2"]}

    # simulate expensive graph generation process
    time.sleep(2)

    # generate 100 multivariate normal samples
    data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], 100)

    scatter = go.Figure(
        data=[go.Scatter(x=data[:, 0], y=data[:, 1], mode="markers")]
    )
    hist_1 = go.Figure(data=[go.Histogram(x=data[:, 0])])
    hist_2 = go.Figure(data=[go.Histogram(x=data[:, 1])])

    # save figures in a dictionary for sending to the dcc.Store
    return {"scatter": scatter, "hist_1": hist_1, "hist_2": hist_2}



if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
'''
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

# Sample data for patients
patients_data = {
    'Patient_ID': [1, 2, 3, 4, 5],
    'Name': ['John Doe', 'Jane Smith', 'Alice Johnson', 'Bob Brown', 'Eve Williams'],
    'Age': [35, 28, 42, 50, 45],
    'Gender': ['Male', 'Female', 'Female', 'Male', 'Female']
}

# Sample data for peptides and proteins
peptides_data = {
    'Peptide_ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Peptide': ['Peptide A', 'Peptide B', 'Peptide C', 'Peptide D', 'Peptide E',
                'Peptide F', 'Peptide G', 'Peptide H', 'Peptide I', 'Peptide J'],
    'Patient_ID': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
}

proteins_data = {
    'Protein_ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Protein': ['Protein A', 'Protein B', 'Protein C', 'Protein D', 'Protein E',
                'Protein F', 'Protein G', 'Protein H', 'Protein I', 'Protein J'],
    'Patient_ID': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
}

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sidebar navigation
sidebar = html.Div(
    [
        html.H2("Navigation", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Patients", href="/patients", id="patients-link"),
                dbc.NavLink("Peptides", href="/peptides", id="peptides-link"),
                dbc.NavLink("Proteins", href="/proteins", id="proteins-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="bg-light",
    style={'position': 'fixed', 'height': '100%', 'width': '20%'}
)

# Content div
content = html.Div(id="page-content", style={'margin-left': '25%', 'padding': '20px'})

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# Callback to update page content based on URL
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/patients":
        return generate_patient_list()
    elif pathname == "/peptides":
        return generate_peptides_list()
    elif pathname == "/proteins":
        return generate_proteins_list()
    else:
        return generate_patient_list()


def generate_patient_list():
    # Retrieve patient data
    df_patients = pd.DataFrame(patients_data)
    # Create table with patient info
    table = dbc.Table.from_dataframe(df_patients, striped=True, bordered=True, hover=True)
    return table


def generate_peptides_list():
    # Retrieve peptides data
    df_peptides = pd.DataFrame(peptides_data)
    # Create table with peptides info
    table = dbc.Table.from_dataframe(df_peptides, striped=True, bordered=True, hover=True)
    return table


def generate_proteins_list():
    # Retrieve proteins data
    df_proteins = pd.DataFrame(proteins_data)
    # Create table with proteins info
    table = dbc.Table.from_dataframe(df_proteins, striped=True, bordered=True, hover=True)
    return table


if __name__ == "__main__":
    app.run_server(debug=True)

'''