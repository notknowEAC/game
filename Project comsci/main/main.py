from math import asin, radians, sin, cos, sqrt, atan2, degrees
from direction import get_direction, compress_get_bearing
from distance import haversine
from pathlib import Path
import pandas as pd
import pygame
import sys
import random
import csv

pygame.init()

screen = pygame.display.set_mode((1920 ,1080))
pygame.display.set_caption("เกมทายประทาศจากเข็มทิศ")
font = pygame.font.SysFont(None,28)
big_font = pygame.font.SysFont(None,40)
#icon = pygame.image.load()
#pygame.display.set_icon(icon)

#รายชื่อประเทศทั้งหมด (Country Data) เก็บเป็น(ละติจูด,ลองติจูด)
data_path = Path(__file__).resolve().parent / "data" / "countries.csv"
df = pd.read_csv(data_path)

#random country
random_country = df.sample(n=1).iloc[0]

#เก็บคำใบ้ของแต่ละประเทศ (โดยมีคำใบ้เกี่ยว ทวีปที่อยู่ ,ขึ้นต้นด้วยอะไร)
country_hint = {}
hint_text = ""

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
                guess = input_text.lower()#user input
                if guess in df["name"].str.lower().values:
                    count += 1
                    if guess == random_country["name"].lower():
                        message = f""
                    else:
                        lat1, lon1 = df[df["name"].str.lower() == guess].iloc[0][["latitude", "longitude"]]
                        lat2, lon2 = random_country[["latitude", "longitude"]]
                        disstance = round(haversine(lat1, lon1,lat2,lon2))
                        direction = get_direction(compress_get_bearing(lat1, lon1,lat2,lon2))
                        guess_history.append((guess, disstance, direction))
                        current_bearing = compress_get_bearing(lat1, lon1,lat2,lon2)
                        message  =""
                else:
                    message = ""
                input_text = ""
            elif event.key == null:
                hint_tyep = random.choice([])
                lat, lon = random_country[["latitude", "longitude"]]
        elif event.key == pygame.K_BACKSPACE:
            input_text = input_text[:-1]
        else:
            input_text += event.unicode
    #ค้นหาชื่อประเทศตามตัวอักษร
    suggestions = [c for c in df["name"].str.lower().values if c.startswith(input_text.lower())]

    #input 
    input_surface = big_font.render("Whis country? :" + input_text,True,(255,255,255))
    screen.blit(input_surface, (50,50))