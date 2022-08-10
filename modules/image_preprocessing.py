import cv2 as cv

def image_preprocess(image):
    # Transformar para escala de cinza e aplicar threshold
    # Analisar histograma de testes para validar melhor threshold
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    threshold, thresh = cv.threshold(gray, 200, 255, cv.THRESH_BINARY)

    return thresh