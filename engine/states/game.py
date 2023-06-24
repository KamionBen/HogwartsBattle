import pygame
from pygame.constants import *
from .. import common, prepare, Cards, Character


class Game(common.State):
    def __init__(self):
        common.State.__init__(self)

        self.image = pygame.Surface(prepare.RESOLUTION)
        self.locations = None
        self.sample = Cards.import_hogwarts(1)
        self.sample.shuffle()
        self.board = Cards.OrderedDeck()
        while self.board.get_vacant() != 0:
            self.board.add(self.sample.pick())
        self.darkarts = Cards.import_darkarts(1)
        self.villains = Cards.import_villains(1)

        self.board_button = pygame.Rect((1370, 5, 547, 501))
        self.panel_flag = False
        self.panel_str = None

        self.character = Character.Character('Ron Weasley')
        self.character.pick_five()
        self.character.active = True

        self.focus_button = []

    def startup(self):
        self.locations = Cards.import_locations(1)

        self.game_year = pygame.Surface((400, 50), SRCALPHA, 32)
        for i in range(200):
            vert = pygame.Surface((1, 50), SRCALPHA, 32)
            vert.fill('black')
            vert.set_alpha(255-i)
            self.game_year.blit(vert, (199-i, 0))
            self.game_year.blit(vert, (200+i, 0))

        year = prepare.ENCHANTED.M.render("Jeu 1", True, 'white')
        shdw = prepare.ENCHANTED.M.render("Jeu 1", True, 'black')
        self.game_year.blit(shdw, ((400 - year.get_width()) / 2 + 1, 1))
        self.game_year.blit(year, ((400 - year.get_width()) / 2, 0))
        left = (1070 + (252 * len(self.character.hand))) / 2
        for i, card in enumerate(self.character.hand):
            self.focus_button.append((pygame.Rect(left - i * 155, 780, 155, 240), i))
            #pygame.draw.rect(self.image, 'green', (left - i * 155, 780, 155, 240), width=1)

    def panel(self, kind: str) -> pygame.Surface:
        """ Return a panel to be blitted over the screen """
        surface = pygame.Surface(prepare.RESOLUTION, SRCALPHA, 32)
        surface.fill((0, 0, 0, 128))
        if kind == "board":
            for i, card in enumerate(self.board):
                if card is not None:
                    #  (252, 348)
                    span = 5
                    left, top = (1920-(252+span)*3)/2, 100
                    position = (left + (i % 3) * (252 + span), top + (i % 2) * (348 + span))
                    surface.blit(card.image, position)
        return surface

    def cancel(self):
        self.panel_flag = False
        self.panel_str = None

    def set_panel(self, string=None):
        self.panel_str = string



    def update(self):
        self.locations[0].update()
        self.character.update()

    def get_event(self, event):
        self.character.card_focus = 0
        for rect, i in self.focus_button:
            if rect.collidepoint(pygame.mouse.get_pos()):
                self.character.card_focus = i

        if event.type == KEYUP:
            if event.key == K_DOWN:
                self.character.get_damage(1)
            if event.key == K_UP:
                self.character.heal(1)
            if event.key == K_ESCAPE:
                self.cancel()
            if self.locations[0].is_dead():
                self.locations[0].add_token(-1)
            else:
                self.locations[0].add_token()
                self.locations[0].anim_tick = pygame.time.get_ticks()
        if event.type == MOUSEBUTTONUP:
            if event.button == BUTTON_LEFT and self.board_button.collidepoint(event.pos):
                if self.panel_flag:
                    self.set_panel()
                    self.panel_flag = False
                else:
                    self.set_panel('board')
                    self.panel_flag = True


    def draw(self, screen):
        self.image.fill('black')
        self.image.blit(self.locations[0].image, (0, 0))

        self.image.blit(self.game_year, (760, 0))
        self.image.blit(self.darkarts[0].image, (810, 60))
        self.image.blit(self.board.get_image(), (1370, 5))
        pygame.draw.rect(self.image, 'green', (1370, 5, 547, 501), width=1)
        self.image.blit(self.character.image, (300, 580))

        left = (1070 + (252 * len(self.character.hand))) / 2
        for i, card in enumerate(self.character.hand):
            pygame.draw.rect(self.image, 'green', (left - i * 155, 780, 155, 240), width = 1)

        screen.blit(self.image, (0,0))

        if self.panel_flag:
            screen.blit(self.panel(self.panel_str), (0,0))

