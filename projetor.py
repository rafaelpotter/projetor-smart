import numpy as np
import cv2 as cv

def read_webcam():
    cap = cv.VideoCapture('data\laser_tests_trim.mp4') # use (0) for webcam
    # Frames da webcam
    ret, frame = cap.read()
    blank = np.zeros(frame.shape, dtype='uint8')

    while True:
        ret, frame = cap.read()
        # Transformar para escala de cinza e aplicar threshold
        # Analisar histograma de testes para validar melhor threshold
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        threshold, thresh = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)

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
    read_webcam()
    