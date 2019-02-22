import pygame

from collections.abc import Sequence

pygame.init()


class EscalerasContainer(Sequence):
    ESPACIO_ENTRE_ESCALERAS = 24

    escaleras = []

    def __init__(self, center, card_rect, color_placeholder, color_plus):
        self.center = center
        self.nueva_escalera_rect = card_rect.copy()

        self._draw_nueva_escalera_rect(
            card_rect.size, color_placeholder, color_plus)

        self._actualizar_posiciones()

    def __getitem__(self, index):
        return self.escaleras[index]

    def __len__(self):
        return len(self.escaleras)

    def agregar_escalera(self, carta_ui):
        self.escaleras.append(carta_ui)
        self._actualizar_posiciones()

    def agregar_carta(self, indice_escalera, carta_ui):
        self.escaleras[indice_escalera] = carta_ui
        self._actualizar_posiciones()

    def render(self, surface):
        surface.blit(self.nueva_escalera_surface, self.nueva_escalera_rect)

        for escalera in self.escaleras:
            escalera.render(surface)

    def _draw_nueva_escalera_rect(self, size, color_placeholder, color_plus):
        self.nueva_escalera_surface = pygame.Surface(size)
        self.nueva_escalera_surface.fill(color_placeholder)
        plus_rect = pygame.Rect(0, 0, 32, 8)
        plus_rect.center = (
            self.nueva_escalera_surface.get_width() / 2,
            self.nueva_escalera_surface.get_height() / 2,
        )
        self.nueva_escalera_surface.fill(color_plus, plus_rect)
        plus_rect = pygame.Rect(0, 0, 8, 32)
        plus_rect.center = (
            self.nueva_escalera_surface.get_width() / 2,
            self.nueva_escalera_surface.get_height() / 2,
        )
        self.nueva_escalera_surface.fill(color_plus, plus_rect)

    def _actualizar_posiciones(self):
        cant_escaleras = len(self.escaleras)
        if cant_escaleras > 0:
            ancho_escaleras = cant_escaleras * self.nueva_escalera_rect.width \
                + (cant_escaleras - 1) * self.ESPACIO_ENTRE_ESCALERAS
            rect_escaleras = pygame.Rect(
                0, 0, ancho_escaleras, self.nueva_escalera_rect.height)
            rect_escaleras.center = self.center

            y = rect_escaleras.y
            x = rect_escaleras.x
            for escalera in self.escaleras:
                escalera.rect.topleft = (x, y)
                x += self.nueva_escalera_rect.width + self.ESPACIO_ENTRE_ESCALERAS

            midleft = (
                rect_escaleras.midright[0] + self.ESPACIO_ENTRE_ESCALERAS,
                rect_escaleras.midright[1]
            )
            self.nueva_escalera_rect.midleft = midleft
        else:
            self.nueva_escalera_rect.center = self.center
