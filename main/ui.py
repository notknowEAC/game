import math
import pygame
import sys
from pathlib import Path
import pandas as pd
import button
from direction import get_direction, compress_get_bearing
from distance import haversine

pygame.init()

SCREEN = pygame.display.set_mode((1280,720))
pygame.display.set_caption("GEOGUESS")

clock = pygame.time.Clock()

#รายชื่อประเทศทั้งหมด (Country Data) เก็บเป็น(ละติจูด,ลองติจูด,ทวีป,ซีกโลก)
base_path = Path(__file__).resolve().parent.parent
data_path = base_path / "data" / "countries.csv"
assets = base_path / "assets"
df = pd.read_csv(data_path)

bg_menu = pygame.image.load(assets / "bgmenu.jpg")
bg_play = pygame.image.load(assets / "bgplay.jpg")
bg_menu = pygame.transform.scale(bg_menu, (1280,720))
bg_play = pygame.transform.scale(bg_play, (1280,720))

def get_font(size):
    return pygame.font.SysFont(None,size)

font = get_font(28)
big_font = get_font(40)

input_text = ""
guess_history = []
hint_text = ""
message = "Guess country"
current_bearing = None
display_angle = 0
count = 0

hint_count = 0
max_hints = 3

#random country
random_country = df.sample(1).iloc[0]


def draw_game_ui(
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
    back_button,
    mouse_pos,
    message,
):

    screen.blit(bg_play,(0,0))

    # Title background
    pygame.draw.rect(SCREEN,(30,30,50),(440,20,400,90),border_radius=25)

    title_font = pygame.font.SysFont(None,50)
    title = title_font.render("Guess The Country", True, (255,255,255))
    screen.blit(title, title.get_rect(center=(640,65)))

    # message
    msg_surface = font.render(message, True, (255,255,255))
    screen.blit(msg_surface,(50,40))

    # Input box
    pygame.draw.rect(screen,(40,40,60),(40,80,300,50),border_radius=10)
    text_surface = font.render(input_text,True,(255,255,255))
    screen.blit(text_surface,(60,95))

    label = font.render("Type country:",True,(200,200,200))
    screen.blit(label,(50,60))

    # Suggestions panel
    pygame.draw.rect(screen,(30,30,50),(40,150,300,220),border_radius=10)

    y_offset = 160
    for suggestion in suggestions[:6]:
        sug = font.render(suggestion,True,(200,200,100))
        screen.blit(sug,(60,y_offset))
        y_offset += 30

    # Compass
    display_angle = _draw_compass(screen,current_bearing,display_angle)

    # Guess history panel
    pygame.draw.rect(screen,(40,40,60),(880,150,360,420),border_radius=10)

    history_title = big_font.render("History",True,(255,255,255))
    screen.blit(history_title,(1020,130))

    y_offset = 180
    for guess,distance,direction in guess_history[-10:]:
        line = f"{guess} | {distance} km | {direction}"
        line_surface = font.render(line,True,(255,255,255))
        screen.blit(line_surface,(920,y_offset))
        y_offset += 40

    # Hint text
    if hint_text != "":
        pygame.draw.rect(screen,(30,30,30),(420,520,450,70),border_radius=12)
        pygame.draw.rect(screen,(255,255,255),(420,520,450,70),2,border_radius=12)

        hint_surface = font.render("Hint: " + hint_text, True, (255,255,0))
        screen.blit(hint_surface,(440,545))

    # Hint button
    pygame.draw.rect(SCREEN,(40,40,60),(40,620,160,60),border_radius=15)

    hint_button.changeColor(mouse_pos)
    hint_button.update(screen)

    # Back button
    pygame.draw.rect(SCREEN,(40,40,60),(1080,10,180,60),border_radius=12)
    back_button.changeColor(mouse_pos)
    back_button.update(screen)

    return display_angle


def _draw_input_area(screen,input_text,suggestions):

    text = big_font.render("Country : " + input_text,True,(255,255,255))
    screen.blit(text,(50,60))

    pygame.draw.rect(screen,(40,40,60),(40,100,260,170))

    y = 110
    for s in suggestions[:5]:
        surface = font.render(s,True,(200,200,100))
        screen.blit(surface,(50,y))
        y += 30


def _draw_compass(screen,current_bearing,display_angle):

    center = (640, 360)
    radius = 110

    pygame.draw.circle(screen,(40,50,70),center,radius)
    pygame.draw.circle(screen,(200,200,200),center,radius,3)

    for degree in range(0,360,10):
        rad = math.radians(degree-90)

        x1 = center[0] + math.cos(rad)*radius
        y1 = center[1] + math.sin(rad)*radius

        length = 18 if degree % 30 == 0 else 8

        x2 = center[0] + math.cos(rad)*(radius-length)
        y2 = center[1] + math.sin(rad)*(radius-length)

        pygame.draw.line(screen,(200,200,200),(x1,y1),(x2,y2),2)

    directions = [("N",0),("E",90),("S",180),("W",270)]

    for text,degree in directions:

        rad = math.radians(degree-90)

        x = center[0] + math.cos(rad)*(radius-30)
        y = center[1] + math.sin(rad)*(radius-30)

        label = font.render(text,True,(255,255,255))
        screen.blit(label,label.get_rect(center=(x,y)))

    if current_bearing is not None:

        diff = (current_bearing - display_angle + 540) % 360 - 180
        display_angle += diff * 0.08

        rad = math.radians(display_angle)

        x = center[0] + math.sin(rad)*100
        y = center[1] - math.cos(rad)*100

        pygame.draw.line(screen,(255,0,0),center,(x,y),6)

        back = math.radians(display_angle+180)

        bx = center[0] + math.sin(back)*50
        by = center[1] - math.cos(back)*50

        pygame.draw.line(screen,(255,255,255),center,(bx,by),4)

        pygame.draw.circle(screen,(255,255,255),center,6)

    return display_angle


def _draw_guess_history(screen,guess_history):

    pygame.draw.rect(screen,(50,50,70),(600,50,350,500))

    title = big_font.render("Guesses",True,(255,255,255))
    screen.blit(title,(700,60))

    y = 120

    for guess,distance,direction in guess_history[-10:]:

        line = f"{guess} | {distance} km | {direction}"
        surface = font.render(line,True,(255,255,255))

        screen.blit(surface,(620,y))

        y += 40


def _draw_hint_text(screen,hint_text):

    if hint_text != "":
        surface = font.render("Hint : " + hint_text,True,(255,255,0))
        screen.blit(surface,(600,200))

def play():

    global input_text, hint_text, display_angle, current_bearing
    global guess_history, hint_count, message, count, random_country

    input_text = ""
    guess_history = []
    hint_text = ""
    message = "Guess country"
    current_bearing = None
    display_angle = 0
    count = 0
    hint_count = 0

    random_country = df.sample(1).iloc[0]

    hint_button = button.Button(
    image=None,
    pos=(120,650),
    text_input="HINT",
    font=get_font(35),
    base_color=(255,255,255),
    hovering_color=(255,80,80)
)
    back_button = button.Button(
        image=None,pos=(1200,40),
        text_input="BACK",
        font=get_font(35),
        base_color=(255,255,255),
        hovering_color=(255,0,0)
)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    count += 1
                    guess = df[df["country"].str.lower()==input_text.lower()]
                    guess = guess.iloc[0] if not guess.empty else None

                    if guess is not None:
                        if guess["country"].lower() == random_country["country"].lower():
                            message = f"Correct! {random_country['country']}"

                        else:
                            lat1,lon1 = guess["lat"],guess["lon"]
                            lat2,lon2 = random_country["lat"],random_country["lon"]

                            distance = round(haversine(lat1,lon1,lat2,lon2))
                            bearing = compress_get_bearing(lat1,lon1,lat2,lon2)

                            direction = get_direction(bearing)

                            guess_history.append(
                                (guess["country"],distance,direction)
                            )

                            current_bearing = bearing
                    else:
                        message = "Country not found"

                    input_text = ""

                elif event.key == pygame.K_BACKSPACE:#backspace to delete
                    input_text = input_text[:-1]

                else:
                    input_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:#press hint button

                if hint_button.checkForInput(mouse_pos):

                    if hint_count < max_hints:

                        if hint_count == 0:
                            hint_text = f"{random_country['hemisphere']} Hemisphere"

                        elif hint_count == 1:
                            hint_text = f"Continent : {random_country['continent']}"

                        elif hint_count == 2:
                            hint_text = f"Starts with : {random_country['country'][0]}"

                        hint_count += 1

                    else:
                        hint_text = "No more hints"

                if back_button.checkForInput(mouse_pos):
                    return

        #ค้นหาชื่อประเทศตามตัวอักษร
        suggestions = [c for c in df["country"]if c.lower().startswith(input_text.lower())]

        display_angle = draw_game_ui(
            SCREEN,
            font,
            big_font,
            input_text,
            suggestions,
            guess_history,
            hint_text,
            current_bearing,
            display_angle,
            hint_button,
            back_button,
            mouse_pos,
            message
        )
        pygame.draw.rect(SCREEN,(30,30,50),(500,150,280,70),border_radius=20)

        count_surface = big_font.render(f"Guesses : {count}",True,(255,255,255))
        SCREEN.blit(count_surface,count_surface.get_rect(center=(640,185)))

        pygame.display.flip()
        clock.tick(60)


def rules():

    rules_text = [
        "1. The system randomly selects one target country.",
        "2. Type the name of a country and press ENTER to guess.",
        "3. If the guess is incorrect, the system will show:",
        "   - Distance (km) from your guess to the target country",
        "   - Direction of the target country (N, NE, E, SE, S, SW, W, NW)",
        "4. The compass shows the direction of the target country.",
        "5. Press HINT to receive clues (maximum 3 hints):",
        "   - Hemisphere",
        "   - Continent",
        "   - First letter of the country",
        "6. The history panel shows previous guesses.",
        "7. The game ends when the correct country is guessed.",
        "8. Total number of guesses will be displayed."
    ]

    while True:

        SCREEN.blit(bg_menu,(0,0))
        mouse_pos = pygame.mouse.get_pos()

        # กล่องพื้นหลังใหญ่
        panel = pygame.Surface((1100,600))
        panel.set_alpha(170)
        panel.fill((20,20,30))
        SCREEN.blit(panel,(90,70))

        # กรอบ
        pygame.draw.rect(SCREEN,(230,230,230),(90,70,1100,600),4,border_radius=20)

        # Title
        title = get_font(90).render("GAME RULES",True,"#b68f40")
        SCREEN.blit(title,title.get_rect(center=(640,140)))

        y = 200

        # ตัวหนังสือ
        for line in rules_text:
            text_surface = get_font(32).render(line,True,(255,255,255))
            SCREEN.blit(text_surface,(140,y))
            y += 36

        # ปุ่ม BACK ซ้ายบน
        back = button.Button(
            image=None,
            pos=(120,40),
            text_input="BACK",
            font=get_font(50),
            base_color="White",
            hovering_color="Green"
        )

        back.changeColor(mouse_pos)
        back.update(SCREEN)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.checkForInput(mouse_pos):
                    return

        pygame.display.update()

def main_menu():

    while True:
        SCREEN.blit(bg_menu,(0,0))

        mouse_pos = pygame.mouse.get_pos()

        pygame.draw.rect(SCREEN,(30,30,50),(220,10,840,160),border_radius=40)

        title = get_font(100).render("GUESS THE COUNTRY",True,"#b68f40")
        SCREEN.blit(title,title.get_rect(center=(640,100)))

        pygame.draw.rect(SCREEN,(40,40,60),(490,210,300,80),border_radius=20)
        pygame.draw.rect(SCREEN,(40,40,60),(490,360,300,80),border_radius=20)
        pygame.draw.rect(SCREEN,(40,40,60),(490,510,300,80),border_radius=20)

        play_button = button.Button(
            image=None,
            pos=(640,250),
            text_input="PLAY",
            font=get_font(70),
            base_color="#d7fcd4",
            hovering_color="White"
        )

        rules_button = button.Button(
            image=None,
            pos=(640,400),
            text_input="RULE",
            font=get_font(70),
            base_color="#d7fcd4",
            hovering_color="White"
        )

        quit_button = button.Button(
            image=None,
            pos=(640,550),
            text_input="QUIT",
            font=get_font(70),
            base_color="#d7fcd4",
            hovering_color="White"
        )

        for b in [play_button,rules_button,quit_button]:
            b.changeColor(mouse_pos)
            b.update(SCREEN)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if play_button.checkForInput(mouse_pos):
                    play()

                if rules_button.checkForInput(mouse_pos):
                    rules()

                if quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()