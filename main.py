import sys
import pygame
from engine import control
from engine.states import game


states_dict = {
    'game': game.Game(),
}
app = control.Control(states_dict, 'game')

app.main_game_loop()
pygame.quit()
sys.exit()
