import pygame
import random
import math
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
PLAYER_START_X = 370
PLAYER_START_Y = 380
ENEMY_START_Y_MIN = 50
ENEMY_START_Y_MAX = 150
ENEMY_SPEED_X = 4
ENEMY_SPEED_Y = 40
BULLET_SPEED_Y = 10
COLLISION_DISTANCE = 27
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load('background.jfif')
pygame.display.set_caption("Space Invader")
playerimg = pygame.image.load('Spaceship.avif')
playerX = PLAYER_START_X
playerY = PLAYER_START_Y
playerX_change = 0
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for _i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, SCREEN_WIDTH - 64))
    enemyY.append(random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX))
    enemyY_change.append(ENEMY_SPEED_Y)
    enemyX_change.append(ENEMY_SPEED_X)
    bulletimg = pygame.image.load('bullet.png')
    bulletx = 0
    bullety = PLAYER_START_Y
    bulletx_change = 0
    bullety_change = BULLET_SPEED_Y
    bullet_state = 'ready'
    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    textx = 10
    texty = 10
    over_font = pygame.font.Font('freesansbold.ttf', 64)
    def show_score(x, y):
        score = font.render("Score : " + str(score_value), True, (225, 225, 225))
        screen.blit(over_font, (200, 250))
    def player(x, y):
        screen.blit(playerimg, (x, y))
    def enemy(x, y, i):
        screen.blit(enemyimg[i], (x, y))
    def fire_bullet():
        global bullet_state
        bullet_state = "fire"
        screen.blit(bulletimg, (x + 16, y + 10))
    def iscollision(enemyX, enemyY, bulletx, bullety):
        distance = math.sqrt((enemyX - bulletx) ** 2 + (enemyY - bullety) ** 2)
        return distance < COLLISION_DISTANCE