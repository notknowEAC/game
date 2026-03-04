import pygame
import math
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Compass")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24, bold=True)

CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 200

angle = 0
target_angle = 0
input_text = ""

def draw_compass():
    pygame.draw.circle(screen, (30, 41, 59), CENTER, RADIUS)
    pygame.draw.circle(screen, (51, 65, 85), CENTER, RADIUS - 30)

    for i in range(360):
        rad = math.radians(i)
        x1 = CENTER[0] + math.cos(rad) * (RADIUS - 30)
        y1 = CENTER[1] + math.sin(rad) * (RADIUS - 30)

        if i % 30 == 0:
            length = 15
        elif i % 10 == 0:
            length = 8
        else:
            length = 3

        x2 = CENTER[0] + math.cos(rad) * (RADIUS - 30 - length)
        y2 = CENTER[1] + math.sin(rad) * (RADIUS - 30 - length)

        pygame.draw.line(screen, (200, 200, 200), (x1, y1), (x2, y2), 2)

    directions = [("N", 90), ("E", 0), ("S", 270), ("W", 180)]
    for text, deg in directions:
        rad = math.radians(deg)
        x = CENTER[0] + math.cos(rad) * (RADIUS - 60)
        y = CENTER[1] + math.sin(rad) * (RADIUS - 60)
        label = font.render(text, True, (255, 255, 255))
        rect = label.get_rect(center=(x, y))
        screen.blit(label, rect)

def draw_needle(angle):
    rad = math.radians(90 - angle)

    x = CENTER[0] + math.cos(rad) * 140
    y = CENTER[1] + math.sin(rad) * 140
    pygame.draw.line(screen, (255, 0, 0), CENTER, (x, y), 5)

    back_rad = math.radians(270 - angle)
    bx = CENTER[0] + math.cos(back_rad) * 50
    by = CENTER[1] + math.sin(back_rad) * 50
    pygame.draw.line(screen, (255, 255, 255), CENTER, (bx, by), 3)

running = True
while running:
    clock.tick(60)
    screen.fill((15, 23, 42))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                target_angle -= 5
            if event.key == pygame.K_RIGHT:
                target_angle += 5
            if event.key == pygame.K_RETURN:
                try:
                    target_angle = float(input_text)
                except:
                    pass
                input_text = ""
            elif event.unicode.isdigit():
                input_text += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]

    if abs(target_angle - angle) > 0.5:
        angle += (target_angle - angle) * 0.1

    draw_compass()
    draw_needle(angle)

    angle_text = font.render(f"Angle: {round(angle,1)}°", True, (255,255,255))
    input_display = font.render(f"Input: {input_text}", True, (200,200,200))
    screen.blit(angle_text, (20, 20))
    screen.blit(input_display, (20, 50))

    pygame.display.flip()

pygame.quit()
sys.exit()