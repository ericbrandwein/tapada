from src.ui.pilones import PilonUi


class TapadaUi:
    def __init__(self, rect, card_rect, card_back_surface, cartas_tapadas=[], cartas_destapadas=[],
                 up_orientation=False, padding_entre_tapadas_y_destapadas=8):
        self.pilon = PilonUi(rect.copy(), card_rect, up_orientation)
        self.rect = rect
        self.card_back_surface = card_back_surface
        self.cartas_tapadas = cartas_tapadas
        self.up_orientation = up_orientation
        self.padding_entre_tapadas_y_destapadas = padding_entre_tapadas_y_destapadas

        for carta in cartas_destapadas:
            self.pilon.agregar_carta(carta)

    def __len__(self):
        return len(self.cartas_tapadas) + len(self.pilon)

    def agregar_carta(self, carta_ui):
        self.pilon.agregar_carta(carta_ui)

    def sacar_carta(self):
        carta_sacada = self.pilon.pop()
        if not self.pilon and self.cartas_tapadas:
            nueva_carta = self.cartas_tapadas.pop()
            self.pilon.agregar_carta(nueva_carta)
        return carta_sacada

    def set_orientation(self, up):
        if self.up_orientation != up:
            self.up_orientation = up
            self.pilon.set_orientation(up)

    def render(self, surface):
        pilon_y = self.rect.y
        if self.cartas_tapadas:
            surface.blit(self.card_back_surface, self.rect)
            if self.up_orientation:
                pilon_y -= self.padding_entre_tapadas_y_destapadas
            else:
                pilon_y += self.padding_entre_tapadas_y_destapadas
        self.pilon.y = pilon_y
        self.pilon.render(surface)

    def check_collision(self, point):
        return self.pilon and self.pilon.check_collision(point)
