import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import time

import pyrealsense2 as rs

# Dimensions de l'image projetée
IMG_W = 1280
IMG_H = 720
SCALE = (16, 9)
GRID_DIV = int(IMG_W / SCALE[0])

def marqueur():
    """
    Fonction d'initialisation qui :
    - Crée l'image virtuelle avec les marqueurs
    - Projète ces marqueurs
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
    for i in range(1, SCALE[0]-1):
        for j in range(1, SCALE[1]-1):
            caseColor = 255 * ((i+j) % 2) # Alternate between black and white boxes
            cv.rectangle(imgCalib, (i*GRID_DIV, j*GRID_DIV), ((i+1)*GRID_DIV, (j+1)*GRID_DIV), caseColor, -1)

    cv.imshow('image', imgCalib)
    cv.waitKey(0)

    # return H

def calibration():
    """
    - Récupère leur position via la caméra
    - En tire la matrice d'homographie

    :return: La matrice d'homographie
    """
    # Récupération des points de l'image projetée
    
    # TODO: get feed from camera
    frame = 1 # Capter la première frame de la caméra pour le setup

    # captedCornerPoints = []
    # cv.findChessboardCorners(frame, SCALE, captedCornerPoints)

    # Récupération de l'homographie entre l'image projetée et l'image captée
    # H, status = cv.findHomography(cornerPoints, captedCornerPoints)

    # On ferme l'image de calibration
    # cv.destroyAllWindows()

def camTest():
    # Create a context object. This object owns the handles to all connected realsense devices
    pipeline = rs.pipeline()
    pipeline.start()

    align = rs.align(rs.stream.color)

    try:
        while True:
            # Create a pipeline object. This object configures the streaming camera and owns it's handle
            frames = pipeline.wait_for_frames()
            depth = frames.get_depth_frame()
            if not depth: continue

            alignedFrames = align.process(frames)

            depthFrame = alignedFrames.get_depth_frame()
            depthImage = np.asanyarray(depthFrame.get_data())*5
            depthImage = cv.rotate(depthImage, cv.ROTATE_180)
            depthImage = np.dstack([depthImage, depthImage, depthImage])

            colorFrame = alignedFrames.get_color_frame()
            colorImage = np.asanyarray(colorFrame.get_data())
            colorImage = cv.rotate(colorImage, cv.ROTATE_180)
            colorImage = cv.cvtColor(colorImage, cv.COLOR_RGB2BGR)

            # # Print a simple text-based representation of the image, by breaking it into 10x20 pixel regions and approximating the coverage of pixels within one meter
            # coverage = [0]*64
            # for y in range(480):
            #     for x in range(640):
            #         dist = depth.get_distance(x, y)
            #         if 0 < dist and dist < 1:
            #             coverage[x//10] += 1

            #     if y%20 is 19:
            #         line = ""
            #         for c in coverage:
            #             line += " .:nhBXWW"[c//25]
            #         coverage = [0]*64
            #         print(line)

            cv.imshow("RenderImage", colorImage)
            cv.imshow("Render", depthImage)
            cv.waitKey(0)

    finally:
        pipeline.stop()

if __name__=="__main__":
    # marqueur()
    camTest()
