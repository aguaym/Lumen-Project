import cv2
import numpy as np

def testar_com_arquivo():
    # Carrega a imagem que já tirou.OpenCV já lê em formato BGR por padrão
    nome_arquivo = "hardware_test.jpg"
    img = cv2.imread(nome_arquivo)

    if img is None:
        print(f"Erro: Não foi encontrado  o arquivo {nome_arquivo}. Verifique se ele está na mesma pasta.")
        return

    print("Invertendo e processando...")

    # Inversão de Cores. Transformamos o negativo em positivo
    foto_invertida = cv2.bitwise_not(img)

    # Remoção da Máscara (Algoritmo Gray World)
    b, g, r = cv2.split(foto_invertida)
    
    media_b = np.mean(b)
    media_g = np.mean(g)
    media_r = np.mean(r)
    media_total = (media_b + media_g + media_r) / 3

    # Ajuste fino: divide a média total pela média de cada canal
    # Compensa o excesso de ciano que vem do laranja do filme
    b = cv2.convertScaleAbs(b, alpha=(media_total / media_b)*0.85)
    g = cv2.convertScaleAbs(g, alpha=(media_total / media_g)*0.90)
    r = cv2.convertScaleAbs(r, alpha=(media_total / media_r)*1.25)

    resultado_final = cv2.merge((b, g, r))

    # Salvar o resultado
    cv2.imwrite("teste_positivo_final.jpg", resultado_final)
    print("Sucesso! Verifique o arquivo: teste_positivo_final.jpg")

if __name__ == "__main__":
    testar_com_arquivo()

