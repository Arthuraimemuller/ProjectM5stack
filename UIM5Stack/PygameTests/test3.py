import pygame
import sys
import math

pygame.init()

screen = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
clock = pygame.time.Clock()

cx, cy = 300, 300
base_radius = 100
num_points = 60
angle_offset = 0
time = 0

def get_radial_oscillating_points(cx, cy, base_radius, num_points, time, angle_offset):
    points = []
    oscillation_factor = math.sin(time)
    for i in range(num_points):
        angle = (2 * math.pi / num_points) * i
        deformation = 10 * oscillation_factor * math.sin(5 * angle + time)
        radius = base_radius + deformation
        x = cx + radius * math.cos(angle + angle_offset)
        y = cy + radius * math.sin(angle + angle_offset)
        points.append((x, y))
    return points

def get_vitesse(valeur):
    min_vitesse = 0.005
    max_vitesse = 0.1
    norm = max(0, min(valeur / 100, 1))
    return min_vitesse + norm * (max_vitesse - min_vitesse)

valeur = 50  # Valeur initiale

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        elif event.type == pygame.MOUSEWHEEL:
            # event.y = +1 (molette vers le haut), -1 (vers le bas)
            valeur += event.y * 5  # change valeur par pas de 5
            valeur = max(0, min(valeur, 300))  # clamp entre 0 et 100

    screen.fill((0, 0, 0))
    cx, cy = screen.get_width() // 2, screen.get_height() // 2

    points = get_radial_oscillating_points(cx, cy, base_radius, num_points, time, angle_offset)
    pygame.draw.polygon(screen, (0, 150, 255), points, width=3)

    vitesse = get_vitesse(valeur)
    time += vitesse
    angle_offset += 0.01

    # Afficher la valeur à l'écran pour feedback
    font = pygame.font.SysFont(None, 24)
    text = font.render(f'Valeur (molette): {valeur}', True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
