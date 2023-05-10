import base64
import io

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table

import pandas as pd
import requests
import csv
import os

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['/assets/css/main.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "CSC310 APP"
app.layout = html.Div(
    id='body',
    children=[
        # Header
        html.Div(
            id='header',
            children=html.Div('DATA SCIENCE APP')
        ),
        html.Div(
            id='upload-title',
            children=html.Div('Upload CSV')
        ),

        # drop upload
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select File')
            ]),
            # Allow multiple files to be uploaded
            multiple=True
        ),

        # url upload
        html.Div([
            dcc.Input(
                id="input",
                type='text',
                placeholder="enter csv url",
            ),
            html.Button('Submit', id='submit-val', n_clicks=0)
        ]),


        html.Div(id='output-data-upload'),
        html.Div(id='data-preview'),

        # Footer 
        html.Div(
            id='footer',
            children=[
                html.Div(
                    id='footer-content',
                    children=[
                        html.H3('About'),
                        html.P("This utility is designed for data science purposes and enables the user to upload CSV files either by providing a URL or by dragging and dropping the file. It facilitates viewing of data in a table form along with important attributes such as column names, data types, null values, and unique values. This tool simplifies the process of data analysis by providing an efficient way to view data without requiring manual extraction through code.")
                    ]
                ),
                html.Div(
                    id='footer-content',
                    children=[
                        html.H3('Features'),
                        html.P("• Column Names"),
                        html.P("• Data Types"),
                        html.P("• Null Values"),
                        html.P("• Number of Uniques"),
                        html.P("• Shape (column, row)"),
                    ]
                ),
                html.Div(
                    id='footer-content',
                    children=[
                        html.H3('Author'),
                        html.P("Eric Chin"),
                        html.P("5/10/23"),
                        html.P("Github:"),
                        html.A("https://github.com/EricC1019/DataScienceApp", href="https://github.com/EricC1019/DataScienceApp")
                    ]
                ),
            ]
        )
    ]
)

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    
    return create_tables(filename, df)


def create_tables(filename, df):
    # df analysis
    columns = list(df.columns)
    col_info = [html.Div(
            id='df-cols-header',
            children=[
                html.Div("columns"),
                html.Div("dType"),
                html.Div("isNull"),
                html.Div("unique")
            ])]

    for col in columns:
        line = html.Div(
            id='df-cols',
            children=[
                html.Div(col),
                html.Div(str(df[col].dtype)),
                html.Div(df[col].isnull().sum()),
                html.Div(len(df[col].unique()))
            ]
        )
        col_info.append(line)

    col_info_divs = [html.Div(col_item) for col_item in col_info]

    df_shape = "{}".format(df.shape)

    return html.Div([
        html.Div(
            id='dash-table-title',
            children=[
                html.H3(filename),
                html.H3(df_shape),
            ]
        ),

        html.Hr(),  # horizontal line

        # display col_info here
        *col_info_divs,

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns],
            id='dash-table',
            page_size=15
        ),
    ])
    

# Multi drop
@app.callback(Output('output-data-upload', 'children', allow_duplicate=True),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              prevent_initial_call=True)

def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        return children

# Url request
@app.callback(
    Output("output-data-upload", "children"),
    [Input("submit-val", "n_clicks")],
    [State("input", "value")]
)
def read_input(n_clicks, value):
    if n_clicks > 0:
        
        if not value.endswith('.csv'):
            return
        
        responce = requests.get(value)
        if responce.status_code == 200:
            csv_fname = 'data.csv'
            content = responce.content.decode('utf-8')
            lines = content.splitlines()

            csv_writer = csv.writer(open(csv_fname, 'w', newline=''))

            # Write each line to the CSV file
            for line in lines:
                csv_writer.writerow(line.split(','))

            df = pd.read_csv(csv_fname)
            os.remove(csv_fname)

            return create_tables(value, df)
        
        else:
            return html.Div('Please enter a valid CSV URL.')


if __name__ == '__main__':
    app.run_server(debug=True)
