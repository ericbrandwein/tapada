import pygame

from ...juego.mazo.carta import Palo

pygame.init()

COLOR_CARTA = (255, 255, 255)
COLOR_ROJO = (255, 0, 0)
COLOR_NEGRO = (0, 0, 0)
COLOR_CARTA_BACK = (72, 107, 165)

font_filename = pygame.font.match_font('dejavusans')
FONT_CARTA = pygame.font.Font(font_filename, 14)


class RenderizadorConPalo:
    def __init__(self, simbolo_palo, color):
        self.simbolo_palo = simbolo_palo
        self.color = color

    def render(self, numero, dimensiones):
        card_surface = pygame.Surface(dimensiones)
        card_surface.fill(COLOR_CARTA)

        texto = '{} {}'.format(numero, self.simbolo_palo)
        card_text = FONT_CARTA.render(texto, True, self.color)
        card_surface.blit(card_text, (4, 4))
        return card_surface


RENDERIZADORES = {
    Palo.DIAMANTE: RenderizadorConPalo('♦', COLOR_ROJO),
    Palo.CORAZON: RenderizadorConPalo('♥', COLOR_ROJO),
    Palo.TREBOL: RenderizadorConPalo('♣', COLOR_NEGRO),
    Palo.PICA: RenderizadorConPalo('♠', COLOR_NEGRO),
}


def render(carta, dimensiones):
    return RENDERIZADORES[carta.palo].render(carta.numero, dimensiones)


def render_back(dimensiones):
    """Renderiza una Surface con la parte trasera de una carta."""
    card_surface = pygame.Surface(dimensiones)
    card_surface.fill(COLOR_CARTA)

    padding = 5
    min_x = padding
    max_x = dimensiones[0] - padding - 1
    min_y = padding
    max_y = dimensiones[1] - padding - 1

    back_center_rect = pygame.rect.Rect(
        min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)
    card_surface.fill(COLOR_CARTA_BACK, back_center_rect)

    # Lineas verticales
    usar_color_negro = True
    for x in range(min_x + padding, max_x, padding):
        if usar_color_negro:
            color = COLOR_NEGRO
        else:
            color = COLOR_ROJO
        usar_color_negro = not usar_color_negro
        pygame.draw.line(card_surface, color, (x, min_y),
                         (x, max_y))

    # Lineas horizontales
    for y in range(min_y + padding, max_y, padding):
        if usar_color_negro:
            color = COLOR_NEGRO
        else:
            color = COLOR_ROJO
        usar_color_negro = not usar_color_negro
        pygame.draw.line(card_surface, color,
                         (min_x, y), (max_x, y))

    return card_surface
