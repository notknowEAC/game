"""Rendering helpers for the main game UI."""

import math

import pygame

from constants import (
    COLOR_BORDER,
    COLOR_HINT,
    COLOR_LABEL,
    COLOR_PANEL,
    COLOR_PANEL_DARK,
    COLOR_SUGGESTION,
    COLOR_TEXT,
    MAX_HISTORY,
    MAX_SUGGESTIONS,
)
from resources import BG_PLAY, SCREEN, get_font
from text_utils import draw_wrapped_text, truncate_text

FONT_SMALL = get_font(28)
FONT_MED = get_font(40)
FONT_GAME_TITLE = get_font(50)


def draw_game_ui(state, suggestions, hint_button, back_button, mouse_pos):
    """Draw the play screen and return the updated compass display angle."""
    screen = SCREEN

    # Background and title banner.
    screen.blit(BG_PLAY, (0, 0))

    pygame.draw.rect(SCREEN, COLOR_PANEL_DARK, (440, 20, 400, 90), border_radius=25)

    title = FONT_GAME_TITLE.render("Guess The Country", True, COLOR_TEXT)
    screen.blit(title, title.get_rect(center=(640, 65)))

    # Status message and input field.
    safe_message = truncate_text(FONT_SMALL, state.message, 360)
    msg_surface = FONT_SMALL.render(safe_message, True, COLOR_TEXT)
    screen.blit(msg_surface, (50, 40))

    pygame.draw.rect(screen, COLOR_PANEL, (40, 80, 300, 50), border_radius=10)
    safe_input_text = truncate_text(FONT_SMALL, state.input_text, 250)
    text_surface = FONT_SMALL.render(safe_input_text, True, COLOR_TEXT)
    screen.blit(text_surface, (60, 95))

    label = FONT_SMALL.render("Type country:", True, COLOR_LABEL)
    screen.blit(label, (50, 60))

    # Autocomplete suggestions panel.
    pygame.draw.rect(screen, COLOR_PANEL_DARK, (40, 150, 300, 220), border_radius=10)

    y_offset = 160
    for suggestion in suggestions[:MAX_SUGGESTIONS]:
        sug = FONT_SMALL.render(suggestion, True, COLOR_SUGGESTION)
        screen.blit(sug, (60, y_offset))
        y_offset += 30

    # Compass visualization.
    display_angle = _draw_compass(screen, state.current_bearing, state.display_angle)

    # Guess history panel.
    history_rect = pygame.Rect(860, 150, 380, 420)
    pygame.draw.rect(screen, COLOR_PANEL, history_rect, border_radius=10)

    history_title = FONT_MED.render("History", True, COLOR_TEXT)
    screen.blit(history_title, history_title.get_rect(center=(history_rect.centerx, 170)))

    y_offset = 205
    max_history_bottom = history_rect.bottom - 20
    for guess, distance, direction in state.guess_history[-MAX_HISTORY:]:
        line = f"{guess} | {distance} km | {direction}"
        used_height = draw_wrapped_text(
            screen,
            FONT_SMALL,
            line,
            COLOR_TEXT,
            history_rect.x + 20,
            y_offset,
            history_rect.width - 40,
            max_lines=2,
        )
        y_offset += used_height + 8
        if y_offset >= max_history_bottom:
            break

    # Hint banner when available.
    if state.hint_text:
        pygame.draw.rect(screen, COLOR_PANEL_DARK, (420, 520, 450, 70), border_radius=12)
        pygame.draw.rect(screen, COLOR_BORDER, (420, 520, 450, 70), 2, border_radius=12)
        draw_wrapped_text(
            screen,
            FONT_SMALL,
            "Hint: " + state.hint_text,
            COLOR_HINT,
            440,
            532,
            410,
            max_lines=2,
        )

    # Buttons.
    pygame.draw.rect(SCREEN, COLOR_PANEL, (40, 620, 160, 60), border_radius=15)
    hint_button.changeColor(mouse_pos)
    hint_button.update(screen)

    pygame.draw.rect(SCREEN, COLOR_PANEL, (1080, 10, 180, 60), border_radius=12)
    back_button.changeColor(mouse_pos)
    back_button.update(screen)

    # Guess counter.
    pygame.draw.rect(SCREEN, COLOR_PANEL_DARK, (500, 150, 280, 70), border_radius=20)
    count_surface = FONT_MED.render(f"Guesses : {state.count}", True, COLOR_TEXT)
    SCREEN.blit(count_surface, count_surface.get_rect(center=(640, 185)))

    return display_angle


def draw_win_popup(mouse_pos, win_again_button, win_exit_button):
    """Draw the win modal and update its buttons."""
    popup_rect = pygame.Rect(360, 260, 560, 220)
    pygame.draw.rect(SCREEN, COLOR_PANEL, popup_rect, border_radius=20)
    pygame.draw.rect(SCREEN, COLOR_BORDER, popup_rect, 2, border_radius=20)

    popup_text = FONT_MED.render("Correct!", True, COLOR_TEXT)
    SCREEN.blit(popup_text, popup_text.get_rect(center=(640, 310)))

    win_again_button.changeColor(mouse_pos)
    win_exit_button.changeColor(mouse_pos)
    win_again_button.update(SCREEN)
    win_exit_button.update(SCREEN)


def _draw_compass(screen, current_bearing, display_angle):
    """Draw a compass and ease the needle toward the target bearing."""
    center = (640, 360)
    radius = 110

    pygame.draw.circle(screen, (40, 50, 70), center, radius)
    pygame.draw.circle(screen, (200, 200, 200), center, radius, 3)

    for degree in range(0, 360, 10):
        rad = math.radians(degree - 90)

        x1 = center[0] + math.cos(rad) * radius
        y1 = center[1] + math.sin(rad) * radius

        length = 18 if degree % 30 == 0 else 8

        x2 = center[0] + math.cos(rad) * (radius - length)
        y2 = center[1] + math.sin(rad) * (radius - length)

        pygame.draw.line(screen, (200, 200, 200), (x1, y1), (x2, y2), 2)

    directions = [("N", 0), ("E", 90), ("S", 180), ("W", 270)]

    for text, degree in directions:
        rad = math.radians(degree)

        x = center[0] + math.sin(rad) * (radius - 30)
        y = center[1] - math.cos(rad) * (radius - 30)

        label = FONT_SMALL.render(text, True, COLOR_TEXT)
        screen.blit(label, label.get_rect(center=(x, y)))

    if current_bearing is not None:
        diff = (current_bearing - display_angle + 540) % 360 - 180
        display_angle += diff * 0.08

        rad = math.radians(display_angle)

        x = center[0] + math.sin(rad) * 100
        y = center[1] - math.cos(rad) * 100

        pygame.draw.line(screen, (255, 0, 0), center, (x, y), 6)

        back = math.radians(display_angle + 180)

        bx = center[0] + math.sin(back) * 50
        by = center[1] - math.cos(back) * 50

        pygame.draw.line(screen, (255, 255, 255), center, (bx, by), 4)
        pygame.draw.circle(screen, (255, 255, 255), center, 6)

    return display_angle
