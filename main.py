import cv2 as cv
import numpy as np

# Dimensions de l'image projetée
IMG_W = 1920
IMG_H = 1080

def calibration():
    """
    Fonction d'initialisation qui :
    - Crée l'image virtuelle avec les marqueurs
    - Projète ces marqueurs
    - Récupère leur position via la caméra
    - En tire la matrice d'homographie

    :return: La matrice d'homographie
    """

    # Création d'une image blanche
    imgCalib = np.ones(shape=(IMG_H, IMG_W, 4), dtype=np.float32) * 255

    # On positionne nos marqueurs aux quatre coins de l'image
    sourcePoints = [
        (int(IMG_W/10), int(IMG_H/10)),
        (int(9*IMG_W/10), int(IMG_H/10)),
        (int(IMG_W/10), int(9*IMG_H/10)),
        (int(9*IMG_W/10), int(9*IMG_H/10))
    ]

    for pt in sourcePoints:
        cv.circle(imgCalib, center=(pt), radius=4, color=(0,0,0), thickness=8)

    cv.imshow('image', imgCalib)
    cv.waitKey(0)
    
    ###
    # RECUPERER COORDONNEES PROJETEES
    captedPoints = [] #placeholder
    ###

    # Récupération de l'homographie entre l'image projetée et l'image captée
    # H, status = cv.findHomography(sourcePoints, captedPoints)
    # return H



def main():
    calibration()


main()