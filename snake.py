import pygame
import time
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
FPS = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
GRAY = (169, 169, 169)

# Initialize screen and fonts
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
menu_font = pygame.font.SysFont("comicsansms", 45)

# Clock for controlling the frame rate
clock = pygame.time.Clock()


# Helper Functions
def display_score(score):
    value = score_font.render("Score: " + str(score), True, BLUE)
    screen.blit(value, [10, 10])


def draw_snake(block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], block_size, block_size])


def message(msg, color, position, font):
    mesg = font.render(msg, True, color)
    screen.blit(mesg, position)


def start_menu():
    while True:
        screen.fill(BLACK)
        message("Welcome to Snake Game", WHITE, [WIDTH // 6, HEIGHT // 5], menu_font)
        message("Press S to Start or Q to Quit", GRAY, [WIDTH // 6, HEIGHT // 3], font_style)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Start the game
                    return
                elif event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    sys.exit()


def check_food_position(snake_list):
    while True:
        food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        if [food_x, food_y] not in snake_list:
            return food_x, food_y


# Main Game Logic
def game_loop():
    game_over = False
    game_close = False

    # Initial snake position and direction
    x1, y1 = WIDTH // 2, HEIGHT // 2
    x1_change, y1_change = 0, 0

    # Snake body and length
    snake_list = []
    snake_length = 1

    # Initial food position
    food_x, food_y = check_food_position(snake_list)

    while not game_over:

        while game_close:
            screen.fill(WHITE)
            message("You lost! Press Q to Quit or C to Play Again", RED, [WIDTH // 6, HEIGHT // 3], font_style)
            display_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        return  # Restart the game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        # Check for boundary collision
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)

        # Draw food
        pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

        # Update snake
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check for self-collision
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(BLOCK_SIZE, snake_list)
        display_score(snake_length - 1)
        pygame.display.update()

        # Check if snake eats food
        if x1 == food_x and y1 == food_y:
            food_x, food_y = check_food_position(snake_list)
            snake_length += 1

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


# Main Function
def main():
    start_menu()
    while True:
        game_loop()


if __name__ == "__main__":
    main()