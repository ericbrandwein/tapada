from enum import Enum

class Palo(Enum):
    DIAMANTE = 1
    CORAZON = 2
    TREBOL = 3
    PICA = 4

class Carta:
    def __init__(self, palo, numero):
        self.palo = palo
        self.numero = numero