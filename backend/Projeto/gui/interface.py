import tkinter as tk
import threading

import motor.nema17 as motor
import led_control.led_control as led


class AppControle:

    def __init__(self, root):

        self.root = root

        self.root.title("Controle de Filme")

        self.root.geometry("320x220")

        self.rodando = False

        self.label = tk.Label(
            root,
            text="Status: Parado",
            font=("Arial",12)
        )

        self.label.pack(pady=20)

        self.bt_ligar = tk.Button(

            root,

            text="LIGAR",

            bg="green",

            fg="white",

            width=20,

            command=self.iniciar

        )

        self.bt_ligar.pack(pady=10)

        self.bt_parar = tk.Button(

            root,

            text="DESLIGAR",

            bg="red",

            fg="white",

            width=20,

            command=self.parar

        )

        self.bt_parar.pack()

    def loop_motor(self):

        motor.alinhar_filme(lambda: self.rodando)

    def iniciar(self):

        if self.rodando:

            return

        self.rodando = True

        self.label.config(

            text="Status: Operando",

            fg="green"

        )

        led.ligar_led()

        self.thread = threading.Thread(

            target=self.loop_motor,

            daemon=True

        )

        self.thread.start()

    def parar(self):

        self.rodando = False

        self.label.config(

            text="Status: Parado",

            fg="red"

        )

        led.desligar_led()

        motor.desligar_motor()
