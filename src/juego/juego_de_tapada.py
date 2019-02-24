from mazo.mazo_de_cartas import MazoInicial
from tapada import Tapada
from accion_jugador import Fuente, Destino
from escalera import Escalera


class Juego:
    CARTAS_EN_MANO = 5

    def __init__(self, jugador1, jugador2, cantidad_tapadas=10):
        """Empieza siempre primero el jugador1."""
        self.jugadores = (jugador1, jugador2)
        self.mazo = MazoInicial()
        self.cartas_jugadores = [[], []]
        self.tapadas = [
            Tapada(self.mazo.sacar_cartas(cantidad_tapadas)) for i in range(2)
        ]
        self.pilones = [
            [[[], [], []] for j in range(2)]
        ]
        self.escaleras = []
        self.cartas_usadas = []

    def jugar(self):
        """
        Juega la partida y devuelve el ganador.

        Si el mazo se quedó sin cartas antes de poder terminar el juego,
        devuelve -1.
        """
        jugador_actual = 0
        while True:
            self._turno(jugador_actual)
            if self._gano(jugador_actual):
                return jugador_actual
            jugador_actual = self._jugador_contrario(jugador_actual)
            if not self._hay_cartas_para_jugador(jugador_actual):
                return -1

    def _turno(self, indice_jugador):
        """Comienza el turno del jugador ```indice_jugador```."""
        if self._hay_cartas_para_jugador(indice_jugador):
            self._dar_cartas(indice_jugador)
            self._correr_acciones_de_jugador(indice_jugador)

    def _correr_acciones_de_jugador(self, indice_jugador):
        """
        Llama a ```jugar_turno``` del jugador correspondiente
        y realiza la accion correspondiente hasta que pase una de estas cosas:
            - El jugador termine su turno
            - El jugador gane la partida
            - El jugador necesite cartas y no haya más en el mazo
        """
        while True:
            accion_jugador = self.jugadores[indice_jugador].jugar_turno(
                self._informacion_para_jugador(indice_jugador)
            )
            self._realizar_accion(accion_jugador, indice_jugador)
            if accion_jugador.destino == Destino.PILON or self._gano(indice_jugador):
                break
            elif not self.cartas_jugadores[indice_jugador]:
                if not self._hay_cartas_para_jugador(indice_jugador):
                    break
                self._dar_cartas(indice_jugador)

    def _realizar_accion(self, accion, indice_jugador):
        carta = None
        indice_fuente = accion.indice_fuente

        if accion.fuente == Fuente.MANO:
            if indice_fuente >= len(self.cartas_jugadores[indice_jugador]):
                raise ValueError(
                    "La carta número {} no es una de la mano del jugador {}."
                    .format(indice_fuente, indice_jugador)
                )
            carta = self.cartas_jugadores[indice_jugador].pop(indice_fuente)

        elif accion.fuente == Fuente.TAPADA:
            if not self.tapadas[indice_jugador]:
                raise ValueError(
                    "No hay ninguna carta en la tapada del jugador {}."
                    .format(indice_jugador)
                )
            carta = self.tapadas[indice_jugador].pop()

        elif accion.fuente == Fuente.PILON:
            if not self.pilones[indice_jugador][indice_fuente]:
                raise ValueError(
                    "No hay ninguna carta en el pilón {} del jugador {}."
                    .format(indice_fuente, indice_jugador)
                )
            carta = self.pilones[indice_jugador][indice_fuente].pop()

        indice_destino = accion.indice_destino

        if accion.destino == Destino.PILON:
            self.pilones[indice_jugador][indice_destino].append(carta)
        elif accion.destino == Destino.ESCALERA:
            self._agregar_carta_a_escalera(carta, indice_destino)
        elif accion.destino == Destino.TAPADA_CONTRARIA:
            indice_contrario = self._jugador_contrario(indice_jugador)
            tapada_contraria = self.tapadas[indice_contrario]
            if not tapada_contraria.puede_agregar_carta(carta):
                raise ValueError(
                    "No se puede agregar la carta {} a la tapada del jugador {}."
                    .format(carta, indice_contrario)
                )
            tapada_contraria.agregar_carta(carta)

    def _informacion_para_jugador(self, indice_jugador):
        indice_contrario = self._jugador_contrario(indice_jugador)
        return InformacionParaJugador(
            cartas_en_mano=self.cartas_jugadores[indice_jugador],
            cant_cartas_en_mano_contrario=len(
                self.cartas_jugadores[indice_contrario]),
            tapadas_descubiertas=self.tapadas[indice_jugador].cartas_descubiertas,
            tapadas_descubiertas_contrario=self.tapadas[indice_contrario].cartas_descubiertas,
            cant_tapadas_cubiertas=len(
                self.tapadas[indice_jugador].cartas_cubiertas),
            cant_tapadas_cubiertas_contrario=len(
                self.tapadas[indice_contrario].cartas_cubiertas),
            pilones=self.pilones[indice_jugador],
            pilones_contrario=self.pilones[indice_contrario],
            escaleras=self.escaleras
        )

    def _jugador_contrario(self, indice_jugador):
        return indice_jugador + 1 % 2

    def _hay_cartas_para_jugador(self, indice_jugador):
        cantidad_nuevas_cartas = \
            self.CARTAS_EN_MANO - len(self.cartas_jugadores[indice_jugador])
        return len(self.mazo) >= cantidad_nuevas_cartas

    def _dar_cartas(self, indice_jugador):
        cantidad_nuevas_cartas = \
            self.CARTAS_EN_MANO - len(self.cartas_jugadores[indice_jugador])
        nuevas_cartas = self.mazo.sacar_cartas(cantidad_nuevas_cartas)

        for i in range(len(nuevas_cartas)):
            carta = nuevas_cartas[i]
            if carta.numero == 1:
                nuevas_cartas.pop(i)
                self._crear_nueva_escalera(carta)

        self.cartas_jugadores[indice_jugador].extend(nuevas_cartas)

    def _agregar_carta_a_escalera(self, carta, indice_escalera):
        if indice_escalera < 0:
            self._crear_nueva_escalera(carta)
        elif indice_escalera < len(self.escaleras):
            escalera = self.escaleras[indice_escalera]
            if not escalera.puede_agregar_carta(carta):
                raise ValueError(
                    "No se puede agregar carta {} a escalera número {}"
                    .format(carta, indice_escalera)
                )
            escalera.agregar_carta(carta)
        else:
            raise ValueError(
                "No existe la escalera con índice {}."
                .format(indice_escalera)
            )

    def _crear_nueva_escalera(self, carta):
        nueva_escalera = Escalera()
        if not nueva_escalera.puede_agregar_carta(carta):
            raise ValueError(
                "No se puede crear una escalera con carta {}."
                .format(carta)
            )
        nueva_escalera.agregar_carta(carta)
        self.escaleras.append(nueva_escalera)

    def _gano(self, indice_jugador):
        return (
            not self.tapadas[indice_jugador] and
            not self.cartas_jugadores[indice_jugador]
        )


class InformacionParaJugador:
    def __init__(self, cartas_en_mano, cant_cartas_en_mano_contrario,
                 tapadas_descubiertas, tapadas_descubiertas_contrario,
                 cant_tapadas_cubiertas, cant_tapadas_cubiertas_contrario,
                 pilones, pilones_contrario, escaleras):
        self.cartas_en_mano = cartas_en_mano
        self.cant_cartas_en_mano_contrario = cant_cartas_en_mano_contrario
        self.tapadas_descubiertas = tapadas_descubiertas
        self.tapadas_descubiertas_contrario = tapadas_descubiertas_contrario
        self.cant_tapadas_cubiertas = cant_tapadas_cubiertas
        self.cant_tapadas_cubiertas_contrario = cant_tapadas_cubiertas_contrario
        self.pilones = pilones
        self.pilones_contrario = pilones_contrario
        self.escaleras = escaleras
