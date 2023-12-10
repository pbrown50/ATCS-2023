
import pygame
import sys
import math
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
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Lacrosse Game")

        # Initialize player
        self.player = Player(self.WIDTH // 2, self.HEIGHT // 2, self.PLAYER_SIZE, 5)

        # Initialize goalie
        self.goalie = Goalie(self, self.WIDTH - self.GOAL_WIDTH - 20, self.HEIGHT // 2)

        # Initialize ball
        self.ball_pos = [0, 0]
        self.ball_radius = 10

        # Goal triangle vertices
        self.goal_vertices = [(self.WIDTH - self.GOAL_WIDTH, self.HEIGHT // 2 - self.GOAL_WIDTH // 2),
                              (self.WIDTH - self.GOAL_WIDTH, self.HEIGHT // 2 + self.GOAL_WIDTH // 2),
                              (self.WIDTH, self.HEIGHT // 2)]

        # Crease circle
        self.crease_center = (self.WIDTH - self.GOAL_WIDTH // 2, self.HEIGHT // 2)
        self.crease_radius = 80

        # Font
        self.font = pygame.font.Font(None, 28)

        # Set up clock
        self.clock = pygame.time.Clock()

        # Initialize shooting attribute
        self.shooting = False

    def draw_ball(self):
        pygame.draw.circle(self.screen, self.WHITE, (int(self.ball_pos[0]), int(self.ball_pos[1])), self.ball_radius)

    # Display instructions
    def print_instructions(self):
        instructions = [
            "Welcome to Lacrosse Game!",
            "",
            "Instructions:",
            "- Move the player using arrow keys.",
            "",
            "- Shoot the ball with the mouse.",
            "- Score goals to earn points.",
            "",
            "Press the SPACE BAR to start the game."]
        instruction_texts = [self.font.render(line, True, self.WHITE) for line in instructions]
        instruction_height = sum([text.get_height() for text in instruction_texts])
        # Draw instructions
        for i, text in enumerate(instruction_texts):
            self.screen.blit(text, ((self.WIDTH - text.get_width()) // 2,
                                    (self.HEIGHT - instruction_height) // 2 + i * text.get_height()))

    def shoot(self, destination_x, destination_y):
        # Calculate the angle between the ball and the destination
        angle = math.atan2(destination_y - self.ball_pos[1], destination_x - self.ball_pos[0])

        # Set the shooting speed
        shooting_speed = 5

        # Update the ball's position towards the destination
        self.ball_pos = (self.ball_pos[0] + shooting_speed * math.cos(angle),
                         self.ball_pos[1] + shooting_speed * math.sin(angle))

        # Check if the ball has reached the destination
        if math.dist((self.ball_pos[0], self.ball_pos[1]), (destination_x, destination_y)) < shooting_speed:
            self.shooting = False

            # # Check for goal and goalie contact
            # if (pygame.Rect(self.goalie.x, self.goalie.y, self.PLAYER_SIZE, self.PLAYER_SIZE).colliderect(
            #         pygame.Rect(self.ball_pos[0], self.ball_pos[1],
            #             self.ball_radius * 2, self.ball_radius * 2))):
            #     print("Goalie made contact with the ball!")
            #     self.goalie.score += 1
            # elif self.ball_pos[0] > (self.HEIGHT - self.GOAL_WIDTH) / 2 and self.ball_pos[0] <  ((self.HEIGHT - self.GOAL_WIDTH) / 2) + self.GOAL_WIDTH and self.ball_pos[1] > self.WIDTH - self.GOAL_WIDTH:
            #     print("Goal scored!")
            #     self.player.score += 1

            # Reset ball position
            self.ball_pos = [0, 0]

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
            self.screen.fill(self.GREEN)

            # Draw instructions
            self.print_instructions()

            # Update the display
            pygame.display.flip()

        # Reset the clock for the game loop
        self.clock.tick()

        # Main game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.shooting:
                    self.shooting = True
                    self.ball_pos = (self.player.x + self.PLAYER_SIZE // 2, self.player.y + self.PLAYER_SIZE // 2)
                    self.destination_x, self.destination_y = pygame.mouse.get_pos()

            # Handle player movement
            keys = pygame.key.get_pressed()
            new_x, new_y = self.player.x, self.player.y

            if keys[pygame.K_LEFT] and self.player.x > 0:
                new_x -= self.player.speed
            if keys[pygame.K_RIGHT] and self.player.x < self.WIDTH - self.PLAYER_SIZE:
                new_x += self.player.speed
            if keys[pygame.K_UP] and self.player.y > 0:
                new_y -= self.player.speed
            if keys[pygame.K_DOWN] and self.player.y < self.HEIGHT - self.PLAYER_SIZE:
                new_y += self.player.speed

            # Check if the new position is inside the crease
            if not self.is_inside_crease(new_x + self.PLAYER_SIZE // 2, new_y + self.PLAYER_SIZE // 2):
                self.player.x = new_x
                self.player.y = new_y

            # Update goalie
            self.goalie.update(self.ball_pos)

            # Check for goalie contact
            if pygame.Rect(self.goalie.x, self.goalie.y, self.PLAYER_SIZE, self.PLAYER_SIZE).colliderect(
                pygame.Rect(
                    self.ball_pos[0] - self.ball_radius,
                    self.ball_pos[1] - self.ball_radius,
                    self.ball_radius * 2,
                    self.ball_radius * 2,
                )
            ):
                print("Goalie made contact with the ball!")
                self.goalie.score += 1
                # Reset ball position
                self.ball_pos = [0, 0]
                self.shooting = False

            # Check if the ball is inside the goal
            elif (
                self.ball_pos[1] > self.HEIGHT // 2 - self.GOAL_WIDTH // 2
                and self.ball_pos[1] < self.HEIGHT // 2 + self.GOAL_WIDTH // 2
                and self.ball_pos[0] > self.WIDTH - self.GOAL_WIDTH
            ):
                print("Goal scored!")
                self.player.score += 1
                # Reset ball position
                self.ball_pos = [0, 0]
                self.shooting = False
            # Clear the screen
            self.screen.fill(self.GREEN)

            # Draw the lacrosse field lines
            pygame.draw.rect(self.screen, self.WHITE, (0, 0, self.WIDTH, self.HEIGHT), 2)
            pygame.draw.line(self.screen, self.WHITE, (self.WIDTH // 2, 0), (self.WIDTH // 2, self.HEIGHT), 2)

            # Draw the goal triangle
            pygame.draw.polygon(self.screen, self.RED, self.goal_vertices)

            # Draw the crease circle
            pygame.draw.circle(self.screen, self.WHITE, (int(self.crease_center[0]), int(self.crease_center[1])),
                            self.crease_radius, 2)

            # Draw the player
            self.player.draw(self.screen)

            # Draw the goalie
            self.goalie.draw(self.screen)

            # Draw the ball if shooting
            if self.shooting:
                self.shoot(self.destination_x, self.destination_y)
                self.draw_ball()  # Draw the ball during the shooting

            # Display scores
            player_text = self.font.render(f"Player: {self.player.score}", True, self.WHITE)
            goalie_text = self.font.render(f"Goalie: {self.goalie.score}", True, self.WHITE)
            self.screen.blit(player_text, (10, 10))
            self.screen.blit(goalie_text, (10, 40))

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(60)

    def is_inside_crease(self, x, y):
        # Check if the point (x, y) is inside the crease circle
        crease_center_x, crease_center_y = self.crease_center
        crease_radius = self.crease_radius
        distance_to_center = math.sqrt((x - crease_center_x) ** 2 + (y - crease_center_y) ** 2)
        return distance_to_center <= crease_radius


if __name__ == "__main__":
    g = Game()
    g.run_game()