from pathlib import Path
import pandas as pd
import pygame
import sys
import button
from direction import get_direction, compress_get_bearing, get_hemisphere
from distance import haversine
from ui import draw_game_ui

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

    display_angle = draw_game_ui(
        screen,
        font,
        big_font,
        input_text,
        suggestions,
        guess_history,
        hint_text,
        current_bearing,
        display_angle,
        hint_button,
        mouse_pos,
    )
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()