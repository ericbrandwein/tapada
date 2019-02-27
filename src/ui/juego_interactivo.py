import sys

import pygame

from ..juego.accion_jugador import AccionJugador, Destino, Fuente
from ..juego.mazo.carta import Carta, Palo
from .elements.escaleras import EscalerasContainer
from .elements.pilones import PilonesContainer
from .elements.tapadas import TapadaUi
from .elements.mazo import Mazo
from .cartas import card_renderer
from .cartas.carta_ui import CartaUi
from ..utils.tapada_utils import jugador_contrario
from .layout_designer import LayoutDesigner

pygame.init()


class JuegoInteractivo:
    background_surface = None
    dragging_card = None
    dragging_card_origin = None
    dragging_card_origin_index = None
    jugador_actual = -1

    def __init__(self, referi, size=(1366, 768),
                 background_color=pygame.Color(70, 112, 65), card_size=(70, 100)):
        self.referi = referi
        self.size = self.width, self.height = size
        self.background_color = background_color
        self.color_placeholder = self.background_color + \
            pygame.Color(50, 50, 50)

        self.card_rect = pygame.Rect((0, 0), card_size)
        self.card_back_surface = card_renderer.render_back(card_size)

        self.mazo = self._init_mazo()
        self.pilon_containers = self._init_pilones()
        self.escaleras_container = self._init_escaleras()
        self.tapadas = self._init_tapadas()

        self.layout_designer = LayoutDesigner(
            size, card_size, self.mazo, self.escaleras_container,
            self.pilon_containers, self.tapadas)

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

    def correr_turno(self, jugador_actual):
        if self.jugador_actual != jugador_actual:
            self.jugador_actual = jugador_actual
            self.layout_designer.design(jugador_actual)
            should_render = True
        else:
            should_render = False
        accion_jugador = None
        while not accion_jugador:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    self._drag_card_under(mouse_pos)

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_pos = event.pos
                    if self.dragging_card:
                        accion_jugador = self._release_card(mouse_pos)
                        should_render = True

            if self.dragging_card:
                self.dragging_card.rect.center = pygame.mouse.get_pos()
                should_render = True

            if should_render:
                self._render()
                should_render = False

        return accion_jugador

    def _init_mazo(self):
        mazo_rect = self.card_rect.copy()
        return Mazo(mazo_rect, self.card_back_surface)

    def _init_pilones(self):
        return [
            PilonesContainer(self.card_rect) for i in range(2)
        ]

    def _init_escaleras(self):
        return EscalerasContainer(
            self.card_rect, self.color_placeholder,
            self.background_color)

    def _init_tapadas(self):
        tapadas = []
        for jugador in range(2):
            tapada_rect = self.card_rect.copy()
            cartas_tapadas = self.referi.cartas_tapadas(jugador)
            cartas_ui_tapadas = self._cartas_a_cartas_ui(cartas_tapadas)
            cartas_destapadas = self.referi.cartas_destapadas(jugador)
            cartas_ui_destapadas = self._cartas_a_cartas_ui(cartas_destapadas)
            tapada = TapadaUi(tapada_rect, self.card_rect,
                              self.card_back_surface, cartas_ui_tapadas, cartas_ui_destapadas)
            tapadas.append(tapada)

        return tapadas

    def _cartas_a_cartas_ui(self, cartas):
        return [
            CartaUi(carta) for carta in cartas
        ]

    def _render(self):
        """Renderiza todos los elementos de la pantalla necesarios."""
        self._render_background()
        self._render_mazo()
        self._render_pilones()
        self._render_escaleras()
        self._render_tapadas()
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
        self.mazo.render(self.screen)

    def _render_pilones(self):
        for container in self.pilon_containers:
            container.render(self.screen)

    def _render_escaleras(self):
        self.escaleras_container.render(self.screen)

    def _render_tapadas(self):
        for tapada in self.tapadas:
            tapada.render(self.screen)

    def _render_dragging_card(self):
        if self.dragging_card:
            self.dragging_card.render(self.screen)

    def _render_placeholder_rect(self, surface, rect):
        surface.fill(self.color_placeholder, rect)

    def _drag_card_under(self, position):
        indice_pilon_colisionado = self._check_pilones_collision(position)
        if indice_pilon_colisionado >= 0:
            pilon_container = self.pilon_containers[self.jugador_actual]
            pilon_colisionado = pilon_container[indice_pilon_colisionado]
            if len(pilon_colisionado) > 0:
                self.dragging_card_origin = Fuente.PILON
                self.dragging_card_origin_index = indice_pilon_colisionado
                self.dragging_card = pilon_colisionado.pop()
        else:
            tapada = self.tapadas[self.jugador_actual]
            if tapada.check_collision(position):
                self.dragging_card_origin = Fuente.TAPADA
                self.dragging_card = tapada.sacar_carta()

    def _release_card(self, position):
        destino = self._get_card_destination(position)
        destino_valido = False
        if destino:
            tipo_destino = destino[0]
            indice_destino = destino[1]

            accion_jugador = AccionJugador(
                self.dragging_card_origin, self.dragging_card_origin_index,
                tipo_destino, indice_destino
            )
            destino_valido = self.referi.puede_ejecutar_jugada(accion_jugador)

        if destino_valido:
            self._place_dragging_card(tipo_destino, indice_destino)
            if self.dragging_card_origin == Fuente.TAPADA:
                self.tapadas[self.jugador_actual].revelar_siguiente()
        else:
            self._return_dragging_card()
            accion_jugador = None

        self.dragging_card = None
        self.dragging_card_origin = None
        self.dragging_card_origin_index = None

        return accion_jugador

    def _place_dragging_card(self, tipo_destino, indice_destino):
        if tipo_destino == Destino.PILON:
            pilon_destino = self.pilon_containers[self.jugador_actual][indice_destino]
            pilon_destino.agregar_carta(self.dragging_card)
        elif tipo_destino == Destino.ESCALERA:
            if indice_destino == EscalerasContainer.NUEVA_ESCALERA_INDEX:
                self.escaleras_container.agregar_escalera(
                    self.dragging_card)
            else:
                self.escaleras_container.agregar_carta(
                    indice_destino, self.dragging_card)

    def _return_dragging_card(self):
        if self.dragging_card_origin == Fuente.PILON:
            pilon_container = self.pilon_containers[self.jugador_actual]
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
        return self.pilon_containers[self.jugador_actual].check_collision(position)

    def _jugador_contrario(self):
        return (self.jugador_actual + 1) % 2
