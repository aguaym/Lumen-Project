import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox
import threading
import step_motor.step_motor as motor
import led_control.led_control as led

class AppControle:
    def __init__(self, root):
        self.root = root
        self.root.title("Lumen-Project: Controle de Filme")
        self.root.geometry("300x250")

        self.rodando = False # Flag para controlar o motor

        # Interface Visual
        self.label = tk.Label(root, text="Status: Sistema Parado", font=("Arial", 12))
        self.label.pack(pady=20)

        self.btn_ligar = tk.Button(root, text="LIGAR SISTEMA", bg="green", fg="white", 
                                   width=20, height=2, command=self.iniciar)
        self.btn_ligar.pack(pady=10)

        self.btn_desligar = tk.Button(root, text="DESLIGAR TUDO", bg="red", fg="white", 
                                      width=20, height=2, command=self.parar)
        self.btn_desligar.pack(pady=10)

    def loop_motor(self):
        """Função que rodará em uma linha de execução separada"""
        while self.rodando:
            motor.mover_passo(0.003)
        motor.desligar_motor()
        print("[Thread] Motor finalizou o ciclo e desligou os pinos.")

    def iniciar(self):
        if not self.rodando:
            self.rodando = True
            self.label.config(text="Status: EM OPERAÇÃO", fg="green")

            # Liga o LED
            led.ligar_led()

            # Inicia o motor em uma thread separada para não travar a janela
            self.thread_motor = threading.Thread(target=self.loop_motor)
            self.thread_motor.daemon = True # Garante que a thread morra se fechar a janela
            self.thread_motor.start()
            print("Sistema Iniciado")

    def parar(self):
        self.rodando = False
        self.label.config(text="Status: Sistema Parado", fg="red")

        # Desliga Hardware
        led.desligar_led()
        print("Sistema Desligado com Segurança")

# Execução do Programa
if __name__ == "__main__":
    root = tk.Tk()
    app = AppControle(root)

    # Garante desligamento total ao fechar no 'X' da janela
    def ao_fechar():
        app.parar()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", ao_fechar)
    root.mainloop()
