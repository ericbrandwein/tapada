from abc import ABC, abstractmethod


class Referi(ABC):
    @abstractmethod
    def jugador_actual(self):
        pass

    def jugador_contrario(self):
        return (self.jugador_actual() + 1) % 2
