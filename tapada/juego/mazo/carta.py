from dataclasses import dataclass
from enum import Enum

class Palo(Enum):
    DIAMANTE = 1
    CORAZON = 2
    TREBOL = 3
    PICA = 4

@dataclass
class Carta:
    palo: Palo
    numero: int
    es_joker: bool = False