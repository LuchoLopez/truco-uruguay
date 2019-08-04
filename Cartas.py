import random


class Maso(object):
    def __init__(self, crear_cartas=True):
        self.cartas = list()
        if crear_cartas:
            for palo in Carta.PALOS:
                self.cartas.extend([Carta(numero, palo) for numero in Carta.NUMEROS])

    def barajar(self):
        # for i in range(0, 3):
        #     random.shuffle(self.cartas)
        random.shuffle(self.cartas)

    def repartir(self, jugadores=2, cartas=3):
        if len(self.cartas) < (jugadores * cartas) + 1:
            raise ValueError('No tenemos cartas suficientes para tantos jugadores')
        self.barajar()
        mano = list()
        aux = self.cartas[(-1 * cartas * jugadores) - 1:]
        for jugador in range(0, jugadores):
            mano.append(aux[jugador:cartas*jugadores:jugadores])
        # La muestra simpre es la carta siguiente al finalizar de dar a los jugadores
        muestra = aux.pop(-1)
        mano.append([muestra])
        return mano


class Carta(object):
    """
    Clase para manipular las cartas del juego
    """
    
    PALOS = ['basto', 'copa', 'espada', 'oro']
    NUMEROS = list(range(1, 13))  # Del 1 al 12 inc.

    def __init__(self, numero, palo):
        self.palo = Carta.validar_palo(palo)
        self.numero = Carta.validar_numero(numero)

    def __str__(self):
        return str(self.numero) + self.palo

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def validar_palo(palo):
        """
        Validamos el palo dado y si no es valido levantamos una Excepcion
        """
        if palo not in Carta.PALOS:
            raise ValueError('El palo indicado NO es valido. Utilice: %s' % ','.join(Carta.PALOS))
        return palo

    @staticmethod
    def validar_numero(numero):
        """
        Validamos el numero dado y si no es valido levantamos una Excepcion
        """
        if numero not in Carta.NUMEROS:
            raise ValueError('El numero indicado NO es valido. Utilice: %s' % ','.join(Carta.NUMEROS))
        return numero

    @staticmethod
    def ganadora(cartaA, cartaB):
        """
        Devuelve la instancia de la carta que gana al enfrentar dos de ellas
        """
        return cartaA if cartaA.ponderacion() > cartaB.ponderacion() else cartaB

    @staticmethod
    def orderar_puntuacion(lista_cartas, muestra=None):
        return sorted(lista_cartas, key=lambda carta: carta.puntuacion(muestra), reverse=True)

    def ponderacion(self, *args, **kwargs):
        """
        Determina el valor de la carta dentro del juego (comparada al resto)
        """
        return self.numero

    def puntuacion(self, *args, **kwargs):
        """
        Determina el valor de la carta para sumar puntos
        """
        return self.numero
