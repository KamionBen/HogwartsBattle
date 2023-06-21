import pygame
from .. import common, prepare


class Game(common.State):
    def __init__(self):
        common.State.__init__(self)

        self.bg = None

    def startup(self):
        self.bg = pygame.image.load("images/locations/diagonalley.png").convert()

    def draw(self, screen):
        screen.fill('black')
        screen.blit(self.bg, (0,0))