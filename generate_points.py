import math

def generate_circle(coordinate, radius_in_miles, num_points=360):
    latitude, longitude = coordinate
    points = []
    radius_in_degrees = radius_in_miles / 69  # 69 miles per degree of latitude/longitude
    for degree in range(num_points):
        degree = degree * 360/num_points
        radian = degree * math.pi / 180
        point = [
            latitude + radius_in_degrees * math.cos(radian),
            longitude + 2*radius_in_degrees * math.sin(radian)
        ]
        points.append(point)
    return points
