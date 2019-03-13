import pygame

from collections.abc import Sequence

pygame.init()


class Mano(Sequence):
    ANCHO_MANO = 5*42

    def __init__(self, dimensiones_carta):
        self.dimensiones_carta = self.ancho_carta, self.alto_carta = dimensiones_carta
        self.rect = pygame.Rect(0, 0, self.ANCHO_MANO, self.alto_carta)
        self.cartas = []
        self.posicion = (0, 0)

    def __len__(self):
        return len(self.cartas)

    def __getitem__(self, index):
        return self.cartas[index]

    def agregar_cartas(self, cartas_ui):
        self.cartas += cartas_ui

    def sacar_carta(self, index):
        return self.cartas.pop(index)

    def render(self, surface):
        self._posicionar_cartas()
        for carta in self.cartas:
            carta.render(surface)

    def _posicionar_cartas(self):
        if len(self.cartas) > 1:
            padding_cartas = \
                (self.ANCHO_MANO - self.ancho_carta) / (len(self.cartas) - 1)
            for indice, carta in enumerate(self.cartas):
                carta.rect.y = self.rect.y
                carta.rect.x = self.rect.x + padding_cartas * indice
        elif len(self.cartas) == 1:
            carta = self.cartas[0]
            carta.rect.center = self.rect.center
