import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_q, K_r 
import random
from os import listdir
import math

pygame.init()

FPS = pygame.time.Clock()

screen = width, height = 1280, 800
pos_over = math.modf(width/4)[1], math.modf(height/3)[1]
key_over = math.modf(width/4)[1], math.modf(height/2)[1]

BLACK = 0, 0, 0
#WHITE = 255, 255, 255
RED = 255, 0, 0
#GREEN = 0, 255, 0

player_size = 90, 40
enemy_size = 45, 20
bonus_size = 30, 60

font = pygame.font.SysFont('Verdana', 20)
font_over = pygame.font.SysFont('Verdana', 80)
#player_color = BLACK

main_surface = pygame.display.set_mode(screen)

IMGS_PATH = 'goose'

#player = pygame.Surface((20, 20))
#player.fill((WHITE))
player_imgs = [pygame.transform.scale((pygame.image.load(IMGS_PATH + '/' + file).convert_alpha()), player_size) for file in listdir(IMGS_PATH)]
player = player_imgs[0]
player_rect = player.get_rect()
player_speed = 5

def create_enemy():
    #enemy = pygame.Surface((20, 20))
    #enemy.fill((RED))
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), enemy_size)
    enemy_rect = pygame.Rect(width, random.randint(0, height - enemy.get_size()[1]), *enemy.get_size())
    enemy_speed = random.randint(3, 6)
    return [enemy, enemy_rect, enemy_speed]

def create_bonus():
    #bonus = pygame.Surface((20, 20))
    #bonus.fill((GREEN))
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), bonus_size)
    bonus_rect = pygame.Rect(random.randint(0, width - bonus.get_size()[0]), 0, *bonus.get_size())
    bonus_speed = random.randint(2, 5)
    return [bonus, bonus_rect, bonus_speed]

bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 2

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 2500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3500)

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

img_index = 0           # Індекс картинки з гусаком 
img_sign = 1            # Напрямок перебору картинок
scores = 0              # Кількість бонусів, які зловили
is_gameover = False

enemies = []
bonuses = []

is_working = True

while is_working:
    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if not is_gameover:
            if event.type == CREATE_ENEMY:
                enemies.append(create_enemy())

            if event.type == CREATE_BONUS:
                bonuses.append(create_bonus())

            if event.type == CHANGE_IMG:
                if img_sign < 0 and img_index == 0 or img_sign > 0 and img_index == len(player_imgs)-1:
                    img_sign = -img_sign        # Змінюємо напрямок перебору картинок
                img_index += img_sign #1
                player = player_imgs[img_index]

    pressed_keys = pygame.key.get_pressed()

    #main_surface.fill(BLACK)
    #main_surface.blit(bg, (0, 0))
    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < -bg.get_width():
        bgX = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))

    main_surface.blit(font.render(str(scores), True, BLACK), (width - 30, 1))

    if is_gameover:
        main_surface.blit(font_over.render('GAME OVER', True, RED), pos_over)
        main_surface.blit(font.render('Press key "Q" to quit game', True, BLACK), key_over)
        main_surface.blit(font.render('Press key "R" to restart game', True, BLACK), (key_over[0], key_over[1]+40))

        if pressed_keys[K_q]:
            is_working = False
        elif pressed_keys[K_r]:
            scores = 0 
            is_gameover = False
            player = player_imgs[0]
            player_rect = player.get_rect()
            continue

    else:
        main_surface.blit(player, player_rect)

        for enemy in enemies:
            enemy[1] = enemy[1].move(-enemy[2], 0)
            main_surface.blit(enemy[0], enemy[1])

            if enemy[1].left < -enemy[0].get_width():
                enemies.pop(enemies.index(enemy))

            if player_rect.colliderect(enemy[1]):
                #enemies.pop(enemies.index(enemy))
                is_gameover = True
                enemies.clear()
                bonuses.clear()

        for bonus in bonuses:
            bonus[1] = bonus[1].move(0, bonus[2])
            main_surface.blit(bonus[0], bonus[1])

            if bonus[1].top > height:
                bonuses.pop(bonuses.index(bonus))

            if player_rect.colliderect(bonus[1]):
                bonuses.pop(bonuses.index(bonus))
                scores += 1

        if pressed_keys[K_DOWN] and player_rect.bottom < height:
            player_rect= player_rect.move(0, player_speed)

        if pressed_keys[K_UP]  and player_rect.top > 0:
            player_rect= player_rect.move(0, -player_speed)

        if pressed_keys[K_LEFT] and player_rect.left > 0:
            player_rect= player_rect.move(-player_speed, 0)

        if pressed_keys[K_RIGHT]  and player_rect.right < width:
            player_rect= player_rect.move(player_speed, 0)

    pygame.display.flip()