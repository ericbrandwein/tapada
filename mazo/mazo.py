from random import shuffle
from carta import Palo, Carta


class Mazo:
    def __init__(self, cartas):
        self.cartas = cartas
        self.mezclado = False

    def vacio(self):
        return len(self.cartas) > 0

    def sacar_carta(self):
        """
        Saca la carta de arriba de todo del mazo.

        El mazo no debe estar vacio.
        """
        if not self.mezclado:
            self._mezclar()
        return self.cartas.pop(0)

    def _mezclar(self):
        shuffle(self.cartas)
        self.mezclado = True


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
