from gpiozero import OutputDevice
from time import sleep

# Pinos do motor
eixos = [OutputDevice(17),
         OutputDevice(27),
         OutputDevice(22),
         OutputDevice(23)]

# Sequência de Torque Máximo
sequencia = [[1, 1, 0, 0],
             [0, 1, 1, 0],
             [0, 0, 1, 1],
             [1, 0, 0, 1]]

# Se precisar inverter o sentido, descomente/comente a linha abaixo:
# sequencia.reverse()

def mover_passo(delay=0.003):
    for estado in sequencia:
        for i in range(4):
            if estado[i] == 1: eixos[i].on()
            else: eixos[i].off()
        sleep(delay)

def desligar_motor():
    for pino in eixos:
        pino.off()
