import numpy as np
import cv2 as cv
import time

def read_webcam(webcam):
    # para usar webcam, webcam=0
    cap = cv.VideoCapture(webcam)
    if not cap.isOpened():
        print("Error opening video")

    fps= int(cap.get(cv.CAP_PROP_FPS))

    # Criar canvas simulando quadro de projeção
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

            time.sleep(1/fps)
            cv.namedWindow("projetor", cv.WINDOW_NORMAL)
            cv.setWindowProperty("projetor", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
            cv.imshow('projetor', contours_generated)

        else:
            print("Video file finished. Total Frames: %d" % (cap.get(cv.CAP_PROP_FRAME_COUNT)))
            break

        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    read_webcam('standard_data\laser_emulation.mp4')
    