import os
import travel as t
import numpy as np
import generate_points as gp
import map as m

DIR = os.path.dirname(__file__)
DENSITY = 25
centre = (55.83572232622345, -4.25126796966773)
target = t.QUEH
radius_miles = 3


def generate_fig(centre, target, radius_miles, show=False,
                 opacity=0.5,
                 nx_hexagon=25,
                 range_color=None):
    points = []
    for radius_miles in range(1, radius_miles):
        points.extend(gp.generate_circle(centre, radius_miles, num_points=DENSITY))
    # points = [points[:100]]
    lats = list(map(lambda p: p[0], points))
    longs = list(map(lambda p: p[1], points))
    travel_times = np.repeat(1, len(lats))

    hex_points = m.create_heatmap(lats, longs, travel_times, centre[0], centre[1], target[0], target[1])

    lats = list(map(lambda p: p[1], hex_points))
    longs = list(map(lambda p: p[0], hex_points))
    # travel_times = np.repeat(1, len(lats))
    travel_times = t.get_travel_time(list(zip(lats, longs)))

    fig = m.create_heatmap(lats, longs, travel_times, centre[0], centre[1], target[0], target[1], zoom=11.5,
                           hex_points=True,
                           opacity=opacity,
                           nx_hexagon=nx_hexagon,
                           range_color=range_color,
                           return_=not show)
    return fig


if __name__ == '__main__':
    fig = generate_fig(centre, target, radius_miles, show=True)




