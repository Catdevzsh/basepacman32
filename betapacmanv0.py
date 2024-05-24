import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
pink = (255, 105, 180)
cyan = (0, 255, 255)
orange = (255, 165, 0)

# Screen dimensions
screen_width = 608
screen_height = 672

# Cell dimensions
cell_size = 32

# Font
font = pygame.font.Font(None, 36)

# Maze layout (1 represents wall, 0 represents empty space)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Pacman
pacman_x = 9
pacman_y = 15
pacman_speed = 2 
pacman_direction = "LEFT"
pacman_rect = pygame.Rect(pacman_x * cell_size, pacman_y * cell_size, cell_size, cell_size)

# Ghosts
ghost_speed = 1.5
ghost_positions = [
    {"x": 7, "y": 8, "color": red, "direction": "UP", "rect": pygame.Rect(7 * cell_size, 8 * cell_size, cell_size, cell_size)},
    {"x": 8, "y": 8, "color": pink, "direction": "DOWN", "rect": pygame.Rect(8 * cell_size, 8 * cell_size, cell_size, cell_size)},
    {"x": 9, "y": 8, "color": cyan, "direction": "LEFT", "rect": pygame.Rect(9 * cell_size, 8 * cell_size, cell_size, cell_size)},
    {"x": 10, "y": 8, "color": orange, "direction": "RIGHT", "rect": pygame.Rect(10 * cell_size, 8 * cell_size, cell_size, cell_size)},
]

# Game state
game_over = False
game_started = False

# Create screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("UltraPacman M1 Edition")

# Frame rate
frame_rate = 60

# Game speed (delay between frames in milliseconds)
game_speed = 100

def draw_maze():
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 1:
                pygame.draw.rect(
                    screen,
                    blue,
                    (x * cell_size, y * cell_size, cell_size, cell_size),
                    2,
                )
            else:
                pygame.draw.circle(
                    screen,
                    white,
                    (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2),
                    2,
                )

def draw_pacman():
    pygame.draw.circle(
        screen,
        yellow,
        (pacman_rect.centerx, pacman_rect.centery),
        cell_size // 2,
    )

def draw_ghosts():
    for ghost in ghost_positions:
        pygame.draw.circle(
            screen,
            ghost["color"],
            (ghost["rect"].centerx, ghost["rect"].centery),
            cell_size // 2,
        )

def move_pacman(direction):
    global pacman_x, pacman_y, pacman_rect

    new_x = pacman_x
    new_y = pacman_y

    if direction == "LEFT":
        new_x -= 1
    elif direction == "RIGHT":
        new_x += 1
    elif direction == "UP":
        new_y -= 1
    elif direction == "DOWN":
        new_y += 1

    if (
        0 <= new_x < len(maze[0])
        and 0 <= new_y < len(maze)
        and maze[new_y][new_x] == 0
    ):
        pacman_x = new_x
        pacman_y = new_y
        pacman_rect.x = pacman_x * cell_size
        pacman_rect.y = pacman_y * cell_size

def move_ghosts():
    for ghost in ghost_positions:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x = int(ghost["x"] + dx)
            new_y = int(ghost["y"] + dy)

            if (
                0 <= new_x < len(maze[0])
                and 0 <= new_y < len(maze)
                and maze[new_y][new_x] == 0
            ):
                ghost["x"] = new_x
                ghost["y"] = new_y
                ghost["rect"].x = ghost["x"] * cell_size
                ghost["rect"].y = ghost["y"] * cell_size
                break  # Move only one step

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman_direction = "LEFT"
            if event.key == pygame.K_RIGHT:
                pacman_direction = "RIGHT"
            if event.key == pygame.K_UP:
                pacman_direction = "UP"
            if event.key == pygame.K_DOWN:
                pacman_direction = "DOWN"
            if event.key == pygame.K_SPACE and not game_started:
                game_started = True

    # Move Pacman if game has started
    if game_started:
        move_pacman(pacman_direction)
        move_ghosts()

    # Check game over
    for ghost in ghost_positions:
        if pacman_rect.colliderect(ghost["rect"]):
            game_over = True

    # Draw everything
    screen.fill(black)
    draw_maze()
    draw_pacman()
    draw_ghosts()

    if game_over:
        text = font.render("GAME OVER", True, red)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)
    elif not game_started:
        start_text = font.render("Press SPACE to start", True, white)
        start_text_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(start_text, start_text_rect)

    # Update the display
    pygame.display.flip()

    # Delay to control game speed
    pygame.time.delay(game_speed)

    # Limit the frame rate
    clock.tick(frame_rate)

# Quit Pygame
pygame.quit()
