import pygame
import random
pygame.init()
pygame.font.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW_CAPTION = "Sprite Collision Game"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
PLAYER_SPRITE_FILENAME = "Spaceship.avif"
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
        self.image = load_image_with_fallback(PLAYER_SPRITE_FILENAME, PLAYER_SIZE, RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 20 # Start near the bottom center
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

        # Keep player on screen
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
        self.image = load_image_with_fallback(ENEMY_SPRITE_FILENAME, ENEMY_SIZE, BLUE)
        self.rect = self.image.get_rect()
        # Random initial position, avoiding edges too closely
        self.rect.x = random.randrange(ENEMY_SIZE[0], WINDOW_WIDTH - ENEMY_SIZE[0])
        self.rect.y = random.randrange(ENEMY_SIZE[1], WINDOW_HEIGHT - ENEMY_SIZE[1] - 50) # Keep them off the very bottom initially

# --- Create the game screen ---
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(WINDOW_CAPTION)

# --- Score Font ---
try:
    score_font = pygame.font.Font(None, SCORE_FONT_SIZE) # Default system font
except Exception as e:
    print(f"Could not load default font: {e}. Using basic font.")
    score_font = pygame.font.SysFont("arial", SCORE_FONT_SIZE)


# --- Sprite Groups ---
all_sprites = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for _ in range(NUM_ENEMIES):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies_group.add(enemy)

# --- Game Loop ---
running = True
clock = pygame.time.Clock()

while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # --- Update Sprites ---
    all_sprites.update() # Calls the update() method of each sprite in the group (only Player has one here)

    # --- Collision Detection ---
    # pygame.sprite.spritecollide(sprite, group, dokill)
    # sprite: The sprite to check for collisions (our player).
    # group: The group of sprites to check against (our enemies_group).
    # dokill: If True, the colliding sprites in 'group' will be removed from all groups they belong to.
    collided_enemies = pygame.sprite.spritecollide(player, enemies_group, True) # True to remove collided enemies

    for enemy in collided_enemies:
        score += 1
        print(f"Collision! Score: {score}")
        # Optionally, you could spawn a new enemy here or have some other effect

    # --- Drawing ---
    screen.fill(GREEN) # Background

    all_sprites.draw(screen) # Draw all sprites

    # Draw Score
    score_text_surface = score_font.render(f"Score: {score}", True, SCORE_COLOR)
    score_rect = score_text_surface.get_rect()
    score_rect.topleft = (10, 10) # Position score at top-left
    screen.blit(score_text_surface, score_rect)

    # --- Update the display ---
    pygame.display.flip()

    # --- Cap the frame rate ---
    clock.tick(60) # Aim for 60 frames per second

# --- Quit Pygame ---
pygame.quit()