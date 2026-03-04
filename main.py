import pygame
import math
import sys
import random

pygame.init()

screen = pygame.display.set_mode((1920 ,1080))
pygame.display.set_caption("เกมทายประทาศจากเข็มทิศ")
font = pygame.font.SysFont(None,28)
big_font = pygame.font.SysFont(None,40)
#icon = pygame.image.load()
#pygame.display.set_icon(icon)

#รายชื่อประเทศทั้งหมด (Country Data) เก็บเป็น(ละติจูด,ลองติจูด)
countries = {

}

country_name = sorted(countries.keys())

#random country
random_country = random.choice(country_name)

#เก็บคำใบ้ของแต่ละประเทศ (โดยมีคำใบ้เกี่ยว ทวีปที่อยู่ ,ขึ้นต้นด้วยอะไร)
country_hint = {

}

hint_text = ""

#function คำนวณส่วนระยะทางโดยใช้สมการ Haversine
#lat = ละติจูด , lon = ลองติจูด
def haversine(lat1,lon1,lat2,lon2):
    #d = 2R * arcsin( sqrt( sin²((lat2-lat1)/2) + cos(lat1)cos(lat2)sin²((lon2-lon1)/2) ) )
    R_earth = 6371 #km
    rad_lat1 = math.radians(lat1)
    rad_lat2 = math.radians(lat2)
    d_rad_lat = math.radians(lat2-lat1)
    d_rad_lon = math.radians(lon2-lon1)

    a = math.sin(d_rad_lat/2)**2 + math.cos(rad_lat1) * math.cos(rad_lat1) * math.cos(rad_lat2) * math.sin(d_rad_lon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R_earth * c

#function หาทิศทางของประเทศที่ระบบสุ่มไว้ เทียบกับ ประเทศที่เราทายว่าอยู่ทิศไหน
def get_direction(lat1, lon1, lat2, lon2):
    d_lat = lat2 - lat1
    d_lon = lon2 - lon1

    if d_lat > 0:
        vertical = "์North"
    else:
        "South"
    if d_lon > 0:
        horizontal = "East"
    else:
        "West"

    if abs(d_lat) < 1:
        return horizontal
    if abs(d_lon) < 1:
        return vertical
    
    return vertical + "-" + horizontal

#function คำนวณองศาของเข็มที่จะชี้
# θ = atan2(x,y)
# x=sin(Δλ)cos(ϕ2​)
# y=cos(ϕ1​)sin(ϕ2​)−sin(ϕ1​)cos(ϕ2​)cos(Δλ)
def compress_get_bearing(lat1, lon1, lat2, lon2):
    rad_lat1 = math.radians(lat1)
    rad_lat2 = math.radians(lat2)
    d_rad_lon = math.radians(lon2 - lon1)

    x = math.sin(d_rad_lon) * math.cos(rad_lat2)
    y = math.cos(rad_lat1) * math.sin(rad_lat2) - math.sin(rad_lat1) * math.cos(rad_lat2) * math.cos(d_rad_lon)

    bearing = math.degrees(math.atan2(y,x))
    return (bearing + 360) % 360

current_bearing = None


input_text = ""
guess_history = []
count = 0
message = "Guess country"

running = True
while running:
    #กำหนดสี
    screen.fill()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if  event.key == pygame.K_RETURN:
                guess = input_text.lower()
                if guess in countries:
                    count += 1
                    if guess == random_country:
                        message = f""
                    else:
                        lat1, lon1 = countries[guess]
                        lat2, lon2 = countries[random_country]
                        disstance = round(haversine(lat1, lon1,lat2,lon2))
                        direction = get_direction(lat1,lon1,lat2,lon2)
                        guess_history.append((guess, disstance, direction))
                        current_bearing = compress_get_bearing(lat1, lon1,lat2,lon2)
                        message  =""
                else:
                    message = ""
                input_text = ""
            elif event.key == null:
                hint_tyep = random.choice([])
                lat, lon = countries[random_country]

            
        elif event.key == pygame.K_BACKSPACE:
            input_text = input_text[:-1]
        else:
            input_text += event.unicode
    #ค้นหาชื่อประเทศตามตัวอักษร
    suggestions = [c for c in country_name if c.startswith(input_text.lower())]

    #input 
    input_surface = big_font.render("Whis country? :" + input_text,True,(255,255,255))
    screen.blit(input_surface, (50,50))

    #

    