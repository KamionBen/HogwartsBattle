import pygame
from pygame.constants import *
from os import path

RESOLUTION = 1920, 1080
FPS = 30
TITLE = "Harry Potter : Bataille à Poudlard"
VERSION = '0.2'

pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

AQUIFER = {x: pygame.font.Font('fonts/Aquifer.ttf', x) for x in range(16, 64)}


def get_location_img(imgfile) -> pygame.Surface:
    """ Return the image with a black gradient """
    image = pygame.Surface((1920, 720), SRCALPHA, 32)
    image.blit(pygame.image.load(imgfile).convert_alpha(), (0, 0))
    for i in range(256):
        surf = pygame.Surface((1920, 2), SRCALPHA, 32)
        surf.fill((0,0,0, 255-i))
        image.blit(surf, (0, 718-i*2))

    return image

BG = get_location_img('images/locations/diagonalley.png')

game_on = True
while game_on:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            game_on = False
    screen.fill('black')
    screen.blit(BG, (0,0))
    pygame.display.flip()