import numpy as np
import cv2 as cv
import os
import datetime

def show_image(path):
    cv.namedWindow("calibration", cv.WINDOW_NORMAL)
    cv.setWindowProperty("calibration", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    image = cv.imread(path)
    cv.imshow('calibration', image)

def calibrate(webcam):
    # Alteração de env variable para resolver bug de lentidão na inicialização de camera logitech
    # https://github.com/opencv/opencv/issues/17687
    os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

    # Inicialização da câmera
    cap = cv.VideoCapture(webcam, cv.CAP_DSHOW)

    if not cap.isOpened():
        print("Erro ao abrir a webcam")
        exit()

    show_image('../calibration_images/camera_position.png')

    while (cap.isOpened()):
        # Execução a cada frame da webcam
        status, frame = cap.read()
        if status:
            lower_red = np.array([0, 0, 60])
            upper_red = np.array([70, 70, 255])
            mask = cv.inRange(frame, lower_red, upper_red)

            # Achar contornos
            contours, hier = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

            # Achar maior contorno
            cnt = contours[0]
            for cont in contours:
                if cv.contourArea(cont) > cv.contourArea(cnt):
                    cnt = cont


            epsilon = 0.01*cv.arcLength(cnt,True)
            approx = cv.approxPolyDP(cnt,epsilon,True)

            # Desenhar contornos na imagem canvas escuro
            mask_draw = mask.copy()
            mask_draw = cv.cvtColor(mask_draw, cv.COLOR_GRAY2BGR)
            contours_generated = cv.drawContours(mask_draw, [approx], -1, (0,0,255), 3)

            # cv.namedWindow("projetor", cv.WINDOW_NORMAL)
            # cv.setWindowProperty("projetor", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
            cv.imshow('projetor', contours_generated)

        else:
            print("Arquivo de vídeo terminou. Número total de frames: %d" % (cap.get(cv.CAP_PROP_FRAME_COUNT)))
            break

        key = cv.waitKey(1)
        # Esperar por tecla "q" para sair
        if key == ord('q'):
            break
        # Esperar por tecla "l" para limpar a tela
        elif key == ord('l'):
            blank = np.zeros(frame.shape, dtype='uint8')
        # Esperar por tecla "s" para salvar imagem
        elif key == ord('s'):
            ct = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            cv.imwrite(f'../screenshots/projetor_{ct}.jpg', frame)
            print(f"Imagem salva em ../screenshots/projetor_{ct}.jpg")

    cap.release()
    cv.destroyAllWindows()

def read_webcam(webcam):
    # Alteração de env variable para resolver bug de lentidão na inicialização de camera logitech
    # https://github.com/opencv/opencv/issues/17687
    os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

    # Inicialização da câmera
    cap = cv.VideoCapture(webcam, cv.CAP_DSHOW)

    if not cap.isOpened():
        print("Erro ao abrir a webcam")
        exit()

    # Criar canvas simulando quadro de projeção
    status, frame = cap.read()
    blank = np.zeros(frame.shape, dtype='uint8')

    show_image('../calibration_images/camera_position.png')

    while (cap.isOpened()):
        # Execução a cada frame da webcam
        status, frame = cap.read()
        if status:
            # Transformar para escala de cinza e aplicar threshold
            # Analisar histograma de testes para validar melhor threshold
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            threshold, thresh = cv.threshold(gray, 200, 255, cv.THRESH_BINARY)

            # Achar contornos
            contours, hier = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

            # Desenhar contornos em canvas escuro
            contours_generated = cv.drawContours(blank, contours, -1, (10,10,200), -1)

            cv.namedWindow("projetor", cv.WINDOW_NORMAL)
            cv.setWindowProperty("projetor", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
            cv.imshow('projetor', contours_generated)

        else:
            print("Arquivo de vídeo terminou. Número total de frames: %d" % (cap.get(cv.CAP_PROP_FRAME_COUNT)))
            break

        key = cv.waitKey(1)
        # Esperar por tecla "q" para sair
        if key == ord('q'):
            break
        # Esperar por tecla "l" para limpar a tela
        elif key == ord('l'):
            blank = np.zeros(frame.shape, dtype='uint8')
        # Esperar por tecla "s" para salvar imagem
        elif key == ord('s'):
            ct = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            cv.imwrite(f'./screenshots/projetor_{ct}.jpg', contours_generated)
            print(f"Imagem salva em ./screenshots/projetor_{ct}.jpg")

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    calibrate(0)
    