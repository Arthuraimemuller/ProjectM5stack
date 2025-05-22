import pygame
import sys
import time
from datetime import datetime, timedelta
import requests
from io import BytesIO

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

# Load image from URL into Pygame surface
def load_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image_file = BytesIO(response.content)
        image = pygame.image.load(image_file).convert_alpha()
        return pygame.transform.scale(image, (24, 24))  # taille 24x24 px
    except Exception as e:
        print(f"Failed to load image from {url}: {e}")
        return pygame.Surface((24, 24))

# Icon URLs from OpenWeatherMap (exemple)
ICON_URLS = {
    "01": "https://openweathermap.org/img/wn/01d.png",
    "02": "https://openweathermap.org/img/wn/02d.png",
    "03": "https://openweathermap.org/img/wn/03d.png",
    "04": "https://openweathermap.org/img/wn/04d.png",
    "09": "https://openweathermap.org/img/wn/09d.png",
    "10": "https://openweathermap.org/img/wn/10d.png",
    "11": "https://openweathermap.org/img/wn/11d.png",
    "13": "https://openweathermap.org/img/wn/13d.png",
    "50": "https://openweathermap.org/img/wn/50d.png",
    "unknown": "https://openweathermap.org/img/wn/01d.png",  # fallback
}

# Preload icons to avoid downloading each frame
def preload_icons():
    icons = {}
    for code, url in ICON_URLS.items():
        icons[code] = load_image_from_url(url)
    return icons

icons = preload_icons()

# Dummy icons for buttons (replace by URLs or keep placeholders)
icon_home = pygame.Surface((24,24))
icon_outdoor = pygame.Surface((24,24))
icon_co2 = pygame.Surface((24,24))
icon_home.fill(GREEN)
icon_outdoor.fill(BLUE)
icon_co2.fill(YELLOW)

# Fonts
font_small = pygame.font.Font(FONT_NAME, 14)
font_medium = pygame.font.Font(FONT_NAME, 18)

def get_french_weekdays():
    jours = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
    today = datetime.now()
    weekdays = []
    for i in range(7):
        day = today + timedelta(days=i)
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
    prefix = icon_code[:2]
    return icons.get(prefix, icons["unknown"])

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

    # Line 3-5: forecast (descendu plus bas)
    weekdays = get_french_weekdays()
    for i in range(7):
        x = 10 + i * 40
        day = weekdays[i]
        temp = 20 + i  # exemple d'évolution des températures
        icon = "01d" if i % 2 == 0 else "03d"
        draw_label(day, x, 170, font_small)       # +20 px
        draw_label(f"{temp}°C", x, 190, font_small)  # +20 px
        screen.blit(icon_to_img_file(icon), (x - 10, 210))  # +20 px

    pygame.display.flip()
    clock.tick(1)
