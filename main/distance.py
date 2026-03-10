"""Distance helpers."""

from math import asin, cos, radians, sin, sqrt

# Function to compute distance using the Haversine formula.
# lat = latitude, lon = longitude
def haversine(lat1,lon1,lat2,lon2):
    """Return the great-circle distance between two coordinates in km."""
    #d = 2R * arcsin( sqrt( sin²((lat2-lat1)/2) + cos(lat1)cos(lat2)sin²((lon2-lon1)/2) ) )
    R_earth = 6371 #km
    rad_lat1, rad_lon1, rad_lat2, rad_lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = rad_lat2 - rad_lat1
    dlon = rad_lon2 - rad_lon1

    a = sin(dlat/2)**2 + cos(rad_lat1) * cos(rad_lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    return R_earth * c
