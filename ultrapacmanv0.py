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

# Ghosts
ghost_positions = [
    {"x": 7, "y": 8, "color": red},
    {"x": 8, "y": 8, "color": pink},
    {"x": 9, "y": 8, "color": cyan},
    {"x": 10, "y": 8, "color": orange},
]

# Game state
game_over = False

# Create screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pacman")

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
        (pacman_x * cell_size + cell_size // 2, pacman_y * cell_size + cell_size // 2),
        cell_size // 2,
    )

def draw_ghosts():
    for ghost in ghost_positions:
        pygame.draw.circle(
            screen,
            ghost["color"],
            (ghost["x"] * cell_size + cell_size // 2, ghost["y"] * cell_size + cell_size // 2),
            cell_size // 2,
        )

def move_pacman(dx, dy):
    global pacman_x, pacman_y

    new_x = pacman_x + dx
    new_y = pacman_y + dy

    if (
        0 <= new_x < len(maze[0])
        and 0 <= new_y < len(maze)
        and maze[new_y][new_x] == 0
    ):
        pacman_x = new_x
        pacman_y = new_y

def move_ghosts():
    for ghost in ghost_positions:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x = ghost["x"] + dx
            new_y = ghost["y"] + dy

            if (
                0 <= new_x < len(maze[0])
                and 0 <= new_y < len(maze)
                and maze[new_y][new_x] == 0
            ):
                ghost["x"] = new_x
                ghost["y"] = new_y
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
                move_pacman(-1, 0)
            if event.key == pygame.K_RIGHT:
                move_pacman(1, 0)
            if event.key == pygame.K_UP:
                move_pacman(0, -1)
            if event.key == pygame.K_DOWN:
                move_pacman(0, 1)

    # Move ghosts
    move_ghosts()

    # Check game over
    for ghost in ghost_positions:
        if pacman_x == ghost["x"] and pacman_y == ghost["y"]:
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

    # Update the display
    pygame.display.flip()

    # Delay to control game speed
    pygame.time.delay(game_speed)

    # Limit the frame rate
    clock.tick(frame_rate)

# Quit Pygame
pygame.quit()
