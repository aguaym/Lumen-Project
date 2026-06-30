import cv2
import numpy as np

def balanco_branco_gray_world(img):
    # separa os canais novamente após a inversão
    B, G, R = cv2.split(img)
    
    # calcula o brilho médio de cada canal de cor
    mB = np.mean(B)
    mG = np.mean(G)
    mR = np.mean(R)
    
    # encontra a média global da imagem
    media_global = (mB + mG + mR) / 3.0
    
    # escala cada canal para que a média de todos fique igual
    # O cv2.convertScaleAbs já lida com os limites de 0 a 255 de forma segura
    B_corrigido = cv2.convertScaleAbs(B, alpha=(media_global / mB))
    G_corrigido = cv2.convertScaleAbs(G, alpha=(media_global / mG))
    R_corrigido = cv2.convertScaleAbs(R, alpha=(media_global / mR))
    
    # junta os canais corrigidos
    return cv2.merge([B_corrigido, G_corrigido, R_corrigido])

def converter_negativo(caminho_imagem):
    # 1. Carregamento
    img = cv2.imread(caminho_imagem)
    if img is None:
        raise ValueError("Imagem não encontrada. Verifique o caminho/arquivo.")

    # inversão básica
    invertida = cv2.bitwise_not(img)

    # remoção da máscara laranja
    canais = cv2.split(invertida)
    canais_corrigidos = []

    for canal in canais:
        min_val = np.percentile(canal, 1)
        max_val = np.percentile(canal, 99)
        canal_clip = np.clip(canal, min_val, max_val)
        canal_norm = cv2.normalize(canal_clip, None, 0, 255, cv2.NORM_MINMAX)
        canais_corrigidos.append(np.uint8(canal_norm))

    # reconstrução
    img_final = cv2.merge(canais_corrigidos)

    # correção do desvio Azul/Ciano (White Balance)
    img_balanceada = balanco_branco_gray_world(img_final)

    return img_balanceada

if __name__ == "__main__":
    positivo = converter_negativo('WhatsApp Image 2026-05-15 at 22.04.04.jpeg')
    
    cv2.imwrite('resultado_positivo.jpg', positivo)
    
    cv2.imshow('Conversao Final', positivo)
    cv2.waitKey(0)
    cv2.destroyAllWindows()