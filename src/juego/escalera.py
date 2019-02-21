class Escalera:
    cartas = []
    numero_carta_actual = 0

    def puede_agregar_carta(self, carta):
        return (
            not self.llena() and
            (carta.es_joker or self.numero_carta_actual == carta.numero + 1)
        )

    def agregar_carta(self, carta):
        if not self.puede_agregar_carta(carta):
            raise ValueError("No se puede agregar esta carta.")

        self.cartas.append(carta)
        self.numero_carta_actual += 1

    def llena(self):
        return self.numero_carta_actual == 13
