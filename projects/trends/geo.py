"""Geography and projection utilities."""

from data import DATA_PATH
from math import sin, cos, atan2, radians, sqrt
from json import JSONDecoder

def make_position(lat, lon):
    """Return a geographic position, which has a latitude and longitude."""
    return (lat, lon)

def latitude(position):
    """Return the latitudinal coordinate of a geographic position."""
    return position[0]

def longitude(position):
    """Return the longitudinal coordinate of a geographic position."""
    return position[1]

def geo_distance(position1, position2):
    """Return the great circle distance (in miles) between two
    geographic positions.

    Uses the "haversine" formula.
    http://en.wikipedia.org/wiki/Haversine_formula

    >>> round(geo_distance(make_position(50, 5), make_position(58, 3)), 1)
    559.2
    """
    earth_radius = 3963.2  # miles
    lat1, lat2 = [radians(latitude(p)) for p in (position1, position2)]
    lon1, lon2 = [radians(longitude(p)) for p in (position1, position2)]
    dlat, dlon = lat2-lat1, lon2-lon1
    a = sin(dlat/2) ** 2  + sin(dlon/2) ** 2 * cos(lat1) * cos(lat2)
    c = 2 * atan2(sqrt(a), sqrt(1-a));
    return earth_radius * c;

def position_to_xy(position):
    """Convert a geographic position within the US to a planar x-y point."""
    lat = latitude(position)
    lon = longitude(position)
    if lat < 25:
        return _hawaii(position)
    elif lat > 52:
        return _alaska(position)
    else:
        return _lower48(position)

def albers_projection(origin, parallels, translate, scale):
    """Return an Albers projection from geographic positions to x-y positions.

    Derived from Mike Bostock's Albers javascript implementation for D3
    http://mbostock.github.com/d3
    http://mathworld.wolfram.com/AlbersEqual-AreaConicProjection.html

    origin -- a geographic position
    parallels -- bounding latitudes
    translate -- x-y translation to place the projection within a larger map
    scale -- scaling factor
    """
    phi1, phi2 = [radians(p) for p in parallels]
    base_lat = radians(latitude(origin))
    s, c = sin(phi1), cos(phi1)
    base_lon = radians(longitude(origin))
    n = 0.5 * (s + sin(phi2))
    C = c*c + 2*n*s
    p0 = sqrt(C - 2*n*sin(base_lat))/n

    def project(position):
        lat, lon = radians(latitude(position)), radians(longitude(position))
        t = n * (lon - base_lon)
        p = sqrt(C - 2*n*sin(lat))/n
        x = scale * p * sin(t) + translate[0]
        y = scale * (p * cos(t) - p0) + translate[1]
        return (x, y)
    return project

_lower48 = albers_projection(make_position(38, -98), [29.5, 45.5], [480,250], 1000)
_alaska = albers_projection(make_position(60, -160), [55,65], [150,440], 400)
_hawaii = albers_projection(make_position(20, -160), [8,18], [300,450], 1000)

def load_states():
    """Load the coordinates of all the state outlines and return them
    in a dictionary, from names to shapes lists.

    >>> len(load_states()['HI'])  # Hawaii has 5 islands
    5
    """
    json_data_file = open(DATA_PATH + 'states.json', encoding='utf8')
    states = JSONDecoder().decode(json_data_file.read())
    for state, shapes in states.items():
        for index, shape in enumerate(shapes):
            if type(shape[0][0]) == list:  # the shape is a single polygon
                assert len(shape) == 1, 'Multi-polygon shape'
                shape = shape[0]
            shapes[index] = [make_position(*reversed(pos)) for pos in shape]
    return states

us_states = load_states()
