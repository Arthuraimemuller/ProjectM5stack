import pygame
import sys
import math

pygame.init()

screen = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
clock = pygame.time.Clock()

cx, cy = 300, 300
base_radius = 100
num_points = 60
angle_offset = 0  # rotation globale
time = 0

def get_radial_oscillating_points(cx, cy, base_radius, num_points, time, angle_offset):
    points = []
    oscillation_factor = math.sin(time)  # oscille entre -1 et 1

    for i in range(num_points):
        angle = (2 * math.pi / num_points) * i

        # Amplitude de la déformation (max 30 pixels)
        deformation = 10 * oscillation_factor * math.sin(5 * angle + time)

        # Rayon modifié radialement
        radius = base_radius + deformation

        # Calcul des coordonnées du point sur le cercle déformé
        x = cx + radius * math.cos(angle + angle_offset)
        y = cy + radius * math.sin(angle + angle_offset)

        points.append((x, y))
    return points

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    screen.fill((0, 0, 0))

    cx, cy = screen.get_width() // 2, screen.get_height() // 2

    points = get_radial_oscillating_points(cx, cy, base_radius, num_points, time, angle_offset)

    pygame.draw.polygon(screen, (0, 150, 255), points, width=3)

    time += 0.03
    angle_offset += 0.01

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
