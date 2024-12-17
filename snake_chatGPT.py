import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Snake block size
BLOCK_SIZE = 10

# Font
FONT = pygame.font.SysFont("bahnschrift", 25)

# FPS controller
CLOCK = pygame.time.Clock()

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.segments = [[WIDTH // 2, HEIGHT // 2]]
        self.direction = (0, 0)
        self.grow = False

    def move(self):
        if self.direction != (0, 0):
            head_x, head_y = self.segments[0]
            delta_x, delta_y = self.direction
            new_head = [head_x + delta_x, head_y + delta_y]
            self.segments.insert(0, new_head)
            if not self.grow:
                self.segments.pop()
            self.grow = False

    def draw(self):
        for segment in self.segments:
            pygame.draw.rect(screen, BLACK, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])

    def check_collision(self):
        head = self.segments[0]
        # Check boundaries
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True
        # Check self-collision
        if head in self.segments[1:]:
            return True
        return False

    def grow_snake(self):
        self.grow = True

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 10.0) * 10.0
        self.y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 10.0) * 10.0

    def draw(self):
        pygame.draw.rect(screen, GREEN, [self.x, self.y, BLOCK_SIZE, BLOCK_SIZE])

    def relocate(self):
        self.x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 10.0) * 10.0
        self.y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 10.0) * 10.0

def message(msg, color, x, y):
    text = FONT.render(msg, True, color)
    screen.blit(text, [x, y])

def gameLoop():
    game_over = False
    game_close = False

    # Initialize snake and food
    snake = Snake()
    food = Food()

    while not game_over:

        while game_close:
            screen.fill(BLUE)
            message("You lost! Press Q-Quit or C-Play Again", RED, WIDTH / 6, HEIGHT / 3)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake.direction != (BLOCK_SIZE, 0):
                    snake.direction = (-BLOCK_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-BLOCK_SIZE, 0):
                    snake.direction = (BLOCK_SIZE, 0)
                elif event.key == pygame.K_UP and snake.direction != (0, BLOCK_SIZE):
                    snake.direction = (0, -BLOCK_SIZE)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -BLOCK_SIZE):
                    snake.direction = (0, BLOCK_SIZE)

        snake.move()

        if snake.check_collision():
            game_close = True

        screen.fill(WHITE)
        food.draw()
        snake.draw()

        if snake.segments[0][0] == food.x and snake.segments[0][1] == food.y:
            food.relocate()
            snake.grow_snake()

        pygame.display.update()
        CLOCK.tick(15)

    pygame.quit()
    quit()

# Start the game
gameLoop()
