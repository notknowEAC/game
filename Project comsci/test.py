import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 920, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("")
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()

# ----------------------
# Country Data (lat, lon)
# ----------------------
countries = {
    "thailand": (13.7563, 100.5018),
    "turkey": (39.9334, 32.8597),
    "tanzania": (-6.3690, 34.8888),
    "tunisia": (36.8065, 10.1815),
    "taiwan": (25.0330, 121.5654),
    "japan": (35.6762, 139.6503),
    "brazil": (-15.7939, -47.8828),
    "france": (48.8566, 2.3522)
}

country_names = sorted(countries.keys())

# Random target
import random
target_country = random.choice(country_names)

# Simple country info for hints
country_info = {
    "thailand": {"continent": "Asia"},
    "turkey": {"continent": "Asia/Europe"},
    "tanzania": {"continent": "Africa"},
    "tunisia": {"continent": "Africa"},
    "taiwan": {"continent": "Asia"},
    "japan": {"continent": "Asia"},
    "brazil": {"continent": "South America"},
    "france": {"continent": "Europe"}
}

hint_text = ""

# ----------------------
# Distance (Haversine)
# ----------------------
def haversine(lat1, lon1, lat2, lon2):
    # Haversine Formula
    # d = 2R * arcsin( sqrt( sin²((lat2-lat1)/2) + cos(lat1)cos(lat2)sin²((lon2-lon1)/2) ) )
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

# ----------------------
# Direction
# ----------------------
def get_direction(lat1, lon1, lat2, lon2):
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    vertical = "ทิศเหนือ" if dlat > 0 else "ทิศใต้"
    horizontal = "East" if dlon > 0 else "West"

    if abs(dlat) < 1:
        return horizontal
    if abs(dlon) < 1:
        return vertical

    return vertical + "-" + horizontal

# ----------------------
# Compass Angle
# ----------------------

def get_bearing(lat1, lon1, lat2, lon2):
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dlambda = math.radians(lon2 - lon1)

    x = math.sin(dlambda) * math.cos(phi2)
    y = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(dlambda)

    bearing = math.degrees(math.atan2(x, y))
    return (bearing + 360) % 360

current_bearing = None

# ----------------------
# Game State
# ----------------------
input_text = ""
guess_history = []
attempt_count = 0
message = "Guess the country!"

# ----------------------
# Main Loop
# ----------------------
running = True
while running:
    screen.fill((30, 30, 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                guess = input_text.lower()
                if guess in countries:
                    attempt_count += 1
                    if guess == target_country:
                        message = f"Correct! You found it in {attempt_count} attempts!"
                    else:
                        lat1, lon1 = countries[guess]
                        lat2, lon2 = countries[target_country]
                        distance = round(haversine(lat1, lon1, lat2, lon2), 2)
                        direction = get_direction(lat1, lon1, lat2, lon2)
                        guess_history.append((guess, distance, direction))
                        current_bearing = get_bearing(lat1, lon1, lat2, lon2)
                        message = "Wrong! Try again."
                else:
                    message = "Country not found."
                input_text = ""
            elif event.key == pygame.K_h:
                # Generate random hint
                hint_type = random.choice(["continent", "first_letter", "hemisphere"])
                lat, lon = countries[target_country]

                if hint_type == "continent":
                    hint_text = f"Hint: Continent = {country_info[target_country]['continent']}"
                elif hint_type == "first_letter":
                    hint_text = f"Hint: Starts with '{target_country[0].upper()}'"
                elif hint_type == "hemisphere":
                    ns = "Northern" if lat > 0 else "Southern"
                    ew = "Eastern" if lon > 0 else "Western"
                    hint_text = f"Hint: Located in {ns} & {ew} Hemisphere"

            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    # Suggestions (filter by prefix)
    suggestions = [c for c in country_names if c.startswith(input_text.lower())]

    # Draw Input
    input_surface = big_font.render("Input: " + input_text, True, (255,255,255))
    screen.blit(input_surface, (50, 50))

    # Draw Suggestions
    y_offset = 100
    for s in suggestions[:5]:
        text_surface = font.render(s, True, (200,200,100))
        screen.blit(text_surface, (50, y_offset))
        y_offset += 30

    # Draw Hint
    hint_surface = font.render(hint_text, True, (150,255,150))
    screen.blit(hint_surface, (50, 80))

    # Draw Attempt Counter
    attempt_surface = font.render(f"Attempts: {attempt_count}", True, (255,255,255))
    screen.blit(attempt_surface, (50, 20))

    # Draw Message
    msg_surface = font.render(message, True, (255,150,150))
    screen.blit(msg_surface, (50, HEIGHT - 50))

    # ----------------------
    # Draw Compass
    # ----------------------
    compass_center = (450, 320)
    compass_radius = 100

    pygame.draw.circle(screen, (200,200,200), compass_center, compass_radius, 2)
    pygame.draw.line(screen, (200,200,200), (450,220), (450,420), 1)
    pygame.draw.line(screen, (200,200,200), (350,320), (550,320), 1)

    n_text = font.render("N", True, (255,255,255))
    s_text = font.render("S", True, (255,255,255))
    e_text = font.render("E", True, (255,255,255))
    w_text = font.render("W", True, (255,255,255))

    screen.blit(n_text, (445, 200))
    screen.blit(s_text, (445, 425))
    screen.blit(e_text, (565, 310))
    screen.blit(w_text, (330, 310))

    if current_bearing is not None:
        angle_rad = math.radians(-current_bearing + 90)
        arrow_length = 90
        end_x = compass_center[0] + arrow_length * math.cos(angle_rad)
        end_y = compass_center[1] - arrow_length * math.sin(angle_rad)
        pygame.draw.line(screen, (255,0,0), compass_center, (end_x, end_y), 4)

    # ----------------------
    # Draw Guess History Panel
    pygame.draw.rect(screen, (50,50,70), (600, 50, 350, 500))
    panel_title = big_font.render("Guesses", True, (255,255,255))
    screen.blit(panel_title, (700, 60))

    y_offset = 120
    for guess, dist, direction in guess_history[-10:]:
        line = f"{guess} | {dist} km | {direction}"
        line_surface = font.render(line, True, (255,255,255))
        screen.blit(line_surface, (620, y_offset))
        y_offset += 30

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

#don't press H becaruse h is hint
