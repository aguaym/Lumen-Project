import threading

import motor.nema17 as motor
import led_control.led_control as led


class Controle:

    def __init__(self):
        self.rodando = False
        self.thread = None

    def loop_motor(self):
        motor.alinhar_filme(lambda: self.rodando)

    def iniciar(self):
        if self.rodando:
            return

        self.rodando = True
        led.ligar_led()

        self.thread = threading.Thread(
            target=self.loop_motor,
            daemon=True
        )
        self.thread.start()

    def parar(self):
        self.rodando = False
        led.desligar_led()
        motor.desligar_motor()