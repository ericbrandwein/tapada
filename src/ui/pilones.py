import pygame

from collections.abc import Sequence
from .cartas import card_renderer

pygame.init()


class PilonUi(Sequence):
    def __init__(self, rect, card_rect, padding_entre_cartas=24):
        self.carta_uis = []
        self.rect = rect
        self.card_rect = card_rect
        self.padding_entre_cartas = padding_entre_cartas

    def __getitem__(self, index):
        return self.carta_uis[index]

    def __len__(self):
        return len(self.carta_uis)

    def agregar_carta(self, carta_ui):
        """Agrega la carta al pilon y la posiciona en su lugar."""
        if len(self.carta_uis) == 0:
            pos_nueva_carta = self.rect.topleft
        else:
            rect_ultimo = self.top().rect
            pos_nueva_carta = (rect_ultimo.x, rect_ultimo.y +
                               self.padding_entre_cartas)

        carta_ui.rect.topleft = pos_nueva_carta
        self.carta_uis.append(carta_ui)

    def pop(self):
        return self.carta_uis.pop()

    def top(self):
        return self.carta_uis[len(self) - 1]

    @property
    def midtop(self):
        return self.rect.midtop

    @midtop.setter
    def midtop(self, point):
        self.rect.midtop = point
        for i, carta_ui in enumerate(self.carta_uis):
            carta_point = (point[0], point[1] + self.padding_entre_cartas * i)
            carta_ui.rect.midtop = carta_point


class PilonesContainer(Sequence):
    def __init__(self, card_rect, cantidad_pilones=3, separacion_entre_pilones=24):
        self.card_rect = card_rect
        self.separacion_entre_pilones = separacion_entre_pilones
        self.width = card_rect.width * cantidad_pilones + \
            separacion_entre_pilones * (cantidad_pilones - 1)

        self.pilones = []
        for i in range(cantidad_pilones):
            pilon_rect = card_rect.copy()
            pilon_rect.y = 0
            pilon_rect.x = i * (card_rect.width + separacion_entre_pilones)
            self.pilones.append(PilonUi(pilon_rect, card_rect))

    def __getitem__(self, index):
        return self.pilones[index]

    def __len__(self):
        return len(self.pilones)

    @property
    def midtop(self):
        cantidad_pilones = len(self.pilones)
        indice_medio = cantidad_pilones // 2
        return self.pilones[indice_medio].rect.midtop

    @midtop.setter
    def midtop(self, point):
        cantidad_pilones = len(self.pilones)
        indice_medio = cantidad_pilones // 2
        self.pilones[indice_medio].rect.midtop = point
        for i in range(cantidad_pilones):
            if i != indice_medio:
                y = point[1]
                x = point[0] + (i - indice_medio) * \
                    (self.card_rect.width + self.separacion_entre_pilones)
                self.pilones[i].midtop = x, y
