import pygame

pygame.init()


class LayoutRenderer:
    BACKGROUND_COLOR = pygame.Color(70, 112, 65)
    PLACEHOLDER_COLOR = pygame.Color(120, 162, 115)

    def __init__(self, size, mazo, pilon_containers, escaleras, tapadas, manos):
        self.size = size
        self.mazo = mazo
        self.pilon_containers = pilon_containers
        self.escaleras = escaleras
        self.tapadas = tapadas
        self.manos = manos

        self.screen = pygame.display.set_mode(size)

        self.dragging_card = None
        self.background_surface = None

    def render(self):
        self._render_background()
        self._render_mazo()
        self._render_pilones()
        self._render_escaleras()
        self._render_tapadas()
        self._render_manos()
        self._render_dragging_card()

        pygame.display.flip()

    def mostrar_ganador(self, jugador):
        font_filename = pygame.font.match_font('dejavusans')
        font = pygame.font.Font(font_filename, 28)
        texto = 'Ganó el jugador {}!'.format(jugador + 1)
        texto_render = font.render(texto, True, (0, 0, 0))
        self.screen.blit(texto_render, (self.size[0] / 2, self.size[1] / 2))

        pygame.display.flip()

    def _render_background(self):
        if not self.background_surface:
            self.background_surface = pygame.Surface(self.size)
            self.background_surface.fill(self.BACKGROUND_COLOR)

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
        self.escaleras.render(self.screen)

    def _render_tapadas(self):
        for tapada in self.tapadas:
            tapada.render(self.screen)

    def _render_dragging_card(self):
        if self.dragging_card:
            self.dragging_card.render(self.screen)

    def _render_manos(self):
        for mano in self.manos:
            mano.render(self.screen)

    def _render_placeholder_rect(self, surface, rect):
        surface.fill(self.PLACEHOLDER_COLOR, rect)
