import pygame
import random
import time
from array import array

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
pink = (255, 184, 255)
cyan = (0, 255, 255)
orange = (255, 184, 82)

# Screen dimensions
screen_width = 224
screen_height = 288

# Cell dimensions
cell_size = 8

# Font
font = pygame.font.Font(None, 16)
title_font = pygame.font.Font(None, 24)

# Maze layout (1 represents wall, 0 represents pellet, 2 represents empty space, 3 represents power pellet)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 2, 2, 2, 2, 2, 2, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 2, 2, 2, 2, 2, 2, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 3, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 3, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pac-Man")

# Load sound effects
# Remember to replace these with your actual sound files
intro_sound = pygame.mixer.Sound("intro.wav")
chomp_sound = pygame.mixer.Sound("chomp.wav")
death_sound = pygame.mixer.Sound("death.wav")
intermission_sound = pygame.mixer.Sound("intermission.wav")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((cell_size, cell_size))
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.x = 1
        self.y = 1
        self.speed = 1
        self.direction = "right"
        self.score = 0
        self.lives = 3
        self.power_up = False
        self.power_up_time = 0

    def update(self):
        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed
        self.rect.x = self.x * cell_size
        self.rect.y = self.y * cell_size

        # Check for collision with walls
        if maze[self.y][self.x] == 1:
            if self.direction == "right":
                self.x -= self.speed
            elif self.direction == "left":
                self.x += self.speed
            elif self.direction == "up":
                self.y += self.speed
            elif self.direction == "down":
                self.y -= self.speed

        # Check for collision with pellets
        if maze[self.y][self.x] == 0:
            maze[self.y][self.x] = 2
            self.score += 10
            chomp_sound.play()

        # Check for collision with power pellets
        if maze[self.y][self.x] == 3:
            maze[self.y][self.x] = 2
            self.score += 50
            self.power_up = True
            self.power_up_time = time.time()
            chomp_sound.play()

        # Disable power-up after 5 seconds
        if self.power_up and time.time() - self.power_up_time > 5:
            self.power_up = False

    def draw(self):
        screen.blit(self.image, self.rect)

# Ghost class
class Ghost(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface((cell_size, cell_size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.speed = 1
        self.direction = random.choice(["right", "left", "up", "down"])
        self.frightened = False
        self.frightened_time = 0

    def update(self):
        if self.frightened:
            if time.time() - self.frightened_time > 5:
                self.frightened = False
                self.speed = 1
                self.image.fill(self.original_color)
        
        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed
        self.rect.x = self.x * cell_size
        self.rect.y = self.y * cell_size

        # Check for collision with walls
        if maze[self.y][self.x] == 1:
            if self.direction == "right":
                self.x -= self.speed
                self.direction = random.choice(["left", "up", "down"])
            elif self.direction == "left":
                self.x += self.speed
                self.direction = random.choice(["right", "up", "down"])
            elif self.direction == "up":
                self.y += self.speed
                self.direction = random.choice(["right", "left", "down"])
            elif self.direction == "down":
                self.y -= self.speed
                self.direction = random.choice(["right", "left", "up"])

    def draw(self):
        screen.blit(self.image, self.rect)

    def frighten(self):
        self.frightened = True
        self.frightened_time = time.time()
        self.speed = 0.5
        self.image.fill(blue)
        self.original_color = self.image.get_at((0, 0))  # Store original color

# Create player and ghosts
player = Player()
ghosts = pygame.sprite.Group()
ghosts.add(Ghost(red, 13, 11))
ghosts.add(Ghost(pink, 14, 11))
ghosts.add(Ghost(cyan, 15, 11))
ghosts.add(Ghost(orange, 16, 11))

# Game loop
running = True
game_over = False
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.direction = "right"
            elif event.key == pygame.K_LEFT:
                player.direction = "left"
            elif event.key == pygame.K_UP:
                player.direction = "up"
            elif event.key == pygame.K_DOWN:
                player.direction = "down"

    # Update game objects
    if not game_over:
        player.update()
        ghosts.update()

        # Check for collision between player and ghosts
        if any(pygame.sprite.collide_rect(player, ghost) for ghost in ghosts):
            if player.power_up:
                for ghost in ghosts:
                    if pygame.sprite.collide_rect(player, ghost):
                        ghost.kill()  # Remove ghost if eaten
                        player.score += 200
            else:
                death_sound.play()
                player.lives -= 1
                player.x = 1
                player.y = 1
                if player.lives == 0:
                    game_over = True

        # Frighten ghosts if power-up is active
        if player.power_up:
            for ghost in ghosts:
                ghost.frighten()

    # Draw game objects
    screen.fill(black)
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, blue, (x * cell_size, y * cell_size, cell_size, cell_size))
            elif cell == 0:
                pygame.draw.circle(screen, white, (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), 2)
            elif cell == 3:
                pygame.draw.circle(screen, white, (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), 4)
    player.draw()
    ghosts.draw(screen)

    # Display score and lives
    score_text = font.render("Score: " + str(player.score), True, white)
    screen.blit(score_text, (10, 10))
    lives_text = font.render("Lives: " + str(player.lives), True, white)
    screen.blit(lives_text, (screen_width - lives_text.get_width() - 10, 10))

    # Display game over message
    if game_over:
        game_over_text = title_font.render("Game Over", True, red)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))

    # Update the display
    pygame.display.flip()

    # Limit frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
