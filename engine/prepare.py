import pygame
from os import path


class Font:
    def __init__(self, filepath: str, **kw):
        for k, v in kw.items():
            self.__setattr__(k, pygame.font.Font(filepath, v))



RESOLUTION = 1920, 1080
FPS = 30
TITLE = "Harry Potter : Bataille à Poudlard"
VERSION = '0.2'

pygame.init()
SCREEN = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption(TITLE)

AQUIFER = Font('fonts/Aquifer.ttf', **{'S': 24, 'M': 32, 'L': 40})
ENCHANTED = Font('fonts/Enchanted Land.otf', **{'S': 32, 'M': 48, 'L': 64, 'XL': 80})



