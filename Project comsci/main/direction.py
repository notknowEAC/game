from math import atan2, cos, degrees, radians, sin

#function หาทิศทางของประเทศที่ระบบสุ่มไว้ เทียบกับ ประเทศที่เราทายว่าอยู่ทิศไหน
def get_direction(degrees):
    directions = ["North", "Northeast", "East", "Southeast", "South", "Southwest", "West", "Northwest  "]
    index = int((degrees + 22.5) // 45) % 8

    return directions[index]

#function คำนวณองศาของเข็มที่จะชี้
# θ = atan2(x,y)
# x=sin(Δλ)cos(ϕ2​)
# y=cos(ϕ1​)sin(ϕ2​)−sin(ϕ1​)cos(ϕ2​)cos(Δλ)
def compress_get_bearing(lat1, lon1, lat2, lon2):
    rad_lat1, rad_lat2, rad_lon1, rad_lon2 = map(radians, [lat1, lat2, lon1, lon2])
    dlon = rad_lon2 - rad_lon1

    x = sin(dlon) * cos(rad_lat2)
    y = cos(rad_lat1) * sin(rad_lat2) - sin(rad_lat1) * cos(rad_lat2) * cos(dlon)
    bearing = degrees(atan2(y,x))

    return (bearing + 360) % 360