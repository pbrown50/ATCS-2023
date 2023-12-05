import pygame
import goalie
from fsm import FSM

class Goalie():

    def __init__(self, game, x=50, y=50):
        super().__init__()

        self.game = game

        self.fsm = FSM("S")
        self.init_fsm()
    
    def init_fsm(self):
        self.fsm.add_transition("BallShot", "IDLE", action=goalie.block_goal())
        self.fsm.add_transition("GoalScored", "BLOCKING", action=goalie.celebrate())
        self.fsm.add_transition("CelebrationComplete", "CELEBRATING", action=goalie.move_back_and_forth())
        pass
    
    def get_state(self):
        # TODO: Return the maze bot's current state
        return self.fsm.current_state
    
    