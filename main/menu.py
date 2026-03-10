"""Menu screens and rules UI."""

import sys

import pygame

import button
from constants import COLOR_BORDER, COLOR_PANEL, COLOR_TEXT, COLOR_TITLE
from game import play
from resources import BG_MENU, SCREEN, get_font


def rules():
    """Render the rules screen and return to the menu on BACK."""
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
        "8. Total number of guesses will be displayed.",
    ]

    title_font = get_font(90)
    text_font = get_font(32)
    back_font = get_font(50)
    back = button.Button(
        image=None,
        pos=(120, 40),
        text_input="BACK",
        font=back_font,
        base_color="White",
        hovering_color="Green",
    )

    while True:
        SCREEN.blit(BG_MENU, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        panel = pygame.Surface((1100, 600))
        panel.set_alpha(170)
        panel.fill((20, 20, 30))
        SCREEN.blit(panel, (90, 70))

        pygame.draw.rect(SCREEN, (230, 230, 230), (90, 70, 1100, 600), 4, border_radius=20)

        title = title_font.render("GAME RULES", True, COLOR_TITLE)
        SCREEN.blit(title, title.get_rect(center=(640, 140)))

        y = 200
        for line in rules_text:
            text_surface = text_font.render(line, True, COLOR_TEXT)
            SCREEN.blit(text_surface, (140, y))
            y += 36

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
    """Render the main menu and route to play/rules/quit."""
    title_font = get_font(100)
    menu_font = get_font(70)

    play_button = button.Button(
        image=None,
        pos=(640, 250),
        text_input="PLAY",
        font=menu_font,
        base_color="#d7fcd4",
        hovering_color="White",
    )
    rules_button = button.Button(
        image=None,
        pos=(640, 400),
        text_input="RULES",
        font=menu_font,
        base_color="#d7fcd4",
        hovering_color="White",
    )
    quit_button = button.Button(
        image=None,
        pos=(640, 550),
        text_input="QUIT",
        font=menu_font,
        base_color="#d7fcd4",
        hovering_color="White",
    )

    while True:
        SCREEN.blit(BG_MENU, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        pygame.draw.rect(SCREEN, COLOR_PANEL, (220, 10, 840, 160), border_radius=40)

        title = title_font.render("GEOGUESS", True, COLOR_TITLE)
        SCREEN.blit(title, title.get_rect(center=(640, 100)))

        pygame.draw.rect(SCREEN, COLOR_PANEL, (490, 210, 300, 80), border_radius=20)
        pygame.draw.rect(SCREEN, COLOR_PANEL, (490, 360, 300, 80), border_radius=20)
        pygame.draw.rect(SCREEN, COLOR_PANEL, (490, 510, 300, 80), border_radius=20)

        for b in [play_button, rules_button, quit_button]:
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
