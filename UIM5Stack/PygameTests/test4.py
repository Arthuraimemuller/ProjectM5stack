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
    seuil = 37

    if valeur <= seuil:
        norm = max(0, min(valeur / seuil, 1))
        return min_vitesse + norm * (max_vitesse - min_vitesse)
    else:
        k = 0.1
        exp_val = max_vitesse * math.exp(k * (valeur - seuil))
        return min(exp_val, 1.0)  # plafonne à 1.0

valeur = 20  # valeur initiale

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEWHEEL:
            valeur += event.y * 5  # changer par pas de 5
            valeur = max(0, min(valeur, 100))  # clamp entre 0 et 100

    screen.fill((0, 0, 0))
    cx, cy = screen.get_width() // 2, screen.get_height() // 2

    points = get_radial_oscillating_points(cx, cy, base_radius, num_points, time, angle_offset)
    pygame.draw.polygon(screen, (0, 150, 255), points, width=3)

    vitesse = get_vitesse(valeur)
    time += vitesse
    angle_offset += 0.01

    # Affichage de la valeur pour retour visuel
    font = pygame.font.SysFont(None, 24)
    text = font.render(f'Valeur (molette): {valeur}', True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
