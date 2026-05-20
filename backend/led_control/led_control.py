from gpiozero import OutputDevice

# Configuração do pino 12 (GPIO 18)
rele = OutputDevice(18, active_high=True, initial_value=False)

def ligar_led():
    rele.on()

def desligar_led():
    rele.off()
