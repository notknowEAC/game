"""Load assets, data, and shared pygame resources."""

from pathlib import Path
import random

import pandas as pd
import pygame

from constants import SCREEN_SIZE

pygame.init()

# Window and clock used across screens.
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("GEOGUESS")

CLOCK = pygame.time.Clock()

# Resolve data and asset paths relative to repository root.
BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data" / "countries.csv"
ASSETS_PATH = BASE_PATH / "assets"

# Load country data and build lookup helpers.
DF = pd.read_csv(DATA_PATH)
COUNTRIES = DF.to_dict("records")
COUNTRY_BY_LOWER = {c["country"].lower(): c for c in COUNTRIES}
COUNTRY_NAMES_LOWER = [(c["country"], c["country"].lower()) for c in COUNTRIES]

# Load and scale background images.
BG_MENU = pygame.transform.scale(
    pygame.image.load(ASSETS_PATH / "bgmenu.jpg"), SCREEN_SIZE
)
BG_PLAY = pygame.transform.scale(
    pygame.image.load(ASSETS_PATH / "bgplay.jpg"), SCREEN_SIZE
)


def get_font(size: int):
    """Return a pygame font instance at the requested size."""
    return pygame.font.SysFont(None, size)


def random_country():
    """Pick a random country record from the dataset."""
    return random.choice(COUNTRIES)
