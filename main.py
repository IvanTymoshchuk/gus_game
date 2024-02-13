import random

import pygame
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP, QUIT

pygame.init()
FPS = pygame.time.Clock()
HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont("Verdana", 20)

bg = pygame.transform.scale(pygame.image.load("./img/background.png"), (WIDTH, HEIGHT))
bg_x = 0
bg_x2 = bg.get_width()
bg_move = 3

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)


main_display = pygame.display.set_mode((WIDTH, HEIGHT))

player_size = (15, 15)
player = pygame.image.load("./img/player.png").convert_alpha()
player_rect = player.get_rect()
player_rect.center = main_display.get_rect().center
player_move_down = [0, 4]
player_move_top = [0, -4]
player_move_right = [4, 0]
player_move_left = [-4, 0]


def create_enemy():
    enemy = pygame.image.load("./img/enemy.png").convert_alpha()
    enemy_width = enemy.get_height()
    enemy_rect = pygame.Rect(
        WIDTH, random.randint(enemy_width, HEIGHT - enemy_width), *enemy.get_size()
    )
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]


def create_bonus():
    bonus = pygame.image.load("./img/bonus.png").convert_alpha()
    bonus_width = bonus.get_width()
    bonus_rect = pygame.Rect(
        random.randint(bonus_width, WIDTH - bonus_width),
        -bonus_width,
        *bonus.get_size()
    )
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)

enemies = []
bonuses = []

score = 0

playing = True

while playing:
    FPS.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

    bg_x -= bg_move
    bg_x2 -= bg_move

    if bg_x < -bg.get_width():
        bg_x = bg.get_width()

    if bg_x2 < -bg.get_width():
        bg_x2 = bg.get_width()

    main_display.blit(bg, (bg_x, 0))
    main_display.blit(bg, (bg_x2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_top)
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(player, player_rect)
    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
