from src.ui.juego_interactivo import JuegoInteractivo

from src.ui.referi import Referi
from src.juego.mazo.carta import Carta, Palo


class ReferiPrueba(Referi):
    def puede_ejecutar_jugada(self, accion_jugador):
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
jugador = 0
while True:
    juego.correr_turno(jugador)
    jugador = (jugador + 1) % 2
