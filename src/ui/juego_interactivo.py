import sys
import pygame

from .cartas import card_renderer
from .cartas.carta_ui import CartaUi
from ..juego.mazo.carta import Carta, Palo

from .pilones import PilonesContainer

pygame.init()


class JuegoInteractivo:
    ESPACIO_ENTRE_ESCALERAS_Y_PILONES = 16

    def __init__(self, referi, size=(1366, 768),
                 background_color=pygame.Color(70, 112, 65), card_size=(70, 100)):
        self.referi = referi
        self.size = self.width, self.height = size
        self.background_color = background_color

        self.card_rect = pygame.Rect((0, 0), card_size)
        self.card_back_surface = card_renderer.render_back(card_size)

        self.mazo_rect = self.card_rect.copy()
        ancho_carta = card_size[0]
        self.mazo_rect.center = ancho_carta / 2 + 16, self.height / 2

        self.background_surface = None

        self.pilon_containers = [
            PilonesContainer(self.card_rect),
            PilonesContainer(self.card_rect, up_orientation=True)
        ]

        self._posicionar_pilones()

        self.dragging_card = None

    def _posicionar_pilones(self):
        card_height = self.card_rect.h
        midtop_pilones_arriba = (self.width / 2, self.height / 2 -
                                 card_height * 1.5 - self.ESPACIO_ENTRE_ESCALERAS_Y_PILONES)
        midtop_pilones_abajo = (self.width / 2, self.height / 2 +
                                card_height * 0.5 + self.ESPACIO_ENTRE_ESCALERAS_Y_PILONES)

        jugador_actual = self.referi.jugador_actual()
        jugador_contrario = self.referi.jugador_contrario()

        self.pilon_containers[jugador_contrario].midtop = midtop_pilones_arriba
        self.pilon_containers[jugador_actual].midtop = midtop_pilones_abajo

    def empezar(self):
        self.screen = pygame.display.set_mode(self.size)

        carta = Carta(Palo.DIAMANTE, 12)
        for i in range(12):
            carta_ui = CartaUi(carta)
            self.pilon_containers[0][0].agregar_carta(carta_ui)
        carta = Carta(Palo.TREBOL, 1)
        carta_ui = CartaUi(carta)
        self.pilon_containers[0][0].agregar_carta(carta_ui)
        carta_ui = CartaUi(carta)
        self.pilon_containers[1][0].agregar_carta(carta_ui)
        carta_ui = CartaUi(carta)
        self.pilon_containers[1][0].agregar_carta(carta_ui)

        self._render()

    def correr_turno(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    self.dragging_card = self._drag_card_under(mouse_pos)

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.dragging_card = None

            if self.dragging_card:
                self.dragging_card.rect.center = pygame.mouse.get_pos()
                self._render()

    def _render(self):
        """Renderiza todos los elementos de la pantalla necesarios."""
        self._render_background()
        self._render_mazo()
        self._render_pilones()
        self._render_dragging_card()

        pygame.display.flip()

    def _render_background(self):
        if not self.background_surface:
            background_surface = pygame.Surface(self.size)
            background_surface.fill(self.background_color)

            color_pilones = self.background_color + pygame.Color(50, 50, 50)
            for container in self.pilon_containers:
                for pilon in container:
                    background_surface.fill(color_pilones, pilon.rect)

            self.background_surface = background_surface

        self.screen.blit(self.background_surface, (0, 0))

    def _render_mazo(self):
        self.screen.blit(self.card_back_surface, self.mazo_rect)

    def _render_pilones(self):
        for container in self.pilon_containers:
            container.render(self.screen)

    def _render_dragging_card(self):
        if self.dragging_card:
            self.dragging_card.render(self.screen)

    def _drag_card_under(self, position):
        jugador_actual = self.referi.jugador_actual()
        for pilon in self.pilon_containers[jugador_actual]:
            if pilon:
                card_rect = pilon.top().rect
                if card_rect.collidepoint(position):
                    return pilon.pop()

        return None
