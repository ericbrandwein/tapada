import sys

import pygame

from src.ui.escaleras import EscalerasContainer

from ..juego.accion_jugador import AccionJugador, Destino, Fuente
from ..juego.mazo.carta import Carta, Palo
from .cartas import card_renderer
from .cartas.carta_ui import CartaUi
from .pilones import PilonesContainer

pygame.init()


class JuegoInteractivo:
    ESPACIO_ENTRE_ESCALERAS_Y_PILONES = 48

    background_surface = None
    dragging_card = None
    dragging_card_origin = None
    dragging_card_origin_index = None

    def __init__(self, referi, size=(1366, 768),
                 background_color=pygame.Color(70, 112, 65), card_size=(70, 100)):
        self.referi = referi
        self.size = self.width, self.height = size
        self.background_color = background_color
        self.color_placeholder = self.background_color + \
            pygame.Color(50, 50, 50)

        self.card_rect = pygame.Rect((0, 0), card_size)
        self.card_back_surface = card_renderer.render_back(card_size)

        self._init_mazo()
        self._init_pilones()
        self._init_escaleras()

    def empezar(self):
        self.screen = pygame.display.set_mode(self.size)

        carta = Carta(Palo.DIAMANTE, 12)
        for i in range(6):
            carta_ui = CartaUi(carta)
            self.pilon_containers[0][0].agregar_carta(carta_ui)
        carta = Carta(Palo.TREBOL, 1)
        carta_ui = CartaUi(carta)
        self.pilon_containers[0][0].agregar_carta(carta_ui)
        carta_ui = CartaUi(carta)
        self.pilon_containers[1][0].agregar_carta(carta_ui)
        carta_ui = CartaUi(carta)
        self.pilon_containers[1][0].agregar_carta(carta_ui)

        carta_ui = CartaUi(carta)
        self.escaleras_container.agregar_escalera(carta_ui)

        carta_ui = CartaUi(carta)
        self.escaleras_container.agregar_escalera(carta_ui)

        self._render()

    def correr_turno(self):
        while True:
            should_render = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    self._drag_card_under(mouse_pos)

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_pos = event.pos
                    if self.dragging_card:
                        self._release_card(mouse_pos)
                        should_render = True

            if self.dragging_card:
                self.dragging_card.rect.center = pygame.mouse.get_pos()
                should_render = True

            if should_render:
                self._render()

    def _init_mazo(self):
        self.mazo_rect = self.card_rect.copy()
        ancho_carta = self.card_rect.width
        self.mazo_rect.center = ancho_carta / 2 + 16, self.height / 2

    def _init_pilones(self):
        self.pilon_containers = [
            PilonesContainer(self.card_rect),
            PilonesContainer(self.card_rect, up_orientation=True)
        ]
        self._posicionar_pilones()

    def _init_escaleras(self):
        center = (self.width / 2, self.height / 2)
        self.escaleras_container = EscalerasContainer(
            center, self.card_rect,
            self.color_placeholder, self.background_color)

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

    def _render(self):
        """Renderiza todos los elementos de la pantalla necesarios."""
        self._render_background()
        self._render_mazo()
        self._render_pilones()
        self._render_escaleras()
        self._render_dragging_card()

        pygame.display.flip()

    def _render_background(self):
        if not self.background_surface:
            self.background_surface = pygame.Surface(self.size)
            self.background_surface.fill(self.background_color)

            for container in self.pilon_containers:
                for pilon in container:
                    self._render_placeholder_rect(
                        self.background_surface, pilon.rect)

        self.screen.blit(self.background_surface, (0, 0))

    def _render_mazo(self):
        self.screen.blit(self.card_back_surface, self.mazo_rect)

    def _render_pilones(self):
        for container in self.pilon_containers:
            container.render(self.screen)

    def _render_escaleras(self):
        self.escaleras_container.render(self.screen)

    def _render_dragging_card(self):
        if self.dragging_card:
            self.dragging_card.render(self.screen)

    def _render_placeholder_rect(self, surface, rect):
        surface.fill(self.color_placeholder, rect)

    def _drag_card_under(self, position):
        pilon_colisionado = self._check_pilones_collision(position)
        if pilon_colisionado >= 0:
            self.dragging_card_origin = Fuente.PILON
            self.dragging_card_origin_index = pilon_colisionado
            jugador_actual = self.referi.jugador_actual()
            pilon_container = self.pilon_containers[jugador_actual]
            self.dragging_card = pilon_container[pilon_colisionado].pop()

    def _release_card(self, position):
        destino = self._get_card_destination(position)

        if destino:
            tipo_destino = destino[0]
            indice_destino = destino[1]

            accion_jugador = AccionJugador(
                self.dragging_card_origin, self.dragging_card_origin_index,
                tipo_destino, indice_destino
            )
            if self.referi.ejecutar_jugada(accion_jugador):
                self._place_dragging_card(tipo_destino, indice_destino)
            else:
                self._return_dragging_card()
        else:
            self._return_dragging_card()

        self.dragging_card = None
        self.dragging_card_origin = None
        self.dragging_card_origin_index = None

    def _place_dragging_card(self, tipo_destino, indice_destino):
        jugador_actual = self.referi.jugador_actual()
        if tipo_destino == Destino.PILON:
            pilon_destino = self.pilon_containers[jugador_actual][indice_destino]
            pilon_destino.agregar_carta(self.dragging_card)
        elif tipo_destino == Destino.ESCALERA:
            if indice_destino == EscalerasContainer.NUEVA_ESCALERA_INDEX:
                self.escaleras_container.agregar_escalera(
                    self.dragging_card)
            else:
                self.escaleras_container.agregar_carta(
                    indice_destino, self.dragging_card)

    def _return_dragging_card(self):
        jugador_actual = self.referi.jugador_actual()
        if self.dragging_card_origin == Fuente.PILON:
            pilon_container = self.pilon_containers[jugador_actual]
            pilon = pilon_container[self.dragging_card_origin_index]
            pilon.agregar_carta(self.dragging_card)

    def _get_card_destination(self, position):
        pilon_colisionado = self._check_pilones_collision(position)
        if pilon_colisionado >= 0:
            return Destino.PILON, pilon_colisionado

        escalera_colisionada = self.escaleras_container.check_collision(
            position)
        if escalera_colisionada != EscalerasContainer.NO_COLLISION:
            return Destino.ESCALERA, escalera_colisionada

        return None

    def _check_pilones_collision(self, position):
        jugador_actual = self.referi.jugador_actual()
        return self.pilon_containers[jugador_actual].check_collision(position)
