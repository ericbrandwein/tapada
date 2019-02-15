from random import shuffle
from carta import Palo, Carta


class Mazo:
    def __init__(self, cartas):
        self.cartas = cartas
        shuffle(self.cartas)
        self.cartas_nuevas = []

    def __len__(self):
        return self.restantes()

    def restantes(self):
        return len(self.cartas) + len(self.cartas_nuevas)

    def sacar_cartas(self, cantidad):
        """
        Saca ```cantidad``` cartas de arriba de todo del mazo.

        La cantidad de cartas pedidas debe ser menor o igual a las restantes.
        """
        if self.restantes() < cantidad:
            raise ValueError("El mazo no tiene suficientes cartas.")

        cartas_sacadas = []
        if len(self.cartas) < cantidad:
            cartas_sacadas = self.cartas
            self.cartas = self.cartas_nuevas
            shuffle(self.cartas)
            self.cartas_nuevas = []

        cartas_sacadas.extend(self.cartas[-cantidad:])
        self.cartas = self.cartas[:-cantidad]

        return cartas_sacadas

    def agregar_cartas(self, cartas):
        self.cartas_nuevas.extend(cartas)


class MazoInicial(Mazo):
    def __init__(self):
        cartas_iniciales = []
        for copias in range(2):
            for palo in Palo:
                for numero_carta in range(1, 14):
                    cartas_iniciales.append(Carta(palo, numero_carta))

            for num_joker in range(2):
                cartas_iniciales.append(Carta(None, None, True))

        super(cartas_iniciales)
