import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game constants
BIRD_WIDTH, BIRD_HEIGHT = 50, 35
PIPE_WIDTH = 70
PIPE_HEIGHT = 400
PIPE_GAP = 200
PIPE_VELOCITY = 5
GRAVITY = 1
JUMP_STRENGTH = 12
GROUND_HEIGHT = 100

# Load assets
BIRD_IMAGE = pygame.transform.scale(pygame.image.load("resized_bird.png"), (BIRD_WIDTH, BIRD_HEIGHT))
PIPE_IMAGE = pygame.transform.scale(pygame.image.load("resized_pipe.png"), (PIPE_WIDTH, PIPE_HEIGHT))
GROUND_RECT = pygame.Rect(0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)

# Font for displaying the score
FONT = pygame.font.SysFont("Arial", 30)

# Bird class
class Bird:
    def __init__(self):
        self.x = WIDTH // 4
        self.y = HEIGHT // 2
        self.velocity = 0
        self.rect = pygame.Rect(self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT)

    def jump(self):
        self.velocity = -JUMP_STRENGTH

    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y

    def draw(self):
        SCREEN.blit(BIRD_IMAGE, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(150, HEIGHT - PIPE_GAP - GROUND_HEIGHT)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP)

    def move(self):
        self.x -= PIPE_VELOCITY
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        SCREEN.blit(PIPE_IMAGE, (self.x, self.height - PIPE_HEIGHT))  # Top pipe
        SCREEN.blit(PIPE_IMAGE, (self.x, self.height + PIPE_GAP))     # Bottom pipe

    def is_off_screen(self):
        return self.x + PIPE_WIDTH < 0

# Function to display score
def display_score(score):
    score_text = FONT.render(f"Score: {score}", True, BLACK)
    SCREEN.blit(score_text, (10, 10))

# Function to check for collision between bird and pipes
def check_collision(bird, pipes):
    for pipe in pipes:
        if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
            return True
    if bird.rect.colliderect(GROUND_RECT) or bird.y < 0:
        return True
    return False

# Function to reset the game
def reset_game():
    global bird, pipes, score, game_over
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    game_over = False

# Main game loop
def main():
    global bird, pipes, score, game_over
    clock = pygame.time.Clock()

    # Initialize game objects
    reset_game()

    while True:
        clock.tick(30)  # Limit the frame rate to 30 FPS

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.jump()
                elif event.key == pygame.K_r and game_over:  # Restart the game if 'R' is pressed
                    reset_game()

        if not game_over:
            # Bird movement
            bird.move()

            # Pipe movement and generation
            for pipe in pipes:
                pipe.move()

            # Add new pipes when needed
            if pipes[-1].x < WIDTH // 2:
                pipes.append(Pipe())

            # Remove pipes that are off-screen
            pipes = [pipe for pipe in pipes if not pipe.is_off_screen()]

            # Check for collisions
            if check_collision(bird, pipes):
                game_over = True

            # Scoring
            for pipe in pipes:
                if pipe.x + PIPE_WIDTH < bird.x and not pipe.is_off_screen():
                    score += 1

        # Drawing everything
        SCREEN.fill(WHITE)
        bird.draw()
        for pipe in pipes:
            pipe.draw()
        pygame.draw.rect(SCREEN, GREEN, GROUND_RECT)  # Ground
        display_score(score)

        if game_over:
            game_over_text = FONT.render("Game Over", True, RED)
            SCREEN.blit(game_over_text, (WIDTH // 4, HEIGHT // 2))
            restart_text = FONT.render("Press 'R' to Restart", True, RED)
            SCREEN.blit(restart_text, (WIDTH // 3, HEIGHT // 2 + 40))

        pygame.display.update()

if __name__ == "__main__":
    main()
