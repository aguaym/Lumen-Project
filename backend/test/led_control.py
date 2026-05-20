from gpiozero import OutputDevice
from time import sleep

# Configuramos o relé no GPIO 18 (Pino 12)
# Se o seu relé ligar assim que você rodar o script (lógica invertida),
# mude active_high para False.
rele = OutputDevice(18, active_high=True, initial_value=False)

try:
    print("Sistema de Iluminação Pronto!")
    while True:
        comando = input("Digite '1' para LIGAR, '0' para DESLIGAR ou 'S' para sair: ").upper()

        if comando == '1':
            rele.on()
            print("LED: ACESO")
        elif comando == '0':
            rele.off()
            print("LED: APAGADO")
        elif comando == 'S':
            break
        else:
            print("Comando inválido.")

except KeyboardInterrupt:
    print("\nEncerrando...")
finally:
    rele.off() # Por segurança, apaga o LED ao fechar o programa
    print("Pino liberado.")
