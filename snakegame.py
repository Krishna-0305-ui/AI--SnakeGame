import pygame
import sys
import random

# Initialize
pygame.init()

# Constants
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Snake AI")
clock = pygame.time.Clock()

# Snake and Food
snake = [(5, 5)]
direction = (1, 0)
food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))

def draw():
    screen.fill(BLACK)
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (food[0]*CELL_SIZE, food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

def is_collision(pos):
    return (
        pos in snake or
        pos[0] < 0 or pos[0] >= GRID_WIDTH or
        pos[1] < 0 or pos[1] >= GRID_HEIGHT
    )

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_next_move():
    head = snake[0]
    options = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    valid_moves = []

    for dx, dy in options:
        new_pos = (head[0] + dx, head[1] + dy)
        if not is_collision(new_pos):
            dist = manhattan_distance(new_pos, food)
            valid_moves.append((dist, (dx, dy)))

    if valid_moves:
        valid_moves.sort()
        return valid_moves[0][1]
    else:
        return (0, 0)  # No move possible

def update_snake():
    global food
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    if is_collision(new_head):
        pygame.quit()
        sys.exit()

    snake.insert(0, new_head)

    if new_head == food:
        food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        while food in snake:
            food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
    else:
        snake.pop()

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    direction = get_next_move()
    update_snake()
    draw()
    clock.tick(FPS)
