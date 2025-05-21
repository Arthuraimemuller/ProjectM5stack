import pygame
import sys
import math
import random

pygame.init()

screen = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
clock = pygame.time.Clock()

cx, cy = 300, 300
base_radius = 100
num_points = 150
time = 0

phases = [random.uniform(0, 2 * math.pi) for _ in range(10)]

def get_radial_oscillating_points(cx, cy, base_radius, num_points, time, amplitude):
    points = []
    oscillation_time = math.sin(time)
    for i in range(num_points):
        angle = (2 * math.pi / num_points) * i

        deformation = amplitude * oscillation_time * (
            0.4 * math.sin(1 * angle + phases[0]) +
            0.25 * math.sin(2 * angle + phases[1]) +
            0.15 * math.sin(3 * angle + phases[2]) +
            0.1 * math.sin(4 * angle + phases[3]) +
            0.05 * math.sin(5 * angle + phases[4])
        )
        radius = base_radius + deformation
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    return points

# Nouvelle fonction get_vitesse qui augmente doucement la vitesse max
def get_vitesse(valeur):
    min_vitesse = 0.005
    max_vitesse = 0.02  # plus bas pour une montée plus lente
    seuil = 37

    if valeur <= seuil:
        norm = max(0, min(valeur / seuil, 1))
        return min_vitesse + norm * (max_vitesse - min_vitesse)
    else:
        # limite la vitesse à max_vitesse
        return max_vitesse

valeur = 20

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEWHEEL:
            valeur += event.y * 5
            valeur = max(0, min(valeur, 100))

    screen.fill((0, 0, 0))
    cx, cy = screen.get_width() // 2, screen.get_height() // 2

    vitesse = get_vitesse(valeur)
    amplitude = 10 + valeur * 0.6  # amplitude qui augmente plus vite

    points = get_radial_oscillating_points(cx, cy, base_radius, num_points, time, amplitude)

    pygame.draw.polygon(screen, (0, 150, 255), points, width=3)

    time += vitesse

    font = pygame.font.SysFont(None, 24)
    text = font.render(f'Valeur (molette): {valeur}', True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
