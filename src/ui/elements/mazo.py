class Mazo:
    def __init__(self, rect, card_back_surface):
        self.card_back_surface = card_back_surface
        self.rect = rect

    def render(self, surface):
        surface.blit(self.card_back_surface, self.rect)
