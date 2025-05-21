from m5stack import *
from m5stack import lcd
import math
import time

# Parameters
cx = 160
cy = 120
base_radius = 50
num_points = 30
angle_offset = 0
t = 0
valeur = 20

old_points = []

# Get radial points
def get_radial_oscillating_points(cx, cy, base_radius, num_points, t, angle_offset):
    points = []
    oscillation_factor = math.sin(t)
    for i in range(num_points):
        angle = (2 * math.pi / num_points) * i
        deformation = 10 * oscillation_factor * math.sin(5 * angle + t)
        radius = base_radius + deformation
        x = int(cx + radius * math.cos(angle + angle_offset))
        y = int(cy + radius * math.sin(angle + angle_offset))
        points.append((x, y))
    return points

# Get velocity
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
        return min(exp_val, 1.0)

lcd.clear(lcd.BLACK)

while True:
    # Optional: erase previous shape (if desired)
    if old_points:
        for i in range(len(old_points)):
            x1, y1 = old_points[i]
            x2, y2 = old_points[(i + 1) % len(old_points)]
            lcd.line(x1, y1, x2, y2, lcd.BLACK)  # Erase with background

    # New shape
    points = get_radial_oscillating_points(cx, cy, base_radius, num_points, t, angle_offset)
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        lcd.line(x1, y1, x2, y2, lcd.BLUE)

    old_points = points  # Save for next frame erase

    vitesse = get_vitesse(valeur)
    t += vitesse
    angle_offset += 0.01

    valeur = (valeur + 0.1) % 100

    wait_ms(30)  # 33 FPS approx
