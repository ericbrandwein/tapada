import sys
import pygame

import card_renderer
from juego.mazo.carta import Carta, Palo

pygame.init()


background_color = (70, 112, 65)
size = width, height = 1000, 500
screen = pygame.display.set_mode(size)
screen.fill(background_color)

card_back_surface = card_renderer.render_back()
screen.blit(card_back_surface, (width / 2, height / 2))

carta = Carta(Palo.TREBOL, 13)
card_surface = card_renderer.render(carta)
card_rect = pygame.Rect((10, 10), card_renderer.DIMENSIONES_CARTA)
screen.blit(card_surface, card_rect)

pygame.display.flip()

dragging = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if card_rect.collidepoint(mouse_pos):
                dragging = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False

    if dragging:
        card_rect.center = pygame.mouse.get_pos()
        screen.fill(background_color)
        screen.blit(card_surface, card_rect)
        screen.blit(card_back_surface, (width / 2, height / 2))
        pygame.display.flip()
