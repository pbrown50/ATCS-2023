import pygame
import sys
import math
import random
from goalie import Goalie
from player import Player

class Game:
    # Constants
    WIDTH, HEIGHT = 800, 400
    PLAYER_SIZE = 20
    GOAL_WIDTH = 100
    GOALIE_RANGE = 50  # Vertical range for goalie movement

    WHITE = (255, 255, 255)
    GREEN = (0, 128, 0)
    RED = (255, 0, 0)

    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Initialize game window
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Lacrosse Game")

        # Initialize player
        player = Player(self.WIDTH // 2, self.HEIGHT // 2, self.PLAYER_SIZE, 5)

        # Initialize goalie
        goalie = Goalie(self, self.WIDTH - self.GOAL_WIDTH - 20, self.HEIGHT // 2)

        # Ball
        ball_radius = 10
        ball_speed = 8
        ball_pos = (0, 0)
        shooting = False

        # Ball destination (where the mouse was clicked)
        destination_x, destination_y = 0, 0

        # def shoot(self, ball_pos):

        # Goal triangle vertices
        goal_vertices = [(self.WIDTH - self.GOAL_WIDTH, self.HEIGHT // 2 - self.GOAL_WIDTH // 2),
                        (self.WIDTH - self.GOAL_WIDTH, self.HEIGHT // 2 + self.GOAL_WIDTH // 2),
                        (self.WIDTH, self.HEIGHT // 2)]

        # Crease circle
        crease_center = (self.WIDTH - self.GOAL_WIDTH // 2, self.HEIGHT // 2)
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
            instruction_texts = [font.render(line, True, self.WHITE) for line in instructions]
            instruction_height = sum([text.get_height() for text in instruction_texts])
            # Draw instructions
            for i, text in enumerate(instruction_texts):
                screen.blit(text, ((self.WIDTH - text.get_width()) // 2, (self.HEIGHT - instruction_height) // 2 + i * text.get_height()))

        # Set up clock
        clock = pygame.time.Clock()
        def run_game(self):
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
                screen.fill(self.GREEN)

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
                        ball_pos = (player.x + self.PLAYER_SIZE // 2, player.y + self.PLAYER_SIZE // 2)
                        self.shoot(ball_pos)

                # Handle player movement
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and player.x > 0:
                    player.x -= player.speed
                if keys[pygame.K_RIGHT] and player.x < self.WIDTH - self.PLAYER_SIZE:
                    player.x += player.speed
                if keys[pygame.K_UP] and player.y > 0:
                    player.y -= player.speed
                if keys[pygame.K_DOWN] and player.y < self.HEIGHT - self.PLAYER_SIZE:
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
                    if pygame.Rect(goalie.x, goalie.y, self.PLAYER_SIZE, self.PLAYER_SIZE).colliderect(
                        pygame.Rect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, ball_radius * 2, ball_radius * 2)):
                        print("Goalie made contact with the ball!")
                        shooting = False
                        goalie.score += 1
                        # Reset ball position
                        ball_pos = (0, 0)

                # Update goalie
                goalie.update(ball_pos)

                # Clear the screen
                screen.fill(self.GREEN)

                # Draw the lacrosse field lines
                pygame.draw.rect(screen, self.WHITE, (0, 0, self.WIDTH - self.GOAL_WIDTH, self.HEIGHT), 2)
                pygame.draw.line(screen, self.WHITE, (self.WIDTH // 2, 0), (self.WIDTH // 2, self.HEIGHT), 2)

                # Draw the goal triangle
                pygame.draw.polygon(screen, self.RED, goal_vertices)

                # Draw the crease circle
                pygame.draw.circle(screen, self.WHITE, (int(crease_center[0]), int(crease_center[1])), crease_radius, 2)

                # Draw the goal
                pygame.draw.rect(screen, self.WHITE, (self.WIDTH - self.GOAL_WIDTH, self.HEIGHT // 2 - self.GOAL_WIDTH // 2, self.GOAL_WIDTH, self.GOAL_WIDTH), 2)

                # Draw the player
                player.draw(screen)

                # Draw the ball
                goalie.draw(screen)

                # Display scores
                player_text = font.render(f"Player: {player.score}", True, self.WHITE)
                goalie_text = font.render(f"Goalie: {goalie.score}", True, self.WHITE)
                screen.blit(player_text, (10, 10))
                screen.blit(goalie_text, (10, 40))

                # Update the display
                pygame.display.flip()

                # Cap the frame rate
                clock.tick(60)

    