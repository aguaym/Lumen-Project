import RPi.GPIO as GPIO
import time

# Pinos do Driver DRV8825 (Controle do Motor NEMA 17)
DIR_PIN = 22   # Define o sentido (Frente/Trás)
STEP_PIN = 27  # Recebe os pulsos para o passo
EN_PIN = 17    # Liga/Desliga a energia (LOW = Ligado, HIGH = Desligado)

# Pino do Sensor Infrarrojo TCRT5000 (D0)
SENSOR_PIN = 16 # <- AJUSTE PARA O PINO FÍSICO QUE ESCOLHER LIGAR O SENSOR

def inicializar_hardware():
    """
    Prepara os pinos do Raspberry Pi.
    Chama função ao iniciar o servidor.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Motor (Saídas)
    GPIO.setup(DIR_PIN, GPIO.OUT)
    GPIO.setup(STEP_PIN, GPIO.OUT)
    GPIO.setup(EN_PIN, GPIO.OUT)
    
    # Sensor (Entrada) - Usamos pull-up interno por segurança caso o fio solte
    GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Inicia com o motor desligado (livre e sem esquentar)
    GPIO.output(EN_PIN, GPIO.HIGH)
    print("[Hardware] Pinos configurados com sucesso.")

def desligar_hardware():
    """Libera os pinos. Chamar quando o servidor web for desligado."""
    GPIO.output(EN_PIN, GPIO.HIGH)
    GPIO.cleanup()
    print("[Hardware] Pinos liberados.")

def _dar_passo(delay_velocidade):
    """Gera o pulso físico para o driver DRV8825 (Uso interno)."""
    GPIO.output(STEP_PIN, GPIO.HIGH)
    time.sleep(0.001) # Pulso curto suficiente para o DRV8825 registrar
    GPIO.output(STEP_PIN, GPIO.LOW)
    time.sleep(delay_velocidade) # Dita a velocidade de cruzeiro

def ejetar_pelicula(passos=5000, delay=0.005):
    """
    Gira o motor continuamente para cuspir o resto da fita.
    Servidor Web pode chamar isso como um botão "Ejetar Manualmente" por exemplo.
    """
    print("[Motor] Iniciando ejeção da película...")
    GPIO.output(EN_PIN, GPIO.LOW) # Liga torque
    GPIO.output(DIR_PIN, GPIO.LOW) # Sentido de avanço
    
    for _ in range(passos):
        _dar_passo(delay)
        
    GPIO.output(EN_PIN, GPIO.HIGH) # Desliga torque
    print("[Motor] Ejeção concluída.")

# (INTEGRAÇÃO WEB)
def processar_rolo_automatico(verificar_parada_web, callback_tirar_foto):
    """
    Função principal de escaneamento para rodar em uma Thread separada na Web.
    
    Parâmetros que precisam ser passados:
    - verificar_parada_web: Função que retorna True se o usuário apertou "Parar" no navegador.
    - Callback_tirar_foto: Função que tira a foto e salva (o motor para automaticamente enquanto ela roda).
    """
    # Configurações de Segurança e Calibragem
    DELAY_NORMAL = 0.01          # Velocidade do motor procurando o furo
    LIMITE_PASOS_SEM_FURO = 1500 # Se der 1500 passos sem ver furo, a fita acabou ou travou
    
    # Liga o motor
    GPIO.output(EN_PIN, GPIO.LOW)
    GPIO.output(DIR_PIN, GPIO.LOW) # Sentido de avanço
    
    passos_desde_ultimo_furo = 0
    # Lê o estado inicial do sensor (0 = Furo/Luz passa, 1 = Película/Luz reflete)
    estado_anterior = GPIO.input(SENSOR_PIN)
    
    print("[Scanner] Iniciando tração automática...")
    
    try:
        # Loop roda enquanto parte web não mandar parar através da função verificar_parada_web()
        while not verificar_parada_web():
            
            _dar_passo(DELAY_NORMAL)
            passos_desde_ultimo_furo += 1
            
            # Leitura do Sensor TCRT5000
            estado_atual = GPIO.input(SENSOR_PIN)
            
            # LÓGICA DE DETECÇÃO (Borda de Descida: Passou da película para o furo)
            if estado_atual == 0 and estado_anterior == 1:
                print(f"[Scanner] Furo detectado! (Passos: {passos_desde_ultimo_furo})")
                
                # Zera o contador de segurança
                passos_desde_ultimo_furo = 0
                
                # O motor fica travado no lugar (com torque) enquanto a foto é tirada
                print("[Scanner] Avisando a interface Web para tirar a foto...")
                
                # Chama a função da câmera passada pelo parte Web
                callback_tirar_foto() 
                
                print("[Scanner] Foto concluída. Retomando avanço do motor...")
                # Dá um pequeno salto para o sensor sair de cima do furo atual e não ler duplicado
                for _ in range(50): 
                    _dar_passo(DELAY_NORMAL)
                    
            # LÓGICA DE TIMEOUT (Fim do rolo ou Atolamento)
            if passos_desde_ultimo_furo > LIMITE_PASOS_SEM_FURO:
                print("[Scanner] ALERTA: Limite de passos alcançado. Nenhum furo detectado.")
                print("[Scanner] O rolo acabou ou a fita travou. Iniciando Ejeção...")
                ejetar_pelicula(passos=3000)
                break # Encerra o processamento automático
                
            estado_anterior = estado_atual

    except Exception as e:
        print(f"[Erro no Scanner] Ocorreu uma falha: {e}")
        
    finally:
        # Garante que o motor não fique esquentando à toa
        GPIO.output(EN_PIN, GPIO.HIGH)
        print("[Scanner] Processamento finalizado. Motor em repouso.")
