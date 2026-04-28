import cv2
import numpy as np
from picamera2 import Picamera2
import time
import os

# Definir a pasta de saida
PASTA_SAIDA = os.path.expanduser("~/Lumen_Project/output/")
if not os.path.exists(PASTA_SAIDA):
    os.makedirs(PASTA_SAIDA)

def capturar_e_processar():
    # Configuração da Câmera
    picam2 = Picamera2()
    config = picam2.create_still_configuration()
    picam2.configure(config)
    picam2.start()

    print("Preparando captura...")
    time.sleep(17)

    # Captura (formato RGB)
    img_raw = picam2.capture_array()
    picam2.stop()

    timestamp = int(time.time())

    print("Processando cores...")

    # Convertemos de RGB para BGR
    img_bgr = cv2.cvtColor(img_raw, cv2.COLOR_RGB2BGR)

    nome_negativo = os.path.join(PASTA_SAIDA, f"negativo_{timestamp}.jpg")

    # Salva negativo
    cv2.imwrite(nome_negativo, img_bgr)

    print(f"Arquivo original salvo: {nome_negativo}")
    
    # Inversao correta
    img_inv = 255 - img_bgr

    # Converte a float 
    img = img_inv.astype(np.float32) / 255.0

    # Separa canais
    b, g, r = cv2.split(img)

    # Balance de brancos (gray world)
    avg_b = np.mean(b)
    avg_g = np.mean(g)
    avg_r = np.mean(r)

    avg = (avg_b + avg_g + avg_r) / 3

    b *= avg / (avg_b + 1e-6)
    g *= avg / (avg_g + 1e-6)
    r *= avg / (avg_r + 1e-6)

    img = cv2.merge([b, g, r])

    # Normalizacao por canal
    for i in range(3):
        ch = img[:, :, i]
        ch = (ch - ch.min()) / (ch.max() - ch.min() + 1e-6)
        img[:, :, i] = ch

    # Curva tonal (com gamma)
    gamma = 0.9
    img = np.power(img, gamma)

    # Volver a 8 bits
    resultado_positivo = np.clip(img * 255, 0, 255).astype(np.uint8)

    # Ajuste final leve
    resultado_positivo = cv2.convertScaleAbs(resultado_positivo, alpha=1.1, beta=3)
    
    # Salva positivo
    nome_positivo = os.path.join(PASTA_SAIDA, f"positivo_{timestamp}.jpg")
    cv2.imwrite(nome_positivo, resultado_positivo)

    print(f"Digitalização concluída: {nome_positivo}")

    # Abre arquivos 
    print("Abrindo imagens para comparação...")
    os.system(f"xdg-open {nome_negativo}")
    os.system(f"xdg-open {nome_positivo}")

if __name__ == "__main__":
    capturar_e_processar()
