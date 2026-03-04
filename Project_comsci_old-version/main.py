import pygame
import math
import sys
import random
from button import Button

pygame.init()

screen = pygame.display.set_mode((1080 ,900))
pygame.display.set_caption("เกมทายประทาศจากเข็มทิศ")
font = pygame.font.SysFont(None,28)
big_font = pygame.font.SysFont(None,40)
clock = pygame.time.Clock()
#icon = pygame.image.load()
#pygame.display.set_icon(icon)

#รายชื่อประเทศทั้งหมด (Country Data) เก็บเป็น(ละติจูด,ลองติจูด)
countries = {
    "thailand": (13.7563, 100.5018),
    "japan": (35.6762, 139.6503),
    "france": (48.8566, 2.3522),
    "brazil": (-15.7939, -47.8828),
    "canada": (45.4215, -75.6972)
}

country_name = sorted(countries.keys())

#random country
random_country = random.choice(country_name)

#เก็บคำใบ้ของแต่ละประเทศ (โดยมีคำใบ้เกี่ยว ทวีปที่อยู่ ,ขึ้นต้นด้วยอะไร)
country_hint = {
    "thailand": {"continent": "Asia"},
    "japan": {"continent": "Asia"},
    "france": {"continent": "Europe"},
    "brazil": {"continent": "South America"},
    "canada": {"continent": "North America"}
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

    a = math.sin(d_rad_lat/2)**2 + math.cos(rad_lat1) * math.cos(rad_lat2) * math.sin(d_rad_lon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R_earth * c

#function หาทิศทางของประเทศที่ระบบสุ่มไว้ เทียบกับ ประเทศที่เราทายว่าอยู่ทิศไหน
def get_direction(lat1, lon1, lat2, lon2):
    d_lat = lat2 - lat1
    d_lon = lon2 - lon1

    vertical = "North" if d_lat > 0 else "South"
    horizontal = "East" if d_lon > 0 else "West"

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

    bearing = math.degrees(math.atan2(x,y))
    return (bearing + 360) % 360

def get_hemisphere(lat, lon):
    ns = "Northern" if lat>0 else "Southern"
    ew = "Eastern" if lon>0 else "Western"
    return f"{ns} & {ew}"

current_bearing = None
input_text = ""
guess_history = []
count = 0
message = "Guess country"
hint_text = ""
display_angle = 0
hint_count = 0
max_hints = 3
#Button
button_font = pygame.font.SysFont(None, 40)

hint_button = Button(image=None,pos=(640,250),text_input="HINT",font=button_font,base_color=(255,255,255),hovering_color=(255,0,0))


running = True
while running:
    #กำหนดสี
    screen.fill((20,25,40))
    mouse_pos = pygame.mouse.get_pos()

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
                        continent = country_hint[random_country]["continent"]
                        hemisphere = get_hemisphere(lat2,lon2)

                        guess_history.append((guess, disstance, direction))
                        current_bearing = compress_get_bearing(lat1, lon1,lat2,lon2)
                        message  =""
                else:
                    message = ""
                input_text = ""

            
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            if hint_button.checkForInput(mouse_pos):

                if hint_count < max_hints:
                    lat, lon = countries[random_country]

                    if hint_count == 0:
                        hint_text = f"Hint 1: {get_hemisphere(lat, lon)} Hemisphere"

                    elif hint_count == 1:
                        hint_text = f"Hint 2: Continent = {country_hint[random_country]['continent']}"

                    elif hint_count == 2:
                        hint_text = f"Hint 3: Starts with '{random_country[0].upper()}'"

                    hint_count += 1

            else:
                hint_text = "No more hints!"

    #ค้นหาชื่อประเทศตามตัวอักษร
    suggestions = [c for c in country_name if c.startswith(input_text.lower())]

    #input 
    input_surface = big_font.render("Whis country? :" + input_text,True,(255,255,255))
    screen.blit(input_surface, (50,50))

    #
    y_offset = 100
    for s in suggestions[:5]:
        text_surface = font.render(s,True, (200,200,100))
        screen.blit(text_surface, (50, y_offset))
        y_offset += 30
    
    compass_center = (450 ,320)
    compass_radius = 110

    pygame.draw.circle(screen, (40,50,70), compass_center ,compass_radius)
    pygame.draw.circle(screen, (200,200,200),compass_center,compass_radius,3)

    for i in range(0 ,360, 10):
        rad = math.radians(i)
        x1 = compass_center[0] + math.cos(rad) * compass_radius
        y1 = compass_center[1] + math.sin(rad) * compass_radius
        length = 18 if i%30 == 0 else 8
        x2 = compass_center[0] + math.cos(rad) * (compass_radius - length)
        y2 = compass_center[1] + math.sin(rad) * (compass_radius - length)
        pygame.draw.line(screen, (200,200,200), (x1,y1),(x2,y2),2)

    directions = [("S",90),("E",0),("N",270),("W",180)]
    for text, deg in directions:
        rad = math.radians(deg)
        x = compass_center[0] + math.cos(rad)*(compass_radius-30)
        y = compass_center[1] + math.sin(rad)*(compass_radius-30)
        label = font.render(text,True,(255,255,255))
        screen.blit(label, label.get_rect(center=(x,y)))

    if current_bearing is not None:
        diff = (current_bearing - display_angle + 540) % 360 - 180
        display_angle += diff * 0.08

        rad = math.radians(display_angle)

        x = compass_center[0] + math.sin(rad) * 100
        y = compass_center[1] - math.cos(rad) * 100
        pygame.draw.line(screen, (255,0,0), compass_center, (x,y), 6)

        back = math.radians(display_angle + 180)
        bx = compass_center[0] + math.sin(back)*50
        by = compass_center[1] - math.cos(back)*50
        pygame.draw.line(screen, (255,255,255), compass_center, (bx,by), 4)

        pygame.draw.circle(screen, (255,255,255), compass_center, 6)

    #render ประวัติ
    pygame.draw.rect(screen, (50,50,70),(600,50,350,500))
    panel_title = big_font .render("Guesses",True,(255,255,255))
    screen.blit(panel_title, (700,60))

    y_offset = 120
    for guess, dist, direction in guess_history[-10:]:
        line = f"{guess} | {dist} km | {direction}"
        line_surface = font.render(line,True,(255,255,255))
        screen.blit(line_surface, (620,y_offset))
        y_offset +=30
    
    if hint_text != "":
        hint_surface = font.render(hint_text, True, (255,255,0))
        screen.blit(hint_surface, (600, 200))
    hint_button.changeColor(mouse_pos)
    hint_button.update(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()