import logging
import Cartas

logger = logging.getLogger('truco.juego')


class MasoTruco(Cartas.Maso):
    """
    Esta clase maneja el maso de TRUCO especificamente
    """
    def __init__(self):
        super().__init__(crear_cartas=False)
        for palo in Cartas.Carta.PALOS:
            self.cartas.extend([CartaTruco(numero, palo) for numero in CartaTruco.NUMEROS])

    def repartir(self, jugadores=2):
        cartas = 3
        if jugadores not in [2, 4]:
            raise ValueError('Por el momento solo soportamos juego entre 2 o 4 jugadores')
        mano = super().repartir(jugadores, cartas)
        muestra = mano.pop(-1)[0]  # Es el primer elemento de la ultima lista
        muestra.es_muestra = True
        mano.append(muestra)
        logger.debug(mano)
        return mano


class Mano(object):
    """
    Clase para manejar la mano (cartas asignadas) del jugador
    """
    def __init__(self, cartas, muestra):
        self.cartas = cartas
        self.muestra = muestra
        self.piezas = self._extraer_piezas()
        self.grupos = self._agruparXpalo()
        self.es_flor = self._es_flor()
        self.puntos = self._puntos()

    def _extraer_unidades(self, numero):
        """
        Recibe un entero y devuelve sus unidades
        """
        return int(str(numero)[-1:])

    def _extraer_piezas(self):
        """
        Devuelve una lista de las piezas en la mano
        """
        piezas = list()
        for carta in self.cartas:
            if carta.es_pieza(self.muestra):
                piezas.append(carta)
        return piezas

    def _agruparXpalo(self):
        """
        Devuelve un diccionario agrupando las cartas por palo
        """
        grupos = dict()
        for carta in self.cartas:
            if not grupos.get(carta.palo, False):
                grupos[carta.palo] = list()  # Creamos la entrada en el diccionario
            if not carta.es_pieza(self.muestra):  # No vamos a agregar las piezas
                grupos[carta.palo].append(carta)
        return grupos

    def _es_flor(self):
        """
        Determina si las cartas de la mano conforman una Flor
        """
        if len(self.piezas) > 1:
            # Con mas de 1 pieza es flor seguro
            logger.debug('Tiene 3 piezas')
            return True

        elif len(self.piezas) == 1 and max(len(v) for v in self.grupos.values()) == 2:
            # Si 1 es pieza y las otras tienen mismo palo
            logger.debug('Tiene 1 piezas y 2 cartas del mismo palo')
            return True

        elif max(len(v) for v in self.grupos.values()) == 3:
            # Si son 3 del mismo palo
            logger.debug('Tiene 3 del mismo palo')
            return True

        # Si no cumple los criterios anteriores, no es Flor.
        return False

    def _puntos(self):
        """
        Determina los puntos de la mano
        """
        sumatoria = [0, ]
        ordenadas = CartaTruco.orderar_puntuacion(self.cartas, self.muestra)
        if self.es_flor:  # Para un canto se suman las 3 cartas
            # . El valor entero de la carta mas alta y sumamos las unidades de las otras 2
            sumatoria.append(ordenadas[0].puntuacion(self.muestra))
            sumatoria.append(self._extraer_unidades(ordenadas[1].puntuacion(self.muestra)))
            sumatoria.append(self._extraer_unidades(ordenadas[2].puntuacion(self.muestra)))
            if not len(self.piezas):  # Cuando no hay piezas en la flor
                # Le sumamos 20pts por tener al menos 2 cartas del mismo palo ;)
                sumatoria.append(20)
            logger.debug(self.cartas)
            logger.debug(sumatoria)
        else:  # Para un toque hay varias condiciones
            if len(self.piezas) == 1:
                # . El valor entero de la carta mas alta y sumamos las unidades de la que le sigue en ponderacion
                sumatoria.append(ordenadas[0].puntuacion(self.muestra))
                sumatoria.append(self._extraer_unidades(ordenadas[1].puntuacion(self.muestra)))
                logger.debug(self.cartas)
                logger.debug(sumatoria)
            elif len(self.piezas) == 0:
                # Si no hay piezas se evalua si hay al menos 2 del mismo palo
                for cartas in self.grupos.values():
                    if len(cartas) == 2:
                        sumatoria.append(20)
                        sumatoria.extend(carta.puntuacion(self.muestra) for carta in cartas)
                        logger.debug(cartas)
                        logger.debug(sumatoria)
                        break  # Cortamos la iteracion si encontramos las dos cartas del mismo palo

                # Este caso ya seria cuando no tenemos nada de valor en la mano
                if max(len(cartas) for cartas in self.grupos.values()) == 1:
                    sumatoria.append(self._extraer_unidades(ordenadas[0].puntuacion(self.muestra)))
                    logger.debug(self.cartas)
                    logger.debug(sumatoria)
        # Devolvemos la sumatoria de valores
        return sum(sumatoria)


class CartaTruco(Cartas.Carta):
    """
    Esta clase maneja las cartas de TRUCO especificamente
    """
    PIEZAS = [2, 4, 5, 11, 10]
    MATAS = [(1, 'espada'), (1, 'basto'), (7, 'espada'), (7, 'oro')]
    NUMEROS = list(range(1, 8))  # Del 1 al 7 inc.
    NUMEROS.extend(list(range(10, 13)))  # Del 10 al 12 inc.

    def __init__(self, numero, palo, es_muestra=False):
        super().__init__(numero, palo)
        self.numero = CartaTruco.validar_numero(numero)
        self.numero_mostrar = self.numero
        self.es_muestra = es_muestra

    def __str__(self):
        return str(self.numero_mostrar) + self.palo

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def validar_numero(numero):
        """
        Validamos el palo dado y si no es valido levantamos una Excepcion
        """
        if numero not in CartaTruco.NUMEROS:
            raise ValueError('El numero indicado NO es valido. Utilice: %s' % ','.join(CartaTruco.NUMEROS))
        return numero

    def _es_alcahuete(self, muestra):
        """
        Si esta carta es el alcahuete, define sus valores como la pieza que representa
        """
        if self.numero == 12 and self.palo == muestra.palo and muestra.es_pieza(muestra):
            # Debemos copiarnos los valores de la muestra para imitarla
            self.numero = muestra.numero

    def es_pieza(self, muestra):
        """
        Determina si la carta es una pieza
        """
        self._es_alcahuete(muestra)
        # Una pieza se determina por su numero y si es del palo de la muestra
        if self.es_muestra:
            return self.numero in CartaTruco.PIEZAS
        else:
            return self.numero in CartaTruco.PIEZAS and self.palo == muestra.palo

    def es_mata(self):
        """
        Determina si la carta es una mata
        """
        # Las matas se definen por su numero (1 o 7) y su palo (dependiendo del numero).
        return (self.numero, self.palo) in CartaTruco.MATAS

    def es_fio(self, muestra):
        """
        Determina si la carta es un fio
        """
        # Un fio es una carta (1, 2 o 3) que no es pieza ni mata
        return self.numero in [1, 2, 3] \
            and not self.es_pieza(muestra) and not self.es_mata()

    def es_negra(self, muestra):
        """
        Determina si la carta es negra
        """
        # Solo validamos que no sea pieza por el numero que estamos evaluando
        return self.numero in [10, 11, 12] and not self.es_pieza(muestra)

    def es_blanca(self, muestra):
        """
        Determina si la carta es blanca
        """
        return self.numero in list(range(1, 8)) \
            and not self.es_fio(muestra) and not self.es_mata() and not self.es_pieza(muestra)

    def ponderacion(self, muestra):
        """
        Determina el valor de la carta dentro del juego (comparada al resto)
        NO utilizar para obtener el valor para contabilizar puntos de envido o similares.
        """
        pond = 0
        if self.es_pieza(muestra):
            # Le quitamos al valor mas alto el indice en el array
            pond = 30 - CartaTruco.PIEZAS.index(self.numero)  # Entre 30 y 26 inc.
        elif self.es_mata():
            pond = 25 - CartaTruco.MATAS.index((self.numero, self.palo))
        elif self.es_fio(muestra):
            # El valor de la negra mas alta + el numero de la carta
            pond = 12 + self.numero
        else:
            pond = self.numero
        logger.debug('Ponderacion: %i' % pond)
        return pond

    def puntuacion(self, muestra):
        """
        Determina el valor que la carta adquiere al sumar puntos de toque o cantos.
        El valor que adquiera esta carta en conjunto con otras debera manipularse en otro lado.
        """
        punt = 0  # Las negras no tienen valor de puntuacion
        if self.es_pieza(muestra):
            # Le quitamos al valor mas alto el indice en el array
            valor = 30 - CartaTruco.PIEZAS.index(self.numero)  # Entre 30 y 27 inc.
            punt = valor if self.numero != 10 else 27  # Nos aseguramos que la perica devuelva 27
        else:  # Cualquier carta blanca que no sea pieza vale su numero
            if not self.es_pieza(muestra) and self.numero in list(range(1, 8)):
                punt = self.numero
        logger.debug('Puntuacion: %i' % punt)
        return punt


class Jugador(object):
    """
    Clase para manejar a los jugadores, sus acciones, etc.
    """
    def __init__(self, nombre, partido=None, mano=None):
        self.nombre = nombre
        self.partido = partido
        self.mano = mano
