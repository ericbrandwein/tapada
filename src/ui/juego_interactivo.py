import sys
import pygame

from .cartas import card_renderer
from .cartas.carta_ui import CartaUi
from ..juego.mazo.carta import Carta, Palo

from .pilones import PilonesContainer

pygame.init()


class JuegoInteractivo:
    ESPACIO_ENTRE_ESCALERAS_Y_PILONES = 16

    def __init__(self, referi, size=(1000, 700),
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

        # dragging = False
        # while True:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             sys.exit()

        #         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        #             mouse_pos = pygame.mouse.get_pos()
        #             if card_rect.collidepoint(mouse_pos):
        #                 dragging = True

        #         if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        #             dragging = False

        #     if dragging:
        #         card_rect.center = pygame.mouse.get_pos()
        #         screen.fill(background_color)
        #         screen.blit(card_surface, card_rect)
        #         screen.blit(card_back_surface, (width / 2, height / 2))
        #         pygame.display.flip()

    def _render(self):
        """Renderiza todos los elementos de la pantalla necesarios."""
        self._render_background()
        self._render_mazo()
        self._render_pilones()

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
