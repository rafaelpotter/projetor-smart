import numpy as np
import cv2

def read_webcam():
    cap = cv2.VideoCapture('data\laser_tests_trim.mp4') # use (0) for webcam

    while True:
        ret, frame = cap.read()

        cv2.imshow('frame', frame)

        blank_Image = np.zeros(frame.shape, np.uint8)
        cv2.imshow('blank_Image', blank_Image)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    read_webcam()
    