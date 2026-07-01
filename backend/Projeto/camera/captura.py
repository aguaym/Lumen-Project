from picamera2 import Picamera2
import cv2
import os

from processamento.negativo import converter_negativo

picam2 = Picamera2()

config = picam2.create_still_configuration()

picam2.configure(config)

picam2.start()

contador = 1

PASTA_ORIGINAIS = "capturas/originais"
PASTA_POSITIVAS = "capturas/positivas"

os.makedirs(PASTA_ORIGINAIS, exist_ok=True)
os.makedirs(PASTA_POSITIVAS, exist_ok=True)


def capturar_e_processar():

    global contador

    nome = f"foto_{contador:04d}.jpg"

    caminho_original = os.path.join(PASTA_ORIGINAIS, nome)

    caminho_final = os.path.join(PASTA_POSITIVAS, nome)

    print("Capturando imagem...")

    picam2.capture_file(caminho_original)

    print("Imagem capturada.")

    positivo = converter_negativo(caminho_original)

    cv2.imwrite(caminho_final, positivo)

    print("Imagem processada.")

    contador += 1
