import cv2 as cv

def identify_contour(image, blank_image):
    # Achar contornos
    contours, hier = cv.findContours(image, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

    # Desenhar contornos em canvas escuro
    contours_generated = cv.drawContours(blank_image, contours, -1, (0,0,255), -1)
    
    return contours_generated