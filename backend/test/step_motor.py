from gpiozero import OutputDevice
from time import sleep

# Configuração dos pinos
in1 = OutputDevice(17)
in2 = OutputDevice(27)
in3 = OutputDevice(22)
in4 = OutputDevice(23)
eixos = [in1, in2, in3, in4]

# Sequência  de torque máximo (Full-Step)
sequencia = [
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [1, 0, 0, 1]
]

# Para inverter sentido, descomentar essa linha
#sequencia.reverse()

def mover(delay_passo):
    for estado in sequencia:
        for i in range(4):
            if estado[i] == 1:
                eixos[i].on()
            else:
                eixos[i].off()
        sleep(delay_passo)

try:
    print("Rodando indefinidamente em Modo de Torque Máximo.")
    print("Pressione Ctrl+C para parar com segurança.")

    while True:
        mover(0.003) # Mudar valor para ajustar a velocidade/força (0.002 a 0.005)

except KeyboardInterrupt:
    print("\nParada solicitada pelo usuário.")
finally:
    # Desliga tudo para não esquentar o motor parado
    for pino in eixos:
        pino.off()
    print("Sistema desligado com segurança.")
