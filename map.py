import pandas as pd
import plotly.express as px
from plotly.express.colors import sequential
import plotly.graph_objects as go
import plotly.figure_factory as ff


def create_heatmap(lats, lons, travel_time, center_lat, center_lon, target_lat, target_lon,
                   zoom=12,
                   opacity=0.5,
                   nx_hexagon=25,
                   range_color=None,
                   hex_points=False, return_=False):
    # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv')
    # Create a dataframe from the input data
    df = pd.DataFrame({'lat': lats,
                       'lon': lons,
                       'minutes': list(travel_time)})
    # fig, ax = plt.subplots(figsize=(15, 15))
    # sns.kdeplot(data=df,
    #             x='lon',
    #             y='lat',
    #             fill=True,
    #             cmap='coolwarm',
    #             alpha=0.3,
    #             gridsize=200,
    #             levels=20,
    #             ax=ax)

    # Create the heatmap
    # fig = px.density_mapbox(df, lat='lat', lon='lon', z='travel_time',
    #                         mapbox_style="stamen-terrain",
    #                         radius=50, center=dict(lat=center_lat, lon=center_lon),
    #                         opacity=0.5,
    #                         zoom=zoom)
    # Create the heatmap
    fig = ff.create_hexbin_mapbox(df, lat='lat', lon='lon',
                                  center=dict(lat=center_lat, lon=center_lon),
                                  opacity=opacity,
                                  nx_hexagon=nx_hexagon,
                                  color_continuous_scale=sequential.Viridis,
                                  labels={"color": "minutes"},
                                  range_color=range_color,
                                  color='minutes',
                                  # hover_data={'location': True, 'lat': True, 'lon': True},
                                  mapbox_style='open-street-map',
                                  zoom=zoom)

    fig.add_trace(go.Scattermapbox(
        mode="markers+lines",
        lat=[target_lat],
        lon=[target_lon],
        name='Target',
        hovertext='',
        marker={'size': 20}))

    fig.update_layout(margin=dict(b=0, t=0, l=0, r=0))

    if hex_points is False:

        points = []
        for hex in fig.data[0].geojson['features']:
            bottom = hex['geometry']['coordinates'][0][0]
            top = hex['geometry']['coordinates'][0][3]
            centre = (bottom[0], (top[1]-bottom[1])+bottom[1])
            points.append(centre)

        return points
    else:
        fig.update_layout(clickmode='event+select')

        if return_ is False:

            fig.show()
        else:
            return fig