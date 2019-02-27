from abc import ABC, abstractmethod


class Referi(ABC):
    @abstractmethod
    def jugador_actual(self):
        pass

    @abstractmethod
    def ejecutar_jugada(self, accion_jugador):
        """Ejecuta la jugada y devuelve True si es válida, y False sino."""
        pass

    @abstractmethod
    def cartas_tapadas(self, indice_jugador):
        pass

    @abstractmethod
    def cartas_destapadas(self, indice_jugador):
        pass

    def jugador_contrario(self):
        return (self.jugador_actual() + 1) % 2
