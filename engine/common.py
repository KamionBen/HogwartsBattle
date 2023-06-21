import pygame
from pygame.constants import *


class State:
    game_data = {}

    def __init__(self):
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None

        self.buttons = []

    def update(self):
        """ Do things every tick """

    def draw(self, screen):
        """ Draw stuff on screen """

    def startup(self):
        """ Do things when the State start """

    def cleanup(self):
        """ Do things when the State end """

    def get_event(self, event):
        """ Basic events """
        if event.type == MOUSEBUTTONUP:
            if event.button == BUTTON_LEFT:
                for button in self.buttons:
                    if button.rect.collidepoint(event.pos) and button.function is not None:
                        if button.param is None:
                            button.function()
                        else:
                            button.function(**button.param)
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                self.cancel()

    def validate(self):
        """ Enter, or cross button """
        pass

    def cancel(self):
        """ Backspace or circle """
        pass
