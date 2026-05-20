import sys
from time import sleep
from gpiozero import DigitalInputDevice

# Configura o sensor no GPIO 24 com Pull-Up ativado
sensor = DigitalInputDevice(24, pull_up=True)

print("=" * 40)
print("   TESTE LÓGICO DO SENSOR TCRT5000   ")
print("=" * 40)
print("Passe a película ou o dedo na frente do sensor.")
print("Pressione Ctrl+C para encerrar o teste.\n")

try:
    while True:
        # Captura o valor exato que o pino do Pi está recebendo (0 ou 1)
        valor_puro = sensor.value

        # Módulos envia 1 (HIGH) quando detecta reflex
        # e 0 (LOW) quando a luz se perde no furo.
        if valor_puro == 1:
            status = "FILME DETECTADO (Superfície Sólida)"
        else:
            status = "FURO DETECTADO (Vazio / Perfuração)"

        print(f"Valor do Pino: {valor_puro} | Status Lógico: {status}")

        # Aguarda 200 milissegundos antes da próxima leitura
        sleep(0.3)

except KeyboardInterrupt:
    print("\n[INFO] Teste encerrado pelo usuário.")
