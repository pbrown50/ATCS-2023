import random
import bot
import pygame
import game
class Goalie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.movement_speed = 2
        self.movement_direction = random.choice([-1, 1])
        self.state_machine = bot.FSMGoalie()
        self.score = 0

        # Variables for celebrating state
        self.celebration_timer = 0
        self.celebration_duration = 3  # in seconds

    def update(self, ball_pos):
        self.move_randomly()

        # Perform actions based on the goalie's current state
        if self.state_machine.fsm.current_state == "BLOCKING":
            self.block_goal(ball_pos)
        elif self.state_machine.fsm.current_state == "CELEBRATING":
            self.celebrate()
        elif self.state_machine.fsm.current_state == "IDLE":
            self.move_back_and_forth()

        # Update the celebration timer
        if self.celebration_timer > 0:
            self.celebration_timer -= 1 / 60  # 60 frames per second

    def move_back_and_forth(self):
        # Move vertically back and forth
        self.y += self.movement_speed * self.movement_direction

        # Reverse direction if reaching the vertical boundaries
        if self.y <= game.HEIGHT // 2 - game.GOALIE_RANGE or self.y >= game.HEIGHT // 2 + game.GOALIE_RANGE:
            self.movement_direction *= -1

    def block_goal(self, ball_pos):
        # Move towards the ball on the linear plane of the goal width
        if ball_pos[1] < self.y:
            self.y -= min(self.movement_speed, self.y - (game.HEIGHT // 2 - game.GOALIE_RANGE))
        elif ball_pos[1] > self.y:
            self.y += min(self.movement_speed, (game.HEIGHT // 2 + game.GOALIE_RANGE) - self.y)

    def celebrate(self):
        # Rapidly change colors for the celebration duration
        if self.celebration_timer > 0:
            self.color_change()

    def color_change(self):
        # Example color change logic (you can modify this as needed)
        color_change_rate = 10  # The higher the rate, the faster the color change
        r = (self.celebration_timer * color_change_rate) % 255
        g = (self.celebration_timer * color_change_rate * 1.5) % 255
        b = (self.celebration_timer * color_change_rate * 2) % 255
        pygame.draw.rect(game.screen, (r, g, b), (self.x, self.y, game.PLAYER_SIZE, game.PLAYER_SIZE))

    def draw(self, screen):
        # Draw the goalie
        pygame.draw.rect(screen, game.WHITE, (self.x, self.y, game.PLAYER_SIZE, game.PLAYER_SIZE))