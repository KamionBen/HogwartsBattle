import pygame
from . import prepare


class Control:
    def __init__(self, state_dict, current_state_name):
        self.state_dict = state_dict
        self.current_state = current_state_name
        self.state = self.state_dict[current_state_name]
        self.clock = pygame.time.Clock()
        self.state.startup()

    def main_game_loop(self):
        while not self.state.quit:
            self.clock.tick(prepare.FPS)
            self.event_loop()
            self.update()
            pygame.display.flip()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.quit = True
            self.state.get_event(event)

    def update(self):
        self.state.update()
        self.state.draw(prepare.SCREEN)
        if self.state.done:
            self.flip_state()

    def flip_state(self):
        self.state.done = False
        previous, self.current_state = self.current_state, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.current_state]
        self.state.startup()
        self.state.previous = previous
