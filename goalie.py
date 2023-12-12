import random
import bot
import pygame
from fsm import FSM

class Goalie:
    def __init__(self, game, x, y):
        # Initializes variables
        self.x = x
        self.y = y
        self.game = game
        self.movement_speed = 2
        self.block_speed = 1
        self.movement_direction = random.choice([-1, 1])
        self.score = 0

        # Initializes FSM with starting state "IDLE"
        self.fsm = FSM("IDLE")
        self.init_fsm()

    def init_fsm(self):
        # State transitions added
        self.fsm.add_transition(None, "IDLE", action=self.move_back_and_forth, next_state="IDLE")
        self.fsm.add_transition("BallShot", "IDLE", action=self.block_goal, next_state="BLOCKING")
        self.fsm.add_transition("BallShot", "BLOCKING", action=self.block_goal, next_state="BLOCKING")
        self.fsm.add_transition("BallShot", "CELEBRATING", action=self.block_goal, next_state="BLOCKING")
        self.fsm.add_transition("ShotComplete", "BLOCKING", action=self.move_back_and_forth, next_state="IDLE")
        self.fsm.add_transition("ShotComplete", "IDLE", action=self.move_back_and_forth, next_state="IDLE")
        self.fsm.add_transition("BallSaved", "BLOCKING", action=self.move_back_and_forth, next_state="CELEBRATING")
        self.fsm.add_transition("BallSaved", "CELEBRATING", action=self.celebrate, next_state="IDLE")
        self.fsm.add_transition("BallSaved", "IDLE", action=self.move_back_and_forth, next_state="IDLE")
        self.fsm.add_transition("GoalScored", "BLOCKING", action=self.move_back_and_forth, next_state="IDLE")
        self.fsm.add_transition("CelebrationComplete", "CELEBRATING", action=self.move_back_and_forth, next_state="IDLE")
        self.fsm.add_transition("CelebrationComplete", "BLOCKING", action=self.move_back_and_forth, next_state="IDLE")
        self.fsm.add_transition("CelebrationComplete", "IDLE", action=self.move_back_and_forth, next_state="IDLE")
        self.fsm.add_transition("DoneCelebrating", "CELEBRATING", action=self.move_back_and_forth, next_state="IDLE")
        self.fsm.add_transition("DoneCelebrating", "IDLE", action=self.move_back_and_forth, next_state="IDLE")
        self.fsm.add_transition("DoneCelebrating", "BLOCKING", action=self.move_back_and_forth, next_state="IDLE")
        self.fsm.add_transition("GoalScored", "IDLE", action=self.move_back_and_forth, next_state="IDLE")
        pass

    # Uses the finite state machine to process the goalies input
    def update(self, state):
        self.fsm.process(state)

    # Moves the goalie vertically back and forth
    def move_back_and_forth(self):
        self.y += self.movement_speed * self.movement_direction

        # Reverses direction if reaching the vertical boundaries
        if self.y <= self.game.HEIGHT // 2 - self.game.GOALIE_RANGE or self.y >= self.game.HEIGHT // 2 + self.game.GOALIE_RANGE:
            self.movement_direction *= -1

    # Move towards the ball on the linear plane of the goal width
    def block_goal(self):
        if self.game.ball_pos[1] < self.y:
            self.y -= min(self.block_speed, self.y - (self.game.HEIGHT // 2 - self.game.GOALIE_RANGE))
        else:
            self.y += min(self.block_speed, (self.game.HEIGHT // 2 + self.game.GOALIE_RANGE) - self.y)

    # Goalie celebrates after saved goals
    def celebrate(self):
        print("Celebrating")
        
    # Draws the goalie
    def draw(self, screen):
        pygame.draw.rect(screen, self.game.WHITE, (self.x, self.y, self.game.PLAYER_SIZE, self.game.PLAYER_SIZE))