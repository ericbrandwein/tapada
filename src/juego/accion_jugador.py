from enum import Enum
from dataclasses import dataclass


class Fuente(Enum):
    MANO = 0
    TAPADA = 1
    PILON = 2


class Destino(Enum):
    PILON = 0
    ESCALERA = 1
    TAPADA_CONTRARIA = 2


@dataclass
class AccionJugador:
    fuente: Fuente
    destino: Destino
    indice_fuente: int = 0
    indice_destino: int = 0
