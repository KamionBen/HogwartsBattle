import json
from random import shuffle
import pygame
from pygame.locals import SRCALPHA
from engine import prepare, pg_func

from os import path


def clean_text(text):
    replaces = {'!éclairs': 'éclairs'.upper(), '!éclair': 'éclair'.upper(),
                '!mornilles': 'MORNILLES', '!mornille': 'MORNILLE',
                '!coeurs': 'COEURS', '!coeur': 'COEUR'}
    for k, v in replaces.items():
        text = text.replace(k, v)
    return text


""" MOTHER CLASSES """


class Card(pygame.sprite.Sprite):
    def __init__(self, name: str, year: int):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.year = year

        self.mechanics = {}

    def __repr__(self):
        return self.name


class Deck(pygame.sprite.Group):
    def __init__(self, *cards):
        """ A group of any cards  """
        pygame.sprite.Group.__init__(self)
        self._cards = [c for c in cards]

    def append(self, card):
        self._cards.append(card)

    def get(self, item):
        for elt in self._cards:
            if elt == item:
                return elt

    def shuffle(self):
        shuffle(self._cards)

    def copy(self):
        return [e for e in self._cards]

    def pick(self) -> Card:
        return self._cards.pop(0)

    def remove(self, card):
        self._cards.remove(card)

    def insert(self, index, item):
        self._cards.insert(index, item)

    def __iter__(self):
        return iter(self._cards)

    def __repr__(self):
        return str(self._cards)

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, index):
        return self._cards[index]


class OrderedDeck(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        """ Represent and manage de 6 Hogwarts cards """
        self._cards = [None for _ in range(6)]

        self.image = pygame.Surface((400, 600), SRCALPHA, 32)
        self.rect = self.image.get_rect()

    def get_image(self):
        # (252, 348)
        image = pygame.Surface((781, 716), SRCALPHA, 32)
        #image.fill('blue')
        for i, card in enumerate(self._cards):
            if card is not None:
                position = (5 + (i % 3) * 257, 5 + (i % 2) * 353)
                image.blit(pg_func.outline(card.image), position)
        return pygame.transform.scale_by(image, 0.7)

    def get_vacant(self):
        vacant = 0
        for elt in self._cards:
            if elt is None:
                vacant += 1
        return vacant

    def add(self, newcard: Card):
        if self.get_vacant() == 0:
            raise IndexError
        else:
            for i, card in enumerate(self._cards):
                if card is None:
                    self._cards[i] = newcard
                    break

    def remove(self, rm_card: Card):
        found = False
        for i, card in enumerate(self._cards):
            if card == rm_card:
                self._cards[i] = None
                found = True

        if not found:
            raise IndexError(f"{rm_card} n'a pas été trouvée")

    def __len__(self):
        return 6-self.get_vacant()

    def __iter__(self):
        return iter(self._cards)


""" DAUGHTER CLASSES """







class Location(Card):
    def __init__(self, year, order, name, events_nb, control_nb, image_file):
        """ Une carte Lieu """
        Card.__init__(self, name, year)
        self.order = order  # (current, total)

        self.event_nb = events_nb
        self.control_nb, self.control_nb_max = 0, control_nb

        self.image = pygame.Surface((1920, 720), SRCALPHA, 32)
        self.rect = self.image.get_rect()

        self._img_file = image_file
        self._background = self.image.copy()

        self.anim_tick = 0
        self.blink_list = []
        self.alert = None

        self._load()
        self.update()



    def _load(self):
        """ Load the images and create the fixed image """
        """ Blit image """
        img = pygame.image.load(path.join('images/locations', self._img_file)).convert_alpha()
        self._background.blit(img, (0,0))
        """ Create horizontal and vertical gradients"""
        for i in range(256):
            stripe = pygame.Surface((1920, 2), SRCALPHA, 32)
            stripe.fill((0,0,0, 255-i))
            self._background.blit(stripe, (0, 718-i*2))
            v_stripe = pygame.Surface((3, 200), SRCALPHA, 32)
            v_stripe.fill((0, 0, 0, 255-i))
            self._background.blit(v_stripe, (i*3, 0))
        """ Display the number of dark events """
        for i in range(self.event_nb):
            da = pygame.transform.scale(prepare.DARKARTS, (40, 40))
            outlined = pg_func.outline(da)
            self._background.blit(outlined, (200 + i * 50, 11))
        """ Order and shadow """
        lieu = prepare.AQUIFER.M.render(f"LIEU {self.order[0]}/{self.order[1]}", True, 'yellow')
        shdw = prepare.AQUIFER.M.render(f"LIEU {self.order[0]}/{self.order[1]}", True, 'black')

        self._background.blit(pg_func.outline(shdw, 'black'), (22, 22))
        self._background.blit(lieu, (20, 20))
        """ Name and shadow """

        name = prepare.ENCHANTED.XL.render(self.name, True, 'white')
        shdw = prepare.ENCHANTED.XL.render(self.name, True, 'black')
        self._background.blit(pg_func.outline(shdw, 'black'), (22, 52))
        self._background.blit(name, (20, 50))
        """ Alert """
        self.alert = pygame.Surface((name.get_width(), name.get_height()), SRCALPHA, 32).convert_alpha()
        alert = prepare.ENCHANTED.XL.render(self.name, True, (255, 0, 0))
        self.alert.blit(alert, (0,0))

        """ Background token images """
        for i in range(self.control_nb_max):
            inactive_mark = pygame.transform.grayscale(prepare.MARK)
            inactive_mark.set_alpha(128)
            self._background.blit(inactive_mark, (50 + i * 50, 135 + (i % 2*10)))

        high = [(2/7)*x**2 for x in range(30)]
        low = high.copy()
        low.reverse()
        self.blink_list = [0 for _ in range(15)] + high + low + [0 for _ in range(15)]
        self.blink_list = [int(e) for e in self.blink_list]


    def update(self):
        """ Change the numbers of tokens """
        self.image.blit(self._background, (0, 0))
        for i in range(self.control_nb):
            position = (50 + i * 50, 135 + (i % 2*10))
            self.image.blit(prepare.MARK, position)

        if self.is_dead():
            tick = pygame.time.get_ticks()
            tick = int(tick//(100/3) % len(self.blink_list))
            alert = self.alert.copy()
            alert.set_alpha(self.blink_list[tick])
            self.image.blit(alert, (20, 50))

    def is_dead(self):
        return self.control_nb == self.control_nb_max

    def add_token(self, nb=1):
        self.control_nb = min(self.control_nb + nb, self.control_nb_max)


class Villain(Card):
    def __init__(self, year, name, health, description, reward, mechanics):
        Card.__init__(self, name, year)
        self.description = description
        self.reward = reward

        self.health, self.health_max = 0, health
        self.mechanics = mechanics
        self.attack_tokens = 0
        self.image = pygame.Surface((306, 228))
        self.rect = self.image.get_rect()

    def update(self):

        """ FRAME """
        """
        self.image.fill('black')
        pygame.draw.rect(self.image, (40, 40, 40), (1, 1, self.rect.width-2, self.rect.height-2), border_radius=5)

        subtext = AQUIFER[20].render("ENNEMI", True, 'yellow')
        self.image.blit(subtext, (10, 10))

        text = ENCHANTED[48].render(self.name, True, 'white')
        self.image.blit(text, (10, 30))

        for i in range(self.health_max):
            position = (5 + i * 45, 80 + (i%2 * 10))
            if self.health + self.attack_tokens < i + 1:
                token = pygame.transform.grayscale(TOKEN)
                token.set_alpha(128)
                self.image.blit(token, position)
            else:

                self.image.blit(TOKEN, position)
        """

        #health = FONT[28].render(f"{self.health}/{self.health_max}", True, 'white')
        #self.image.blit(health, (250, 10))

        #tokens = FONT[20].render(f"Attack tokens : {self.attack_tokens}", True, 'white')
        #self.image.blit(tokens, (140, 120))

        #description = FONT[22].render(self.description, True, 'grey')
        #self.image.blit(description, (5, 100))

        #reward = FONT[22].render(self.reward, True, 'grey')
        #self.image.blit(reward, (5, 150))

    def assign_token(self, nb):
        self.attack_tokens += nb

    def is_dead(self):
        return self.health + self.attack_tokens >= self.health_max

    def endturn(self):
        self.health += self.attack_tokens
        self.attack_tokens = 0

    def heal(self, nb):
        self.health = max(self.health - nb, self.health)


class DarkArts(Card):
    def __init__(self, year, name, description, mechanics):
        Card.__init__(self, name, year)
        self.description = description
        self.mechanics = mechanics

        self.image = pygame.Surface((300, 150))
        self.rect = self.image.get_rect()

        self._load()

    def _load(self):
        pygame.draw.rect(self.image, (40,40,40), self.rect, border_radius=8)
        pygame.draw.rect(self.image, 'white', self.rect, width=1, border_radius=8)

        pygame.draw.rect(self.image, 'grey', (75, 2, 150, 20))
        event = prepare.AQUIFER.XS.render("évènement".upper(), True, 'black')
        self.image.blit(event, ((300-event.get_width())/2, 3))
        text = clean_text(self.name.upper() + '\n' + self.description)
        text = text.replace('\n', '\n\n')
        surf = pg_func.render_textrect(text, prepare.AQUIFER.XS, pygame.Rect(0, 0, 290, 120), 'white')
        self.image.blit(surf, (5, 30))




    def update(self):

        """
        pygame.draw.rect(self.image, (40,40,40), (1,1,self.rect.width-2,self.rect.height-2), border_radius=5)
        text = AQUIFER[24].render(self.name, True, 'white')
        self.image.blit(text, (10,10))

        limit = 25
        phrase_ls = []
        string = ""
        for word in self.description.split(" "):
            if len(string + " " + word) < limit:
                string = string + " " + word
            else:
                phrase_ls.append(string)
                string = word
        phrase_ls.append(string)
        for i, phrase in enumerate(phrase_ls):
            description = FONT[20].render(phrase, True, 'white')
            self.image.blit(description, ((self.rect.width - description.get_width()) / 2, 70 + i * 20))
        """


class Hogwarts(Card):
    def __init__(self, year, name, description, genre, cost, mechanics):
        Card.__init__(self, name, year)
        self.description = description
        self.genre = genre
        self.cost = cost
        self.mechanics = mechanics

        # Card size : 6.3 / 8.7
        self.image = pygame.Surface((252, 348), SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.active = False

        self.small = None

        self._load()

    def _load(self):
        """ Create the image """
        top = 10
        colors = {"objet": prepare.YELLOW, "sort": prepare.RED, "allié": prepare.BLUE}

        pygame.draw.rect(self.image, (40, 40, 40), self.rect, border_radius=8)
        pygame.draw.rect(self.image, (165, 160, 112), (0, top + 30, 252, 159))
        pygame.draw.rect(self.image, colors[self.genre], (30, top, 192, 20))

        genre = prepare.AQUIFER.XS.render(self.genre.upper(), True, 'white')
        shdw = prepare.AQUIFER.XS.render(self.genre.upper(), True, 'black')
        self.image.blit(shdw, ((self.rect.width - genre.get_width()) / 2 + 1, top + 1))
        self.image.blit(genre, ((self.rect.width - genre.get_width()) / 2, top))

        text = f"{self.name.upper()}\n{self.description}"
        replaces = {'!éclairs': 'éclairs'.upper(), '!éclair': 'éclair'.upper(),
                    '!mornilles': 'MORNILLES', '!mornille': 'MORNILLE',
                    '!coeurs': 'COEURS', '!coeur': 'COEUR'}
        for k, v in replaces.items():
            text = text.replace(k, v)
        text = text.replace('\n', '\n\n')
        pg_text = pg_func.render_textrect(text, font=prepare.TIMES.XS, text_color='black', rect=pygame.Rect(0,0, 248, 174))

        self.image.blit(pg_text, (2, top + 35))

        if self.cost > 0:
            self.image.blit(pg_func.outline(prepare.INFLUENCE, 'black'), (210, top + 170))
            cost = prepare.AQUIFER.M.render(str(self.cost), True, 'white')
            self.image.blit(cost, (222, 187))

        self.small = pygame.transform.scale_by(self.image, 0.7)

    def update(self):
        """"""



CARD_DIR = "engine/cards"
# CARD_DIR = "cards"


def import_locations(year) -> Deck:
    with open(path.join(CARD_DIR, 'locations.json'), 'r', encoding='utf-8') as deck_file:
        data = json.load(deck_file)
    deck = Deck(*[Location(**c) for c in data if c['year'] == year])
    return deck


def import_darkarts(year) -> Deck:
    with open(path.join(CARD_DIR, 'darkarts.json'), 'r', encoding='utf-8') as deck_file:
        data = json.load(deck_file)
    deck = []
    for card in data:
        if card['year'] <= year:
            nb = card['nb']
            card.pop('nb')
            for i in range(nb):
                deck.append(card)
    deck = Deck(*[DarkArts(**c) for c in deck])
    deck.shuffle()
    return deck


def import_hogwarts(year) -> Deck:
    with open(path.join(CARD_DIR, 'hogwarts.json'), 'r', encoding='utf-8') as deck_file:
        data = json.load(deck_file)
    deck = []
    for card in data:
        if card['year'] <= year:
            nb = card['nb']
            card.pop('nb')
            for i in range(nb):
                deck.append(card)
    deck = Deck(*[Hogwarts(**c) for c in deck])
    deck.shuffle()
    return deck


def import_villains(year) -> Deck:
    with open(path.join(CARD_DIR, 'villains.json'), 'r', encoding='utf-8') as deck_file:
        data = json.load(deck_file)
    deck = Deck(*[Villain(**c) for c in data if c['year'] <= year])
    deck.shuffle()
    return deck


def import_basedeck(character) -> Deck:
    with open(path.join(CARD_DIR, 'basedecks.json'), 'r', encoding='utf-8') as deck_file:
        data = json.load(deck_file)

    deck = []
    for card in data:
        if card['character'] == character:
            nb = card.pop('nb')
            card.pop('character')
            for i in range(nb):
                deck.append(card)
    deck = Deck(*[Hogwarts(**c) for c in deck])
    deck.shuffle()
    if len(deck) == 10:
        return deck
    else:
        raise ValueError(f"Le deck ne contient pas 10 cartes mais {len(deck)}")


class Recto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((252, 348), SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.logo = pygame.image.load('images/blason.png').convert_alpha()
        self.update()

    def update(self):
        """ FRAME """
        pygame.draw.rect(self.image, (40, 40, 40), (1, 1, self.rect.width - 2, self.rect.height - 2), border_radius=8)
        pygame.draw.rect(self.image, 'grey', (1, 1, self.rect.width - 2, self.rect.height - 2), border_radius=8,
                         width=2)
        logo = pygame.transform.grayscale(self.logo)
        logo = pygame.transform.scale(logo, (200, 200))
        logo.set_alpha(50)
        self.image.blit(logo, ((252-200)/2, (348-200)/2))


if __name__ == '__main__':
    pass