import pygame
import random
pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW_CAPTION = "Sprite Collision Game"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
PLAYER_SPRITE_FILENAME = "spaceship.png"
ENEMY_SPRITE_FILENAME = "alien.png"
PLAYER_SIZE = (50, 50)
ENEMY_SIZE = (40, 40)
PLAYER_SPEED = 5
NUM_ENEMIES = 7
score = 0
SCORE_FONT_SIZE = 36
SCORE_COLOR = WHITE
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        original_image = pygame.image.load(PLAYER_SPRITE_FILENAME).convert_alpha()
        self.image = pygame.transform.scale(original_image, PLAYER_SIZE)
        self.image = pygame.Surface(PLAYER_SIZE)
        self.image.fill(RED)        
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 20
        self.speed = PLAYER_SPEED
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        original_image = pygame.image.load(ENEMY_SPRITE_FILENAME).convert_alpha()
        self.image = pygame.transform.scale(original_image, ENEMY_SIZE)
        self.image = pygame.Surface(ENEMY_SIZE)
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ENEMY_SIZE[0], WINDOW_WIDTH - ENEMY_SIZE[0])
        self.rect.y = random.randrange(ENEMY_SIZE[1], WINDOW_HEIGHT - ENEMY_SIZE[1] - 50)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(WINDOW_CAPTION)
score_font = pygame.font.Font(None, SCORE_FONT_SIZE)
all_sprites = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for _ in range(NUM_ENEMIES):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies_group.add(enemy)
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
    all_sprites.update()
    collided_enemies = pygame.sprite.spritecollide(player, enemies_group, True)
    if collided_enemies:
        score += len(collided_enemies)
        for _ in range(len(collided_enemies)):
            new_enemy = Enemy()
            all_sprites.add(new_enemy)
            enemies_group.add(new_enemy)
    screen.fill(GREEN)
    all_sprites.draw(screen)
    score_text_surface = score_font.render(f"Score: {score}", True, SCORE_COLOR)
    screen.blit(score_text_surface, (10, 10))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()