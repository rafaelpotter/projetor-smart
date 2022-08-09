import numpy as np
import cv2 as cv

def read_webcam(webcam):
    # webcam standard = 0
    cap = cv.VideoCapture(webcam)

    if not cap.isOpened():
        print("Error opening video")

    # size = (int(cap.get(3)), int(cap.get(4)))
    # print(size)
    status, frame = cap.read()
    blank = np.zeros(frame.shape, dtype='uint8')

    while (cap.isOpened()):
        # Frames da webcam
        status, frame = cap.read()
        if status:
            # Transformar para escala de cinza e aplicar threshold
            # Analisar histograma de testes para validar melhor threshold
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            threshold, thresh = cv.threshold(gray, 150, 255, cv.THRESH_BINARY_INV)

            # Achar contornos
            contours, hier = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

            # Desenhar contornos em canvas escuro
            contours_generated = cv.drawContours(blank, contours, -1, (0,0,255), -1)
            cv.imshow('contours blank', contours_generated)

        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    read_webcam('standard_data\laser_emulation.mp4')
    