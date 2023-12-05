import pygame
import sys
import math
import random
from goalie import Goalie
from player import Player
# Constants
WIDTH, HEIGHT = 800, 400
PLAYER_SIZE = 20
GOAL_WIDTH = 100
GOALIE_RANGE = 50  # Vertical range for goalie movement

WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Initialize game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lacrosse Game")

# Initialize player
player = Player(WIDTH // 2, HEIGHT // 2, PLAYER_SIZE, 5)

# Initialize goalie
goalie = Goalie(WIDTH - GOAL_WIDTH - 20, HEIGHT // 2)

# Ball
ball_radius = 10
ball_speed = 8
ball_pos = (0, 0)
shooting = False

# Ball destination (where the mouse was clicked)
destination_x, destination_y = 0, 0

def shoot(self, ball_pos):
   

# Goal triangle vertices
goal_vertices = [(WIDTH - GOAL_WIDTH, HEIGHT // 2 - GOAL_WIDTH // 2),
                 (WIDTH - GOAL_WIDTH, HEIGHT // 2 + GOAL_WIDTH // 2),
                 (WIDTH, HEIGHT // 2)]

# Crease circle
crease_center = (WIDTH - GOAL_WIDTH // 2, HEIGHT // 2)
crease_radius = 80

#Font
font = pygame.font.Font(None, 28)

# Display instructions
def print_instructions(self):
    instructions = [
            "Welcome to Lacrosse Game!",
            "Instructions:",
            "- Move the player using arrow keys.",
            "- Shoot the ball with the mouse.",
            "- Score goals to earn points.",
            "",
            "Press the SPACE BAR to start the game."]
    instruction_texts = [font.render(line, True, WHITE) for line in instructions]
    instruction_height = sum([text.get_height() for text in instruction_texts])
     # Draw instructions
    for i, text in enumerate(instruction_texts):
        screen.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - instruction_height) // 2 + i * text.get_height()))

# Set up clock
clock = pygame.time.Clock()

# Game loop
game_running = False
while not game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_running = True

    # Clear the screen
    screen.fill(GREEN)

    # Draw instructions
    print_instructions()

    # Update the display
    pygame.display.flip()

# Reset the clock for the game loop
clock.tick()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not shooting:
            shooting = True
            ball_pos = (player.x + PLAYER_SIZE // 2, player.y + PLAYER_SIZE // 2)
            shoot(ball_pos)

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player.speed
    if keys[pygame.K_RIGHT] and player.x < WIDTH - PLAYER_SIZE:
        player.x += player.speed
    if keys[pygame.K_UP] and player.y > 0:
        player.y -= player.speed
    if keys[pygame.K_DOWN] and player.y < HEIGHT - PLAYER_SIZE:
        player.y += player.speed

    elif event.type == pygame.MOUSEBUTTONDOWN and not shooting:
            # Set the destination to the mouse click position
            destination_x, destination_y = pygame.mouse.get_pos()
            shooting = True

    if shooting:
        # Calculate the angle between the ball and the destination
        angle = math.atan2(destination_y - ball_pos[1], destination_x - ball_pos[0])

        # Set the shooting speed
        shooting_speed = 5

        # Update the ball's position towards the destination
        ball_pos[0] += shooting_speed * math.cos(angle)
        ball_pos[1] += shooting_speed * math.sin(angle)

        # Check if the ball has reached the destination
        if math.dist((ball_pos[0], ball_pos[1]), (destination_x, destination_y)) < shooting_speed:
            shooting = False
        # Check for goalie making contact with the ball
        if pygame.Rect(goalie.x, goalie.y, PLAYER_SIZE, PLAYER_SIZE).colliderect(
            pygame.Rect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, ball_radius * 2, ball_radius * 2)):
            print("Goalie made contact with the ball!")
            shooting = False
            goalie.score += 1
            # Reset ball position
            ball_pos = (0, 0)

    # Update goalie
    goalie.update(ball_pos)

    # Clear the screen
    screen.fill(GREEN)

    # Draw the lacrosse field lines
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH - GOAL_WIDTH, HEIGHT), 2)
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)

    # Draw the goal triangle
    pygame.draw.polygon(screen, RED, goal_vertices)

    # Draw the crease circle
    pygame.draw.circle(screen, WHITE, (int(crease_center[0]), int(crease_center[1])), crease_radius, 2)

    # Draw the goal
    pygame.draw.rect(screen, WHITE, (WIDTH - GOAL_WIDTH, HEIGHT // 2 - GOAL_WIDTH // 2, GOAL_WIDTH, GOAL_WIDTH), 2)

    # Draw the player
    player.draw(screen)

    # Draw the ball
    goalie.draw(screen)

    # Display scores
    player_text = font.render(f"Player: {player.score}", True, WHITE)
    goalie_text = font.render(f"Goalie: {goalie.score}", True, WHITE)
    screen.blit(player_text, (10, 10))
    screen.blit(goalie_text, (10, 40))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)