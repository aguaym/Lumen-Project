import RPi.GPIO as GPIO
import time
import camera.captura as camera

# ==========================
# PINOS
# ==========================
DIR_PIN = 22
STEP_PIN = 27
EN_PIN = 17
SENSOR_PIN = 16

VELOCIDADE = 0.005   # Ajuste conforme necessário

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(EN_PIN, GPIO.OUT)

GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def dar_passo():

    GPIO.output(STEP_PIN, GPIO.HIGH)
    time.sleep(VELOCIDADE)

    GPIO.output(STEP_PIN, GPIO.LOW)
    time.sleep(VELOCIDADE)


def alinhar_filme(rodando):

    print("Sistema iniciado.")

    GPIO.output(EN_PIN, GPIO.LOW)

    time.sleep(0.5)

    GPIO.output(DIR_PIN, GPIO.LOW)

    furos_detectados = 0
    alvo_furos = 10

    estado_anterior = GPIO.input(SENSOR_PIN)

    while rodando():

        dar_passo()

        estado_atual = GPIO.input(SENSOR_PIN)

        if estado_atual == 0 and estado_anterior == 1:

            furos_detectados += 1

            print(f"Furo {furos_detectados}/{alvo_furos}")

            if furos_detectados >= alvo_furos:

                print("Fotograma posicionado.")

                camera.capturar_e_processar()

                print("Processamento concluído.")

                furos_detectados = 0
                alvo_furos = 7

                for _ in range(40):

                    if not rodando():
                        break

                    dar_passo()

        estado_anterior = estado_atual

    desligar_motor()


def desligar_motor():

    GPIO.output(EN_PIN, GPIO.HIGH)

    print("Motor desligado.")


def cleanup():

    desligar_motor()
    GPIO.cleanup()
