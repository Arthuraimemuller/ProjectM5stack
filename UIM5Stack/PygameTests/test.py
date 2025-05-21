import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((320, 240), pygame.RESIZABLE)
clock = pygame.time.Clock()

base_radius = 30
zoom = 1.0
zoom_step = 0.1
r = base_radius
dr = 1

def draw_neon_ring(surface, cx, cy, base_radius, color, layers=10):
    for i in range(layers):
        radius = int((base_radius + i) * zoom)
        alpha = max(10, 255 - i * 25)
        glow_color = (*color, alpha)
        s = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        pygame.draw.circle(s, glow_color, (cx, cy), radius, 1)
        surface.blit(s, (0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                zoom += zoom_step
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                zoom = max(0.1, zoom - zoom_step)  # limite zoom minimum

    screen.fill((0, 0, 0))

    cx, cy = screen.get_width() // 2, screen.get_height() // 2

    # Le cercle pulse autour du base_radius (avant zoom)
    r += dr
    if r > base_radius + 10 or r < base_radius - 10:
        dr *= -1

    draw_neon_ring(screen, cx, cy, r, (0, 0, 255))

    pygame.display.flip()
    clock.tick(30)
