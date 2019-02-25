import pygame

from . import card_renderer
pygame.init()


class CartaUi:
    def __init__(self, carta, rect=None):
        self.carta = carta
        if not rect:
            self.dimensiones = 70, 100
            self.rect = pygame.Rect((0, 0), self.dimensiones)
        else:
            self.dimensiones = rect.size
            self.rect = rect

        self.surface = card_renderer.render(carta, self.dimensiones)

    def render(self, surface):
        surface.blit(self.surface, self.rect)

    def check_collision(self, point):
        return self.rect.collidepoint(point)
