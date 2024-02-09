import pygame
from pygame.constants import QUIT

pygame.init()
FPS = pygame.time.Clock()
HEIGHT = 800
WIDTH = 1200

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

player_size = (20, 20)
player = pygame.Surface(player_size)
player.fill(COLOR_WHITE)
player_rect = player.get_rect()
player_spead = [1, 1]

playing = True

while playing:
    FPS.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False

    main_display.fill(COLOR_BLACK)

    player_rect = player_rect.move(player_spead)

    if player_rect.bottom >= HEIGHT or player_rect.top <= 0:
        player_spead[1] = -player_spead[1]
    if player_rect.right >= WIDTH or player_rect.left <= 0:
        player_spead[0] = -player_spead[0]

    main_display.blit(player, player_rect)

    pygame.display.flip()
