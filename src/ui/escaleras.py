import pygame

from collections.abc import Sequence

pygame.init()


class EscalerasContainer(Sequence):
    ESPACIO_ENTRE_ESCALERAS = 24

    escaleras = []

    def __init__(self, center, card_rect, color_placeholder):
        self.center = center
        self.nueva_escalera_rect = card_rect.copy()
        self.color_placeholder = color_placeholder
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
        surface.fill(self.color_placeholder, self.nueva_escalera_rect)

        for escalera in self.escaleras:
            escalera.render(surface)

    def _actualizar_posiciones(self):
        cant_escaleras = len(self.escaleras)
        if cant_escaleras > 0:
            ancho_escaleras = cant_escaleras * self.nueva_escalera_rect.width \
                + (cant_escaleras - 1) * self.ESPACIO_ENTRE_ESCALERAS
            rect_escaleras = pygame.Rect(
                0, 0, ancho_escaleras, self.nueva_escalera_rect.heigth)
            rect_escaleras.center = self.center

            y = rect_escaleras.y
            x = rect_escaleras.y
            for escalera in self.escaleras:
                escalera.rect.topleft = (x, y)
                x += self.nueva_escalera_rect.width + self.ESPACIO_ENTRE_ESCALERAS

            midleft = rect_escaleras.midright + \
                (self.ESPACIO_ENTRE_ESCALERAS, 0)
            self.nueva_escalera_rect.midleft = midleft
        else:
            self.nueva_escalera_rect.center = self.center
