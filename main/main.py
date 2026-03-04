from pathlib import Path
import pandas as pd
import pygame
import math
import sys
import random
import button
from direction import get_direction, compress_get_bearing, get_hemisphere
from distance import haversine

pygame.init()

screen = pygame.display.set_mode((1080 ,900))
pygame.display.set_caption("เกมทายประทาศจากเข็มทิศ")
font = pygame.font.SysFont(None,28)
big_font = pygame.font.SysFont(None,40)
clock = pygame.time.Clock()
#icon = pygame.image.load()
#pygame.display.set_icon(icon)

#รายชื่อประเทศทั้งหมด (Country Data) เก็บเป็น(ละติจูด,ลองติจูด)
data_path = Path(__file__).resolve().parent.parent / "data" / "countries.csv"
df = pd.read_csv(data_path)

# country_name = sorted(countries.keys())

#random country
random_country = df.sample(1).iloc[0]

#เก็บคำใบ้ของแต่ละประเทศ (โดยมีคำใบ้เกี่ยว ทวีปที่อยู่ ,ขึ้นต้นด้วยอะไร)
country_hint = {
    "thailand": {"continent": "Asia"},
    "japan": {"continent": "Asia"},
    "france": {"continent": "Europe"},
    "brazil": {"continent": "South America"},
    "canada": {"continent": "North America"}
}

hint_text = ""
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

hint_button = button.Button(image=None,pos=(640,250),text_input="HINT",font=button_font,base_color=(255,255,255),hovering_color=(255,0,0))


running = True
while running:
    #กำหนดสี
    screen.fill((20,25,40))
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:#enter to submit
                guess = df[df["name"].str.lower() == input_text.lower()].iloc[0] if not df[df["name"].str.lower() == input_text.lower()].empty else None

                if guess is not None:
                    count += 1
                    if guess["name"].lower() == random_country["name"].lower():
                        message = f"Correct! {random_country['name']}"
                    else:
                        lat1, lon1 = guess["latitude"], guess["longitude"]
                        lat2, lon2 = random_country["latitude"], random_country["longitude"]
                        disstance = round(haversine(lat1, lon1,lat2,lon2))
                        bearing = compress_get_bearing(lat1, lon1, lat2, lon2)
                        direction = get_direction(bearing)
                        continent = country_hint.get(random_country["name"].lower(), {}).get("continent", "Unknown")
                        hemisphere = get_hemisphere(lat2,lon2)

                        guess_history.append((guess["name"], disstance, direction))
                        current_bearing = compress_get_bearing(lat1, lon1,lat2,lon2)
                        message = f"{direction} | {disstance} km | {hemisphere} | {continent}"
                else:
                    message = "Country not found"
                input_text = ""

            elif event.key == pygame.K_BACKSPACE:#backspace to delete
                input_text = input_text[:-1]
            else:#add character to input
                input_text += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            if hint_button.checkForInput(mouse_pos):#press hint button

                if hint_count < max_hints:
                    lat, lon = random_country["latitude"], random_country["longitude"]

                    if hint_count == 0:
                        hint_text = f"Hint 1: {get_hemisphere(lat, lon)} Hemisphere"

                    elif hint_count == 1:
                        hint_text = f"Hint 2: Continent = {country_hint.get(random_country['name'].lower(), {}).get('continent', 'Unknown')}"

                    elif hint_count == 2:
                        hint_text = f"Hint 3: Starts with '{random_country['name'].upper()[0]}'"

                    hint_count += 1
            else:
                hint_text = "No more hints!"

    #ค้นหาชื่อประเทศตามตัวอักษร
    suggestions = [c for c in df["name"] if c.lower().startswith(input_text.lower())]

    #input 
    input_surface = big_font.render("this country? :" + input_text,True,(255,255,255))
    screen.blit(input_surface, (50,50))

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