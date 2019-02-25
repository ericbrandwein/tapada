from src.ui.juego_interactivo import JuegoInteractivo

from src.ui.referi import Referi


class ReferiPrueba(Referi):
    def jugador_actual(self):
        return 0

    def ejecutar_jugada(self, accion_jugador):
        """Ejecuta la jugada y devuelve True si es válida, y False sino."""
        return True


juego = JuegoInteractivo(ReferiPrueba())
juego.empezar()
juego.correr_turno()
