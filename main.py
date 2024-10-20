import cv2 as cv
import numpy as np

# Dimensions de l'image projetée
IMG_W = 1920
IMG_H = 1080
SCALE = (16, 9)
GRID_DIV = int(IMG_W / SCALE[0])

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
    imgCalib = np.ones(shape=(IMG_H, IMG_W), dtype=np.float32) * 255

    # On positionne nos marqueurs aux quatre coins de l'image
    cornerPoints = [
        (GRID_DIV, GRID_DIV),
        (IMG_W - GRID_DIV, GRID_DIV),
        (GRID_DIV, IMG_H - GRID_DIV),
        (IMG_W - GRID_DIV, IMG_H - GRID_DIV)
    ]

    # On crée un échiquier
    for i in range(1, SCALE[0]-2):
        for j in range(1, SCALE[1]-2):
            caseColor = 255 * (i * j % 2) # Alternate between black and white boxes
            cv.rectangle(imgCalib, ((i+j)*GRID_DIV), ((i+j+2)*GRID_DIV), caseColor, -1)

    cv.imshow('image', imgCalib)
    
    # Récupération des points de l'image projetée
    
    # TODO: get feed from camera
    frame = 1 # Capter la première frame de la caméra pour le setup

    captedCornerPoints = []
    cv.findChessboardCorners(frame, SCALE, captedCornerPoints)

    # Récupération de l'homographie entre l'image projetée et l'image captée
    H, status = cv.findHomography(cornerPoints, captedCornerPoints)

    # On ferme l'image de calibration
    cv.destroyAllWindows()

    return H



def main():
    calibration()


if __name__ == "__main__":
    main()