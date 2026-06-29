import RPi.GPIO as GPIO
import time

# MAPEAMENTO DOS PINOS
DIR_PIN = 22
STEP_PIN = 27
EN_PIN = 17
SENSOR_PIN = 16

# CONFIGURAÇÃO INICIAL
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define pinos de saída (Motor)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(EN_PIN, GPIO.OUT)

# Define pino de entrada (Sensor IR) com Pull-Up
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# VELOCIDADE (Pulso simétrico)
VELOCIDADE = 0.01

def dar_passo():
    """Função com o pulso simétrico que funciona no driver"""
    GPIO.output(STEP_PIN, GPIO.HIGH)
    time.sleep(VELOCIDADE)
    GPIO.output(STEP_PIN, GPIO.LOW)
    time.sleep(VELOCIDADE)

try:
    print("==================================================")
    print(" INICIANDO ALINHAMENTO AUTOMÁTICO DE FOTOGRAMAS")
    print(" Pressione [ CTRL + C ] para abortar")
    print("==================================================")

    # 1. Liga o motor (Torque ativado) e define a direção
    GPIO.output(EN_PIN, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(DIR_PIN, GPIO.LOW)

    # 2. Variáveis de Controle Lógico
    furos_detectados = 0
    alvo_furos = 10  # Começa buscando 10 furos para pular o início do filme
    estado_anterior = GPIO.input(SENSOR_PIN)

    print(f"\n[Fase 1] Pulando o início do filme. Buscando {alvo_furos} furos...")

    # 3. Loop de Avanço Contínuo
    while True:
        dar_passo()

        # Lê o estado do sensor neste milissegundo
        estado_atual = GPIO.input(SENSOR_PIN)

        # Borda de Descida: 1 (Película) -> 0 (Furo)
        if estado_atual == 0 and estado_anterior == 1:
            furos_detectados += 1
            print(f"> Furo detectado: {furos_detectados} / {alvo_furos}")

            # Verifica se a meta foi atingida
            if furos_detectados >= alvo_furos:
                print("==================================================")
                print(" ALVO ATINGIDO! Fotograma posicionado.")
                print(" Pausando motor por 5 segundos...")

                # Pausa de 5 segundos (O motor continua com torque, segurando a fita no lugar)
                time.sleep(5.0)

                print(" Retomando avanço para a próxima foto...")
                print("==================================================\n")

                # Zera a contagem e muda o alvo para 7 furos a partir de agora
                furos_detectados = 0
                alvo_furos = 7

                # Debounce Mecânico: Dá um pequeno pulo às cegas para tirar
                # o sensor de cima do furo atual, evitando dupla contagem
                for _ in range(40):
                    dar_passo()

        # Atualiza o estado para a próxima volta do loop
        estado_anterior = estado_atual

except KeyboardInterrupt:
    print("\n[Aviso] Comando de parada recebido pelo usuário!")

finally:
    # 4. Encerramento Seguro
    print("Cortando a energia do motor (Enable = HIGH) para esfriar...")
    GPIO.output(EN_PIN, GPIO.HIGH)
    GPIO.cleanup()
    print("Sistema desligado com segurança.")
