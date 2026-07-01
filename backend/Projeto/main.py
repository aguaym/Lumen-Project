import tkinter as tk

from gui.interface import AppControle

import motor.nema17 as motor

import led_control.led_control as led


root = tk.Tk()

app = AppControle(root)


def fechar():

    app.parar()

    motor.cleanup()

    root.destroy()


root.protocol("WM_DELETE_WINDOW", fechar)

root.mainloop()
