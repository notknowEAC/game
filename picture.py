"""Legacy direction helpers (currently unused in the main game)."""

from math import atan2, cos, degrees, radians, sin


def get_direction(degrees):
    """Map a bearing angle (0-360) to a compass direction string."""
    directions = ["North", "Northeast", "East", "Southeast", "South", "Southwest", "West", "Northwest"]
    index = int((degrees + 22.5) // 45) % 8

    return directions[index]

# Function to compute the compass bearing angle.
# θ = atan2(x,y)
# x=sin(Δλ)cos(ϕ2​)
# y=cos(ϕ1​)sin(ϕ2​)−sin(ϕ1​)cos(ϕ2​)cos(Δλ)
def compress_get_bearing(lat1, lon1, lat2, lon2):
    """Compute the bearing angle from (lat1, lon1) to (lat2, lon2)."""
    rad_lat1, rad_lat2, rad_lon1, rad_lon2 = map(radians, [lat1, lat2, lon1, lon2])
    dlon = rad_lon2 - rad_lon1

    x = sin(dlon) * cos(rad_lat2)
    y = cos(rad_lat1) * sin(rad_lat2) - sin(rad_lat1) * cos(rad_lat2) * cos(dlon)
    bearing = degrees(atan2(y,x))

    return (bearing + 360) % 360


def get_hemisphere(lat, lon):
    """Return a human-readable hemisphere label for the coordinate."""
    ns = "Northern" if lat>0 else "Southern"
    ew = "Eastern" if lon>0 else "Western"
    return f"{ns} & {ew}"
