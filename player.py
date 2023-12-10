import pygame

class Player:
    def __init__(self, x, y, PLAYER_SIZE, PLAYER_SPEED):
        self.x = x
        self.y = y
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.score = 0
        self.WHITE = (255, 255, 255)

    def draw(self, screen):
        # Draw the player
        pygame.draw.rect(screen, self.WHITE, (self.x, self.y, self.size, self.size))
