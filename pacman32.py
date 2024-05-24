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
title_font = pygame.font.Font(None, 48)

# Maze layout (1 represents wall, 0 represents pellet, 2 represents empty space)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 1, 0, 1],
    [1, 0, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 0, 1],
    [1, 0, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1, 0, 1],
    [1, 0, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 0, 0, 1],
    [1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 2, 2, 1, 0, 2, 2, 2, 2, 2, 2, 2, 0, 1, 2, 2, 0, 1],
    [1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1],
    [1, 0, 0, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 0, 0, 1],
    [1, 0, 1, 1, 1, 2, 1, 1, 0, 1, 0, 1, 1, 2, 1, 1, 1, 0, 1],
    [1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Pacman
pacman_x = 9
pacman_y = 15

# Ghosts
ghost_positions = [
    {"x": 7, "y": 8, "color": red, "direction": (0, 1)},
    {"x": 8, "y": 8, "color": pink, "direction": (0, 1)},
    {"x": 9, "y": 8, "color": cyan, "direction": (0, 1)},
    {"x": 10, "y": 8, "color": orange, "direction": (0, 1)},
]

# Game state
game_over = False
score = 0

# Create screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pacman")

# Frame rate
frame_rate = 60

# Game speed (delay between frames in milliseconds)
game_speed = 100

# Waka waka sound effect speed (in milliseconds)
waka_waka_speed = 500


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
            elif maze[y][x] == 0:
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
    global pacman_x, pacman_y, score

    new_x = pacman_x + dx
    new_y = pacman_y + dy

    if (
        0 <= new_x < len(maze[0])
        and 0 <= new_y < len(maze)
        and maze[new_y][new_x] != 1
    ):
        pacman_x = new_x
        pacman_y = new_y

        if maze[new_y][new_x] == 0:
            score += 10
            maze[new_y][new_x] = 2  # Mark as empty space


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
                and maze[new_y][new_x] != 1
            ):
                ghost["x"] = new_x
                ghost["y"] = new_y
                break


def check_collision():
    global game_over

    for ghost in ghost_positions:
        if ghost["x"] == pacman_x and ghost["y"] == pacman_y:
            game_over = True
            break


def display_score():
    score_text = font.render("Score: " + str(score), True, white)
    screen.blit(score_text, (10, screen_height - 40))


def game_over_screen():
    game_over_text = font.render("Game Over", True, white)
    screen.blit(game_over_text, (screen_width // 2 - 70, screen_height // 2 - 20))


# Define a function to generate beep sounds with varying frequencies and durations
def generate_beep_sound(frequency, duration):
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * ((i // (sample_rate // frequency)) % 2)) for i in range(samples)]
    sound = pygame.mixer.Sound(buffer=array('h', wave))
    sound.set_volume(0.1)
    return sound


# Create the "wa k a wa ak awaka" sound effect
def create_wa_k_a_wa_ak_awaka_sound():
    sounds = [
        generate_beep_sound(440, 0.1),   # "wa"
        generate_beep_sound(523.25, 0.1),   # "k"
        generate_beep_sound(587.33, 0.1),   # "a"
        generate_beep_sound(440, 0.1),   # "wa"
        generate_beep_sound(587.33, 0.1),   # "ak"
        generate_beep_sound(659.25, 0.1),   # "awa"
        generate_beep_sound(523.25, 0.1),   # "ka"
    ]

    for sound in sounds:
        sound.play()
        pygame.time.wait(waka_waka_speed)


def show_main_menu():
    main_menu = True

    while main_menu:
        screen.fill(black)

        title_text = title_font.render("ULTRA PACMAN V0.1", True, white)
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(title_text, title_rect)

        copyright_text = font.render("[C] Flames Labs 20XX-2025", True, white)
        copyright_rect = copyright_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(copyright_text, copyright_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_menu = False


def show_countdown():
    for i in range(3, 0, -1):
        screen.fill(black)
        countdown_text = title_font.render(str(i), True, white)
        countdown_rect = countdown_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(countdown_text, countdown_rect)
        pygame.display.flip()
        pygame.time.wait(1000)

    screen.fill(black)
    go_text = title_font.render("GO!", True, white)
    go_rect = go_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(go_text, go_rect)
    pygame.display.flip()
    pygame.time.wait(1000)


show_main_menu()
show_countdown()

clock = pygame.time.Clock()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_pacman(-1, 0)
            elif event.key == pygame.K_RIGHT:
                move_pacman(1, 0)
            elif event.key == pygame.K_UP:
                move_pacman(0, -1)
            elif event.key == pygame.K_DOWN:
                move_pacman(0, 1)

    screen.fill(black)

    draw_maze()
    draw_pacman()
    draw_ghosts()
    display_score()

    move_ghosts()
    check_collision()

    if game_over:
        game_over_screen()

    pygame.display.update()
    clock.tick(frame_rate)
    pygame.time.delay(game_speed)

    # Play the "wa k a wa ak awaka" sound effect
    create_wa_k_a_wa_ak_awaka_sound()

pygame.quit()   
