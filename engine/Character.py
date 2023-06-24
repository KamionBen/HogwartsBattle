from engine import Cards, prepare, pg_func
import pygame
from pygame.constants import *


class Profile:
    def __init__(self, name, **kw):
        self.name = name
        for k, v in kw.items():
            self.__setattr__(k, v)


class Character(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.firstname = name.split(' ')[0]
        self.char_image = prepare.CHAR_IMAGES[self.firstname]

        self.deck = Cards.import_basedeck(self.name)
        self.hand = Cards.Deck()
        self.played = Cards.Deck()
        self.discard_pile = Cards.Deck()

        self.health = 10
        self.influence = 0
        self.attack = 0
        self.effects = []
        self.triggers = []

        self.stunned = False
        self.has_discarded = False

        self.image = pygame.Surface((1120, 500), SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 400, 580
        self.active = False

        self.card_focus = 0

        self._damage_flag = False
        self._damage_index = 0

        self._heal_flag = False
        self._heal_index = 0

        self.main_panel = pygame.Surface((1120, 500), SRCALPHA, 32)
        self.side_panel = pygame.Surface((300, 500), SRCALPHA, 32)
        self._load()


    def _draw_mainpanel(self):
        """ Draw Main Panel"""
        self.image.blit(self.main_panel, (0, 0))
        """ Draw Health """
        for i in range(self.health):
            self.image.blit(prepare.HEART, (360 + i * 47, 60 + (i % 2) * 10))
        """ Draw Attack """
        txt = prepare.ENCHANTED.M.render(" x 2", True, 'black')  # TODO : Replace with actual number
        self.image.blit(prepare.ATTACK, (400, 130))
        self.image.blit(txt, (445, 120))
        """ Draw Influence """
        txt = prepare.ENCHANTED.M.render(" x 3", True, 'black')
        self.image.blit(prepare.INFLUENCE, (600, 130))
        self.image.blit(txt, (645, 120))
        """ Draw Discard """
        recto = Cards.Recto()
        self.main_panel.blit(pygame.transform.scale_by(recto.image, 0.5), (130, 0))
        txt = prepare.TIMES.XS.render("Défausse : 0", True, 'white')
        self.main_panel.blit(txt, (150, 175))

        """ Draw Played """
        recto = Cards.Recto()
        self.main_panel.blit(pygame.transform.scale_by(recto.image, 0.5), (0, 0))
        txt = prepare.TIMES.XS.render("Jouée : 0", True, 'white')
        self.main_panel.blit(txt, (0, 175))

        """ Draw Deck """
        self.main_panel.blit(pygame.transform.scale_by(recto.image, 0.5), (862, 0))
        txt = prepare.TIMES.XS.render("Deck : 5", True, 'white')
        self.main_panel.blit(txt, (892, 175))

        """ Health Animations """
        if self._damage_flag:
            i = self.health
            position = (360 + i * 47, 60 + (i % 2) * 10)
            self.image.blit(prepare.HEART_LOSE[self._damage_index], position)
            self._damage_index += 1
            if self._damage_index >= len(prepare.HEART_LOSE):
                self._damage_flag = False
                self._damage_index = 0

        if self._heal_flag:
            i = self.health - 1
            position = (360 + i * 47, 60 + (i % 2) * 10)
            self.image.blit(prepare.HEART_GAIN[self._heal_index], position)
            self._heal_index += 1
            if self._heal_index >= len(prepare.HEART_GAIN):
                self._heal_flag = False
                self._heal_index = 0

        """ Draw Hand """
        left = (320 + (252 * len(self.hand))) / 2
        for i, card in enumerate(reversed(self.hand)):
            self.image.blit(pg_func.outline(card.small, 'black'), (left - i * 150, 200))

        if self.card_focus != 0:
            self.image.blit(pg_func.outline(self.hand[self.card_focus].image, 'black'),
                            (left - self.card_focus * 150, 150))

    def _draw_sidepanel(self):
        self.image.blit(self.side_panel, (0,0))

    def update(self):
        """ Update the image every tick """
        if self.active:
            self._draw_mainpanel()
        else:
            self._draw_sidepanel()


    def _load(self):
        self._load_mainpanel()
        self._load_sidepanel()

    def _load_sidepanel(self):
        self.side_panel.fill('blue')

    def _load_mainpanel(self):
        # Red = Full panel
        #self.main_panel.fill('red')
        # Panel = 600 * 195
        pygame.draw.rect(self.main_panel, 'black', self.main_panel.get_rect(), border_radius=10)
        pygame.draw.rect(self.main_panel, (40, 40,40), self.main_panel.get_rect(), width=2, border_radius=10)

        # Blue = Char infos
        #pygame.draw.rect(self.main_panel, 'blue', (360, 0, 600, 195))
        self.main_panel.blit(prepare.PANEL, (260, 0))

        # Image
        self.main_panel.blit(self.char_image, (260, 0))

        # Name
        name = prepare.ENCHANTED.M.render(self.name.replace(' ', '  '), True, 'black')
        shdw = prepare.ENCHANTED.M.render(self.name.replace(' ', '  '), True, 'white')
        self.main_panel.blit(shdw, (360+1, 1))
        self.main_panel.blit(name, (360, 0))

        # Health
        for i in range(10):
            heart = pygame.transform.grayscale(prepare.HEART)
            heart.set_alpha(128)
            self.main_panel.blit(heart, (360 + i * 47, 60 + (i % 2) * 10))


    def heal(self, nb):
        if not self.stunned:
            self.health = min(self.health + nb, 10)
            self._heal_flag = True

    def __repr__(self):
        return self.name

    def get_damage(self, nb):
        if not self.stunned:
            self.health -= nb
            self._damage_flag = True

    def gain_influence(self, nb):
        self.influence += nb

    def gain_attack(self, nb):
        self.attack += nb

    def pick(self, nb):
        for _ in range(nb):
            if len(self.deck) == 0:
                self.discard_pile.shuffle()
                self.deck, self.discard_pile = self.discard_pile, Cards.Deck()
            self.hand.append(self.deck.pick())
        for card in self.hand:
            if "in_hand" in card.mechanics.keys():
                for elt in card.mechanics['in_hand']:
                    if elt not in self.effects:
                        self.effects.append(elt)

    def pick_five(self):
        self.pick(5)

    def play(self, card):
        self.hand.remove(card)
        self.played.append(card)

    def discard(self, card):
        self.hand.remove(card)
        self.discard_pile.append(card)

    def buy(self, card: Cards.Hogwarts, discard=True):
        if discard:
            self.discard_pile.append(card)
        else:
            self.deck.insert(0, card)
        self.influence -= card.cost

    def endturn(self):
        for card in self.hand:
            self.discard_pile.append(card)
        for card in self.played:
            self.discard_pile.append(card)
        self.played = Cards.Deck()
        self.hand = Cards.Deck()
        self.influence = 0
        self.attack = 0
        self.pick_five()

    def clear_effects(self):
        self.effects = []
        self.triggers = []
