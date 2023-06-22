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

AQUIFER = Font('fonts/Aquifer.ttf', **{'XS': 16, 'S': 24, 'M': 32, 'L': 40})
ENCHANTED = Font('fonts/Enchanted Land.otf', **{'S': 32, 'M': 48, 'L': 64, 'XL': 80})

YELLOW = 201, 200, 77
RED = 146, 40, 47
BLUE = 64, 105, 158

ATTACK = pygame.image.load('images/tokens/attack.png').convert_alpha()
DARKARTS = pygame.image.load('images/tokens/darkarts.png').convert_alpha()
HEART = pygame.image.load('images/tokens/heart.png').convert_alpha()
INFLUENCE = pygame.image.load('images/tokens/influence.png').convert_alpha()
MARK = pygame.image.load('images/tokens/marque.png').convert_alpha()

