import pygame
from pygame.constants import *
from .. import common, prepare, Cards


class Game(common.State):
    def __init__(self):
        common.State.__init__(self)

        self.image = pygame.Surface(prepare.RESOLUTION)
        self.locations = None
        self.sample = None

    def startup(self):
        self.locations = Cards.import_locations(1)
        self.sample = Cards.import_basedeck("Hermione Granger")


    def update(self):
        self.locations[0].update()

    def get_event(self, event):
        if event.type == KEYUP:
            if self.locations[0].is_dead():
                self.locations[0].add_token(-1)
            else:
                self.locations[0].add_token()
                self.locations[0].anim_tick = pygame.time.get_ticks()


    def draw(self, screen):
        screen.fill('black')
        self.image.blit(self.locations[0].image, (0, 0))
        self.image.blit(self.sample[1].image, (600, 600))
        screen.blit(self.image, (0,0))
        year = prepare.ENCHANTED.M.render("Jeu 1", True, 'white')
        shdw = prepare.ENCHANTED.M.render("Jeu 1", True, 'black')
        screen.blit(shdw, ((prepare.RESOLUTION[0] - year.get_width())/2 + 1, 1))
        screen.blit(year, ((prepare.RESOLUTION[0] - year.get_width())/2,0 ))
