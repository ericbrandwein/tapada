from abc import ABC, abstractmethod


class Referi(ABC):
    @abstractmethod
    def puede_ejecutar_jugada(self, accion_jugador):
        """Determina si la accion_jugador es válida."""
        pass

    @abstractmethod
    def cartas_tapadas(self, indice_jugador):
        pass

    @abstractmethod
    def cartas_destapadas(self, indice_jugador):
        pass
