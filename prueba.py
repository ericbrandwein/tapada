from src.ui.juego_interactivo import JuegoInteractivo

from src.ui.referi import Referi


class ReferiPrueba(Referi):
    def jugador_actual(self):
        return 0


juego = JuegoInteractivo(ReferiPrueba())
juego.empezar()
juego.correr_turno()
