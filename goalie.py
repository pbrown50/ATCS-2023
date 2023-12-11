import random
import bot
import pygame
from fsm import FSM

class Goalie:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game
        self.movement_speed = 2
        self.movement_direction = random.choice([-1, 1])
        self.score = 0

        # Variables for celebrating state
        self.celebration_timer = 0
        self.celebration_duration = 3  # in seconds

        self.fsm = FSM("IDLE")
        self.init_fsm()

    def init_fsm(self):
        self.fsm.add_transition(None, "IDLE", action=self.move_back_and_forth,  next_state="IDLE")
        self.fsm.add_transition("BallShot", "IDLE", action=self.block_goal,  next_state="BLOCKING")
        self.fsm.add_transition("BallShot", "BLOCKING", action=self.block_goal,  next_state="BLOCKING")
        self.fsm.add_transition("BallShot", "CELEBRATING", action=self.block_goal,  next_state="BLOCKING")
        self.fsm.add_transition('BallSaved', 'BLOCKING', action=self.move_back_and_forth,  next_state="IDLE")
        self.fsm.add_transition('BallSaved', 'CELEBRATING', action=self.celebrate,  next_state="IDLE")
        self.fsm.add_transition('BallSaved', 'IDLE', action=self.move_back_and_forth,  next_state="IDLE")
        # self.fsm.add_transition("BallSaved", "BLOCKED", action=self.celebrate,  next_state="CELEBRATING")
        self.fsm.add_transition("DoneCelebrating", "CELEBRATING", action=self.move_back_and_forth,  next_state="IDLE")
        self.fsm.add_transition("GoalScored", "BLOCKING", action=self.move_back_and_forth,  next_state="IDLE")
        self.fsm.add_transition("CelebrationComplete", "CELEBRATING", action=self.move_back_and_forth,  next_state="IDLE")
        self.fsm.add_transition("CelebrationComplete", "BLOCKING", action=self.move_back_and_forth,  next_state="IDLE")
        self.fsm.add_transition("CelebrationComplete", "IDLE", action=self.move_back_and_forth,  next_state="IDLE")

        self.fsm.add_transition("DoneCelebrating", "IDLE", action=self.move_back_and_forth,  next_state="IDLE")
        # self.fsm.add_transition("DoneCelebrating", "BLOCKED", action=self.move_back_and_forth,  next_state="IDLE")
        self.fsm.add_transition("DoneCelebrating", "BLOCKING", action=self.move_back_and_forth,  next_state="IDLE")

        self.fsm.add_transition("GoalScored", "IDLE", action=self.move_back_and_forth,  next_state="IDLE")
        
        pass

    def update(self, state):
        self.fsm.process(state)

    def move_back_and_forth(self):
        # Move vertically back and forth
        self.y += self.movement_speed * self.movement_direction

        # Reverse direction if reaching the vertical boundaries
        if self.y <= self.game.HEIGHT // 2 - self.game.GOALIE_RANGE or self.y >= self.game.HEIGHT // 2 + self.game.GOALIE_RANGE:
            self.movement_direction *= -1

    def block_goal(self):
        # Move towards the ball on the linear plane of the goal width
        if self.game.ball_pos[1] < self.y:
            self.y -= min(self.movement_speed, self.y - (self.game.HEIGHT // 2 - self.game.GOALIE_RANGE))
        else:
            self.y += min(self.movement_speed, (self.game.HEIGHT // 2 + self.game.GOALIE_RANGE) - self.y)

    def celebrate(self):
        # Rapidly change colors for the celebration duration
        # if self.celebration_timer > 0:
        #     self.celebration_timer -= 1 / 60  # 60 frames per second
        #     self.color_change()
        print("Celebrating")
        

    def color_change(self):
        # Example color change logic (you can modify this as needed)
        color_change_rate = 10  # The higher the rate, the faster the color change
        r = (self.celebration_timer * color_change_rate) % 255
        g = (self.celebration_timer * color_change_rate * 1.5) % 255
        b = (self.celebration_timer * color_change_rate * 2) % 255
        pygame.draw.rect(self.game.screen, (r, g, b), (self.x, self.y, self.game.PLAYER_SIZE, self.game.PLAYER_SIZE))

    def draw(self, screen):
        # Draw the goalie
        pygame.draw.rect(screen, self.game.WHITE, (self.x, self.y, self.game.PLAYER_SIZE, self.game.PLAYER_SIZE))