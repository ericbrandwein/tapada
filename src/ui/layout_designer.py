from ..utils import tapada_utils


class LayoutDesigner:
    ESPACIO_ENTRE_ESCALERAS_Y_PILONES = 48
    ESPACIO_ENTRE_PILONES_Y_TAPADA = 48

    def __init__(self, dimensiones, dimensiones_carta, mazo, escaleras_container,
                 pilones_containers, tapadas):
        self.dimensiones = self.ancho, self.alto = dimensiones
        self.ancho_carta, self.alto_carta = dimensiones_carta
        self.mazo = mazo
        self.escaleras_container = escaleras_container
        self.pilones_containers = pilones_containers
        self.tapadas = tapadas

    def design(self, jugador_actual):
        self._posicionar_mazo()
        self._posicionar_escaleras()
        self._posicionar_pilones(jugador_actual)
        self._posicionar_tapadas(jugador_actual)

    def _posicionar_mazo(self):
        ancho_mazo = self.mazo.rect.width
        self.mazo.rect.center = ancho_mazo / 2 + 16, self.alto / 2

    def _posicionar_escaleras(self):
        self.escaleras_container.set_center((self.ancho / 2, self.alto / 2))

    def _posicionar_pilones(self, jugador_actual):
        midtop_pilones_arriba = (self.ancho / 2, self.alto / 2 -
                                 self.alto_carta * 1.5 - self.ESPACIO_ENTRE_ESCALERAS_Y_PILONES)
        midtop_pilones_abajo = (self.ancho / 2, self.alto / 2 +
                                self.alto_carta * 0.5 + self.ESPACIO_ENTRE_ESCALERAS_Y_PILONES)

        container_abajo = self.pilones_containers[jugador_actual]
        container_abajo.midtop = midtop_pilones_abajo
        container_abajo.set_orientation(False)

        jugador_contrario = tapada_utils.jugador_contrario(jugador_actual)
        container_arriba = self.pilones_containers[jugador_contrario]
        container_arriba.midtop = midtop_pilones_arriba
        container_arriba.set_orientation(True)

    def _posicionar_tapadas(self, jugador_actual):
        for jugador in range(2):
            tapada = self.tapadas[jugador]
            pilones = self.pilones_containers[jugador]
            tapada.rect.left = pilones.rect.right + self.ESPACIO_ENTRE_PILONES_Y_TAPADA
            tapada.rect.y = pilones.rect.y
            up_orientation = jugador != jugador_actual
            tapada.set_orientation(up_orientation)
