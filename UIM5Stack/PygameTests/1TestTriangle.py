import pygame
import sys
import time
from datetime import datetime, timedelta

# Constants
WIDTH, HEIGHT = 320, 240
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (144, 238, 144)
BLUE = (135, 206, 235)
YELLOW = (255, 215, 0)
RED = (255, 0, 0)
FONT_NAME = 'freesansbold.ttf'

# Init Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("M5Stack Simulator")
clock = pygame.time.Clock()

# Load placeholder images
def load_image(path):
    try:
        return pygame.image.load(path)
    except:
        return pygame.Surface((24, 24))

icon_home = load_image("res/home.png")
icon_outdoor = load_image("res/outdoor.png")
icon_co2 = load_image("res/co2.png")

# Fonts
font_small = pygame.font.Font(FONT_NAME, 14)
font_medium = pygame.font.Font(FONT_NAME, 18)

# Simulated forecast data (icon codes are from OpenWeatherMap)
forecast_cache = [("Mon", 22, "01d")] * 7

def get_french_weekdays():
    jours = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
    today = datetime.now()
    weekdays = []
    for i in range(7):
        day = today + timedelta(days=i)
        # weekday(): Monday=0 ... Sunday=6
        weekdays.append(jours[day.weekday()])
    return weekdays

def draw_label(text, x, y, font, color=BLACK):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def draw_button(text, x, y, w, h, color, text_color=WHITE, image=None):
    pygame.draw.rect(screen, color, (x, y, w, h))
    if image:
        screen.blit(image, (x + (w // 2 - 12), y - 35))
    lines = text.split("\n")
    for i, line in enumerate(lines):
        label = font_medium.render(line, True, text_color)
        screen.blit(label, (x + (w - label.get_width()) // 2, y + 20 + i * 20))

def icon_to_img_file(icon_code):
    if icon_code.startswith("01"): return load_image("res/sunny.png")
    if icon_code.startswith("02"): return load_image("res/partly_cloudy.png")
    if icon_code.startswith("03"): return load_image("res/cloudy.png")
    if icon_code.startswith("04"): return load_image("res/cloudy.png")
    if icon_code.startswith("09"): return load_image("res/shower_rain.png")
    if icon_code.startswith("10"): return load_image("res/rain.png")
    if icon_code.startswith("11"): return load_image("res/thunderstorm.png")
    if icon_code.startswith("13"): return load_image("res/snow.png")
    if icon_code.startswith("50"): return load_image("res/mist.png")
    return load_image("res/unknown.png")

# Main loop
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Line 1: datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw_label(now, 50, 5, font_small)

    # Line 2: buttons
    draw_button("22.5°C\n45%", 5, 60, 100, 140, GREEN, WHITE, icon_home)
    draw_button("18.7°C", 110, 60, 100, 140, BLUE, WHITE, icon_outdoor)
    draw_button("800 ppm", 215, 60, 100, 140, YELLOW, BLACK, icon_co2)

    # Label hello
    draw_label("Hello", 220, 10, font_medium, RED)

    # Line 3-5: forecast (déplacé un peu plus bas)
    weekdays = get_french_weekdays()
    for i in range(7):
        x = 10 + i * 40
        day = weekdays[i]
        temp = 20 + i  # juste un exemple d'évolution des températures
        icon = "01d" if i % 2 == 0 else "03d"
        draw_label(day, x, 150, font_small)
        draw_label(f"{temp}°C", x, 170, font_small)
        screen.blit(icon_to_img_file(icon), (x - 10, 190))

    pygame.display.flip()
    clock.tick(1)
