import pygame
from .. import common, prepare, Cards


class Game(common.State):
    def __init__(self):
        common.State.__init__(self)

        self.image = pygame.Surface(prepare.RESOLUTION)

    def startup(self):
        locations = Cards.import_locations(1)
        self.image.blit(locations[0].image, (0,0))

    def draw(self, screen):
        screen.fill('black')
        screen.blit(self.image, (0,0))