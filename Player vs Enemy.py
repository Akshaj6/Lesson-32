import pygame
import sys
import random

# 1. SETUP
# ===================================================
pygame.init()

# Screen settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Your Background and Player")

# Colors (Only for things that AREN'T images)
WHITE = (255, 255, 255) # For the score text
BLUE = (0, 0, 255)      # For the simple enemy squares

# Game variables
player_speed = 7
score = 0
font = pygame.font.Font(None, 50)
clock = pygame.time.Clock()

# 2. LOAD YOUR IMAGES
# ===================================================
# This loads "background.png" from your folder and resizes it to fit the screen.
background_image = pygame.transform.scale(
    pygame.image.load("Background.png").convert(),
    (WINDOW_WIDTH, WINDOW_HEIGHT)
)

# 3. CREATE THE SPRITES
# ===================================================
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # This loads "player.png" from your folder.
        original_image = pygame.image.load("alien.png").convert_alpha()
        
        # We resize your player image to be 50x50 pixels.
        self.image = pygame.transform.scale(original_image, (50, 50))
        
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= player_speed
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += player_speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= player_speed
        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += player_speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Enemies are still simple blue squares
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(
            center=(random.randint(20, WINDOW_WIDTH - 20), random.randint(20, WINDOW_HEIGHT - 100))
        )

# 4. CREATE GROUPS AND OBJECTS
# ===================================================
all_sprites = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(7):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies_group.add(enemy)

# 5. GAME LOOP
# ===================================================
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    all_sprites.update()

    collided_enemies = pygame.sprite.spritecollide(player, enemies_group, True)
    if collided_enemies:
        score += len(collided_enemies)
        for i in range(len(collided_enemies)):
            new_enemy = Enemy()
            all_sprites.add(new_enemy)
            enemies_group.add(new_enemy)

    # DRAW EVERYTHING
    # ===============================================
    # Step 1: Draw your background image first.
    screen.blit(background_image, (0, 0))
    
    # Step 2: Draw all the sprites (player and enemies) on top of the background.
    all_sprites.draw(screen)
    
    # Step 3: Draw the score text on top of everything.
    score_text = font.render(f"SCORE: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    # ===============================================

    pygame.display.flip()
    clock.tick(60)

# 6. QUIT
# ===================================================
pygame.quit()
sys.exit()