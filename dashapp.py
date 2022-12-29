import dash
from dash import html
from dash import dcc
import pandas as pd
import pickle
import os
import dash_bootstrap_components as dbc
from main import generate_fig
import main as m
import plotly.figure_factory as ff
import plotly.express as px
external_stylesheets = [dbc.themes.BOOTSTRAP]


def create_app(server_):

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server_)

    # Define the layout of the app

    LOWER = 45

    map_height = 60
    settings_pad = 2

    DIR = os.path.dirname(__file__)

    if os.path.exists(f'{DIR}/fig.p'):
        fig = pickle.load(open(f'{DIR}/fig.p', 'rb'))
    else:
        fig = generate_fig(m.centre, m.target, m.radius_miles, opacity=0.4)
        pickle.dump(fig, open(f'{DIR}/fig.p', 'wb'))

    app.layout = html.Div([
        # Add the plotly figure

        dcc.Graph(figure=fig,
                  id='plot',
                  style={'height': f'{int(map_height)}vh', 'width': '100%'}),
        # Add the slider to control the opacity

        dbc.Container([
            dbc.Row([
                dbc.Col([

                    dbc.Card([
                        dbc.CardHeader(),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        html.H4('Radius [miles]:'),
                                        dbc.Spinner(
                                            dcc.Slider(id='radius-slider',
                                                       min=3,
                                                       max=5,
                                                       step=5,
                                                       value=3,
                                                       marks={i: f'{i}' for i in range(3, 6, 2)},
                                                       className='slider'),
                                        )
                                    ])
                                ], width=6),
                                dbc.Col([
                                    html.Div([
                                        html.H4('Opacity:'),
                                        dcc.Slider(id='opacity-slider',
                                                   min=0,
                                                   max=1,
                                                   step=0.01,
                                                   value=0.4,
                                                   marks={i / 10: f'{i / 10}' for i in range(0, 11)},
                                                   className='slider'),
                                    ])
                                ], width=6)
                            ]),

                        ]),
                        dbc.CardHeader(),
                    ]),
                ]),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        html.H4('Upper limit [minutes]:'),
                                        dbc.Spinner(
                                            dcc.RangeSlider(id='limit-slider',
                                                            min=0,
                                                            max=600,
                                                            step=5,
                                                            value=(0, 600),
                                                            marks={i: f'{i}' for i in range(45, 605, 100)},
                                                            className='slider'),
                                        )
                                    ])
                                ], width=6),
                                dbc.Tooltip('This feature has not been implemented yet.', target='granularity-column'),
                                dbc.Col([
                                    html.H4('Granularity:'),
                                    dbc.Row([
                                        dbc.Col(
                                            dbc.Spinner(
                                                dcc.Slider(id='granularity-slider',
                                                           min=10,
                                                           max=50,
                                                           step=5,
                                                           value=25,
                                                           marks={i: f'{i}' for i in range(10, 51, 5)},
                                                           className='slider'),
                                            ),
                                            width=12,
                                        ),
                                    ], justify='center'),
                                ], width=6, id='granularity-column')
                            ]),

                        ]),
                        dbc.CardHeader(),
                    ]),
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.H4('Centre [latitude, longitude]:'),
                                    dbc.Row([
                                        dbc.Col(
                                            dcc.Input(id='centre_input',
                                                      type='text',
                                                      value=f'{m.centre[0]}, {m.centre[1]}',
                                                      placeholder='latitude, longitude',
                                                      debounce=True,
                                                      style={'width': '100%'}),
                                            width=12,
                                        ),
                                    ], justify='center'),
                                ], width=12),
                            ]),

                        ]),
                        dbc.CardHeader(),
                    ]),
                ]),
                dbc.Col([
                    dbc.Tooltip('This feature has not been implemented yet.', target='target-card'),
                    dbc.Card([
                        dbc.CardHeader(),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.H4('Target [latitude, longitude]:'),
                                    dbc.Row([
                                        dbc.Col(
                                            dcc.Input(id='lat_lon_input',
                                                      type='text',
                                                      value=f'{m.target[0]}, {m.target[1]}',
                                                      placeholder='latitude, longitude',
                                                      debounce=True,
                                                      style={'width': '100%'}),
                                            width=12,
                                        ),
                                    ], justify='center'),
                                ], width=12),
                            ]),

                        ]),
                        dbc.CardHeader(),
                    ], id='target-card'),
                ]),
            ], style={'padding-top': f'{settings_pad}vh'})
        ], style={'height': f'{100-int(map_height)-settings_pad}vh', 'width': '100%', 'padding-top': f'{settings_pad}vh'})
    ], style={'height': '100vh', 'width': '100%'})


    # Define a callback function to update the figure's opacity when the slider value changes
    @app.callback(
        [
            dash.dependencies.Output('plot', 'figure'),
            dash.dependencies.Output('limit-slider', 'max'),
            dash.dependencies.Output('limit-slider', 'value'),
            dash.dependencies.Output('limit-slider', 'marks'),
        ],
        [
            dash.dependencies.Input('opacity-slider', 'value'),
            dash.dependencies.Input('radius-slider', 'value'),
            dash.dependencies.Input('limit-slider', 'value'),
            dash.dependencies.Input('granularity-slider', 'value'),
            dash.dependencies.Input('lat_lon_input', 'value'),
        ],
        [
            dash.dependencies.State('plot', 'figure'),
        ],
        prevent_initial_callbacks=True
    )
    def update_figure(opacity, radius, range_, n_hex, lat_lon_target, fig):
        # Get the current figure
        # Update the figure's opacity
        target = [float(c.strip(' ')) for c in lat_lon_target.split(',')]
        max_ = int(max(fig['data'][0]['z']))
        zoom_ = fig['layout']['mapbox']['zoom']
        center_ = fig['layout']['mapbox']['center']
        if dash.callback_context.triggered_id == 'opacity-slider':
            fig['data'][0]['marker']['opacity'] = opacity
        elif dash.callback_context.triggered_id == 'granularity-slider':
            fig = generate_fig(m.centre, target, radius, opacity=opacity, nx_hexagon=n_hex)

        elif dash.callback_context.triggered_id == 'radius-slider':
            fig = generate_fig(m.centre, target, radius, opacity=opacity, nx_hexagon=n_hex)
            max_ = int(max(fig['data'][0]['z']))
            range_ = (0, max_)
            print()
        elif dash.callback_context.triggered_id == 'limit-slider':
            fig = generate_fig(m.centre, target, radius, opacity=opacity, range_color=range_, nx_hexagon=n_hex)
        else:
            range_ = (0, max_)

        if not isinstance(fig, dict):
            geojson_data = pd.DataFrame.from_records(fig.data[0].geojson['features'])
            custom_data = pd.DataFrame(fig.data[0].customdata)
            data = pd.concat([custom_data, geojson_data],
                      axis=1)
            filter_by_range = data[0] < range_[1]
            filter_by_error = data[0] != 0
            filter_ = filter_by_range & filter_by_error

            geojson_data_ = data.loc[filter_, geojson_data.columns]
            custom_data_ = data.loc[filter_, custom_data.columns]
            fig.data[0].geojson['features'] = geojson_data_.to_dict('records')
            fig.data[0].customdata = custom_data_.values
        fig['layout']['mapbox']['zoom'] = zoom_
        fig['layout']['mapbox']['center'] = center_
        return [fig, max_, range_, {i: f'{i}' for i in range(0, max_ + 1, int((max_ + 1)/10))}]
    # Define a callback function to update the figure's opacity when the slider value changes
    # @app.callback(
    #     [
    #         dash.dependencies.Output('lat_lon_input', 'value'),
    #     ],
    #     [
    #         dash.dependencies.Input('plot', 'clickData'),
    #         dash.dependencies.Input('plot', 'hoverData'),
    #         dash.dependencies.Input('plot', 'selectedData'),
    #     ],
    #     [
    #     ],
    #     prevent_initial_callbacks=True
    # )
    # def update_latlong(click, hover, selectedData):
    #     # Get the current figure
    #     # Update the figure's opacity
    #     if dash.callback_context.triggered_id == 'opacity-slider':
    #         pass
    #     latlong = ''
    #     return [latlong]
    return app.server

