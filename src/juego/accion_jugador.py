from enum import Enum


class Fuente(Enum):
    MANO = 0
    TAPADA = 1
    PILON = 2


class Destino(Enum):
    PILON = 0
    ESCALERA = 1
    TAPADA_CONTRARIA = 2


class AccionJugador:
    def __init__(self, fuente, destino, indice_fuente=0, indice_destino=0):
        """
        Si el destino es ESCALERA y el indice_destino es < 0, se crea una nueva.
        """
        self.fuente = fuente
        self.destino = destino
        self.indice_fuente = indice_fuente
        self.indice_destino = indice_destino
