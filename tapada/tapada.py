class Tapada:
    """Pilón de cartas tapadas."""

    def __init__(self, cartas):
        self.cartas_cubiertas = cartas[:-1]
        self.cartas_descubiertas = [cartas[-1]]

    def __len__(self):
        return len(self.cartas_cubiertas) + len(self.cartas_descubiertas)

    def pop(self):
        if len(self) == 0:
            raise ValueError("La tapada está vacía")

        carta_sacada = self.cartas_descubiertas.pop()
        if len(self.cartas_descubiertas) == 0 and len(self.cartas_cubiertas) > 0:
            self.cartas_descubiertas.append(self.cartas_cubiertas.pop())
        return carta_sacada

    def puede_agregar_carta(self, carta):
        primer_carta = self.cartas_descubiertas[-1]
        return not carta.es_joker and (
            carta.numero >= primer_carta.numero - 1 and
            carta.numero <= primer_carta.numero + 1
            ) and carta.palo == primer_carta.palo

    def agregar_carta(self, carta):
        if not self.puede_agregar_carta(carta):
            raise ValueError(
                "No se puede agregar carta {} a esta tapada.".format(carta)
            )
        self.cartas_descubiertas.append(carta)