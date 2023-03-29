import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the width and height of the screen [width, height]
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Set the tile size
TILE_SIZE = 20

# Set the number of tiles in each direction
MAP_WIDTH = SCREEN_WIDTH // TILE_SIZE
MAP_HEIGHT = SCREEN_HEIGHT // TILE_SIZE

# Define the player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load the player image
        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.image.fill(WHITE)

        # Set the player's position
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, MAP_WIDTH - 1) * TILE_SIZE
        self.rect.y = random.randint(0, MAP_HEIGHT - 1) * TILE_SIZE

    def update(self):
        # Move the player based on user input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= TILE_SIZE/20
        elif keys[pygame.K_RIGHT]:
            self.rect.x += TILE_SIZE/20
        elif keys[pygame.K_UP]:
            self.rect.y -= TILE_SIZE/20
        elif keys[pygame.K_DOWN]:
            self.rect.y += TILE_SIZE/20

# Initialize Pygame
pygame.init()

# Set the screen size
screen = pygame.display.set_mode(SCREEN_SIZE)

# Set the window title
pygame.display.set_caption("Roguelike")

# Create a group of sprites for all objects in the game
all_sprites_group = pygame.sprite.Group()

# Create the player object and add it to the sprite group
player = Player()
all_sprites_group.add(player)

# Run the game loop
done = False

while not done:
    # Handle events in the game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Update all sprites in the game loop
    all_sprites_group.update()

    # Draw all sprites in the game loop
    screen.fill(BLACK)
    all_sprites_group.draw(screen)

    # Update the display in the game loop
    pygame.display.flip()

# Quit Pygame when done with the game loop
pygame.quit()