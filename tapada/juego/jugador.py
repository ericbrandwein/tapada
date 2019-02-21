from abc import ABC, abstractmethod


class Jugador(ABC):
    @abstractmethod
    def jugar_turno(self, informacionJuego):
        pass
