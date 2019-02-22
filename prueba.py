from src.ui.juego_interactivo import JuegoInteractivo

from src.ui.referi import Referi


class ReferiPrueba(Referi):
    def jugador_actual(self):
        return 0


JuegoInteractivo(ReferiPrueba()).empezar()

while True:
    pass
