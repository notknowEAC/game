import math
import pygame

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
    mouse_pos,
):
    screen.fill((20, 25, 40))

    _draw_input_area(screen, font, big_font, input_text, suggestions)
    display_angle = _draw_compass(screen, font, current_bearing, display_angle)
    _draw_guess_history(screen, font, big_font, guess_history)
    _draw_hint_text(screen, font, hint_text)

    hint_button.changeColor(mouse_pos)
    hint_button.update(screen)
    return display_angle


def _draw_input_area(screen, font, big_font, input_text, suggestions):
    input_surface = big_font.render("this country? :" + input_text, True, (255, 255, 255))
    screen.blit(input_surface, (50, 50))

    y_offset = 100
    for suggestion in suggestions[:5]:
        text_surface = font.render(suggestion, True, (200, 200, 100))
        screen.blit(text_surface, (50, y_offset))
        y_offset += 30


def _draw_compass(screen, font, current_bearing, display_angle):
    compass_center = (450, 320)
    compass_radius = 110

    pygame.draw.circle(screen, (40, 50, 70), compass_center, compass_radius)
    pygame.draw.circle(screen, (200, 200, 200), compass_center, compass_radius, 3)

    for degree in range(0, 360, 10):
        rad = math.radians(degree)
        x1 = compass_center[0] + math.cos(rad) * compass_radius
        y1 = compass_center[1] + math.sin(rad) * compass_radius
        length = 18 if degree % 30 == 0 else 8
        x2 = compass_center[0] + math.cos(rad) * (compass_radius - length)
        y2 = compass_center[1] + math.sin(rad) * (compass_radius - length)
        pygame.draw.line(screen, (200, 200, 200), (x1, y1), (x2, y2), 2)

    directions = [("S", 90), ("E", 0), ("N", 270), ("W", 180)]
    for text, degree in directions:
        rad = math.radians(degree)
        x = compass_center[0] + math.cos(rad) * (compass_radius - 30)
        y = compass_center[1] + math.sin(rad) * (compass_radius - 30)
        label = font.render(text, True, (255, 255, 255))
        screen.blit(label, label.get_rect(center=(x, y)))

    if current_bearing is not None:
        diff = (current_bearing - display_angle + 540) % 360 - 180
        display_angle += diff * 0.08

        rad = math.radians(display_angle)
        x = compass_center[0] + math.sin(rad) * 100
        y = compass_center[1] - math.cos(rad) * 100
        pygame.draw.line(screen, (255, 0, 0), compass_center, (x, y), 6)

        back = math.radians(display_angle + 180)
        bx = compass_center[0] + math.sin(back) * 50
        by = compass_center[1] - math.cos(back) * 50
        pygame.draw.line(screen, (255, 255, 255), compass_center, (bx, by), 4)

        pygame.draw.circle(screen, (255, 255, 255), compass_center, 6)

    return display_angle


def _draw_guess_history(screen, font, big_font, guess_history):
    pygame.draw.rect(screen, (50, 50, 70), (600, 50, 350, 500))
    panel_title = big_font.render("Guesses", True, (255, 255, 255))
    screen.blit(panel_title, (700, 60))

    y_offset = 120
    for guess, distance, direction in guess_history[-10:]:
        line = f"{guess} | {distance} km | {direction}"
        line_surface = font.render(line, True, (255, 255, 255))
        screen.blit(line_surface, (620, y_offset))
        y_offset += 30


def _draw_hint_text(screen, font, hint_text):
    if hint_text != "":
        hint_surface = font.render(hint_text, True, (255, 255, 0))
        screen.blit(hint_surface, (600, 200))