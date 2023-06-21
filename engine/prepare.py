import pygame
from os import path

RESOLUTION = 1920, 1080
FPS = 30
TITLE = "Harry Potter : Bataille à Poudlard"
VERSION = '0.2'

pygame.init()
SCREEN = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption(TITLE)

AQUIFER = {x: pygame.font.Font('fonts/Aquifer.ttf', x) for x in range(16, 64)}



