import logging
import Juego

logger = logging.getLogger('truco.tests')


def testear():
    maso = Juego.MasoTruco()
    reparto = maso.repartir(jugadores=4)
    muestra = reparto[-1:][0]  # Asi devolvemos la carta, y no una lista
    j1 = Juego.Jugador('luis', mano=Juego.Mano(reparto[0], muestra))
    j2 = Juego.Jugador('luis', mano=Juego.Mano(reparto[1], muestra))
    j3 = Juego.Jugador('luis', mano=Juego.Mano(reparto[2], muestra))
    j4 = Juego.Jugador('luis', mano=Juego.Mano(reparto[3], muestra))
    return {'j1': vars(j1.mano), 'j2': vars(j2.mano), 'j3': vars(j3.mano), 'j4': vars(j4.mano)}


def test_puntuacion():
    carta1 = Juego.CartaTruco(1, 'espada')
    carta2 = Juego.CartaTruco(5, 'espada')
    carta3 = Juego.CartaTruco(3, 'espada')
    muestra = Juego.CartaTruco(4, 'basto', es_muestra=True)
    j1 = Juego.Jugador('jugador1', mano=Juego.Mano([carta1, carta2, carta3], muestra))
    # logger.info(vars(j1.mano))
    return {'j1': vars(j1.mano)}


def test_flor():
    oro11 = Juego.CartaTruco(11, 'oro')
    espada4 = Juego.CartaTruco(4, 'espada')
    espada1 = Juego.CartaTruco(1, 'espada')
    oro3 = Juego.CartaTruco(3, 'oro', es_muestra=True)
    j1 = Juego.Jugador('jugador1', mano=Juego.Mano([oro11, espada4, espada1], oro3))
    logger.info(vars(j1.mano))
