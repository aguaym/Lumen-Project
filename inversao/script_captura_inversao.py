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

    foto_invertida = cv2.bitwise_not(img_bgr)

    b, g, r = cv2.split(foto_invertida)

    media_b = max(np.mean(b), 1)
    media_g = max(np.mean(g), 1)
    media_r = max(np.mean(r), 1)
    media_total = (media_b + media_g + media_r) / 3

    b = cv2.convertScaleAbs(b, alpha=(media_total / media_b) * 0.85)
    g = cv2.convertScaleAbs(g, alpha=(media_total / media_g) * 0.90)
    r = cv2.convertScaleAbs(r, alpha=(media_total / media_r) * 1.25)

    resultado_positivo = cv2.merge((b, g, r))

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
