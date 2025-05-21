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

        deformation = 0
        coefficients = [0.4, 0.25, 0.15, 0.1, 0.05, 0.03, 0.02, 0.015, 0.01, 0.005]

        for n in range(10):
            deformation += coefficients[n] * math.sin((n + 1) * angle + phases[n])

        deformation *= amplitude * oscillation_time
        radius = base_radius + deformation
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    return points

def get_vitesse(valeur):
    min_vitesse = 0.005
    base = 1.1  # facteur de croissance exponentielle
    seuil = 10

    if valeur <= seuil:
        norm = max(0, min(valeur / seuil, 1))
        return min_vitesse + norm * (0.015)  # croissance linéaire
    else:
        facteur = valeur - seuil
        return min_vitesse + 0.015 + (base ** facteur - 1) * 0.0005  # croissance exponentielle

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
    amplitude = 10 + valeur * 0.6

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
