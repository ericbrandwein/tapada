from src.ui.juego_interactivo import JuegoInteractivo

from src.ui.referi import Referi
from src.juego.mazo.carta import Carta, Palo


class ReferiPrueba(Referi):
    def jugador_actual(self):
        return 0

    def ejecutar_jugada(self, accion_jugador):
        """Ejecuta la jugada y devuelve True si es válida, y False sino."""
        return True

    def cartas_destapadas(self, indice_jugador):
        if indice_jugador == 1:
            return [Carta(Palo.DIAMANTE, 12)]
        else:
            return [Carta(Palo.TREBOL, 2)]

    def cartas_tapadas(self, indice_jugador):
        if indice_jugador == 1:
            return [Carta(Palo.DIAMANTE, 12) for i in range(9)]
        else:
            return [Carta(Palo.TREBOL, 2) for i in range(9)]


juego = JuegoInteractivo(ReferiPrueba())
juego.empezar()
juego.correr_turno()
