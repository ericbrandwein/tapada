import pygame

from collections.abc import Sequence
from .cartas import card_renderer

pygame.init()


class PilonUi(Sequence):
    def __init__(self, rect, card_rect, up_orientation=False, padding_entre_cartas=24):
        self.carta_uis = []
        self.rect = rect
        self.card_rect = card_rect
        self.padding_entre_cartas = padding_entre_cartas
        self.up_orientation = up_orientation

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
            if self.up_orientation:
                y = rect_ultimo.y - self.padding_entre_cartas
            else:
                y = rect_ultimo.y + self.padding_entre_cartas
            pos_nueva_carta = (rect_ultimo.x, y)

        carta_ui.rect.topleft = pos_nueva_carta
        self.carta_uis.append(carta_ui)

    def pop(self):
        return self.carta_uis.pop()

    def top(self):
        return self.carta_uis[len(self) - 1]

    def render(self, surface):
        for carta_ui in self.carta_uis:
            carta_ui.render(surface)

    def set_orientation(self, up):
        """Si up es True, la orientación de las cartas será para arriba."""
        if up != self.up_orientation:
            self.up_orientation = up
            self._reorganizar_cartas()

    @property
    def topleft(self):
        return self.rect.topleft

    @topleft.setter
    def topleft(self, point):
        self.rect.topleft = point
        self._reorganizar_cartas()

    def _reorganizar_cartas(self):
        x = self.rect.x
        y = self.rect.y
        for i, carta_ui in enumerate(self.carta_uis):
            if i > 0:
                if self.up_orientation:
                    y -= self.padding_entre_cartas
                else:
                    y += self.padding_entre_cartas
            carta_ui.rect.topleft = (x, y)


class PilonesContainer(Sequence):
    def __init__(self, card_rect, up_orientation=False, cantidad_pilones=3, separacion_entre_pilones=24):
        self.card_rect = card_rect
        self.separacion_entre_pilones = separacion_entre_pilones
        self.up_orientation = up_orientation

        width = card_rect.width * cantidad_pilones + \
            separacion_entre_pilones * (cantidad_pilones - 1)
        self.rect = pygame.Rect(0, 0, width, card_rect.height)

        self.pilones = []
        for i in range(cantidad_pilones):
            pilon_rect = card_rect.copy()
            self.pilones.append(PilonUi(pilon_rect, card_rect, up_orientation))

        self._reorganizar_pilones()

    def __getitem__(self, index):
        return self.pilones[index]

    def __len__(self):
        return len(self.pilones)

    def set_orientation(self, up):
        """Si up es True, la orientación de las cartas será para arriba."""
        if up != self.up_orientation:
            self.up_orientation = up
            self._reorganizar_pilones()

    def render(self, surface):
        for pilon in self.pilones:
            pilon.render(surface)

    @property
    def midtop(self):
        return self.rect.midtop

    @midtop.setter
    def midtop(self, point):
        self.rect.midtop = point
        self._reorganizar_pilones()

    def _reorganizar_pilones(self):
        diferencia_x = self.card_rect.width + self.separacion_entre_pilones
        cantidad_pilones = len(self.pilones)
        for i in range(cantidad_pilones):
            if self.up_orientation:
                x = self.rect.x + (cantidad_pilones - i - 1) * diferencia_x
            else:
                x = self.rect.x + i * diferencia_x

            self.pilones[i].topleft = (x, self.rect.y)
            self.pilones[i].set_orientation(self.up_orientation)
