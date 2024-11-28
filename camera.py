import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pyrealsense2 as rs

# Dimensions de l'image projetée
IMG_W = 1280
IMG_H = 720
SCALE = (16, 9)

CALIB_THRESHOLD = 30
DEPTH_FACTOR = 5



def flatImage(n):
    """
    Fonction d'initialisation qui crée l'image virtuelle avec les marqueurs

    :return: L'image blanche à projeter
    """

    # Création d'une image blanche
    imgFlat = np.ones(shape=(IMG_H, IMG_W), dtype=np.float32) * n

    return imgFlat




def calibration(imageCamera):
    """
    - Récupère leur position via la caméra
    - En tire la matrice d'homographie

    :return: La matrice d'homographie
    """
    
    # Coordonnées de l'image projetée pour la calibration
    # On positionne nos marqueurs aux quatre coins de l'image
    cornerPoints = np.float32([
        (0, 0),
        (0, IMG_H),
        (IMG_W, IMG_H),
        (IMG_W, 0)
    ])

    captedCornerPoints = cornerPoints.copy()
    
    cv.imshow("RenderImage", imageCamera)
    imageContours = imageCamera.copy()

    # Getting corners from the projected white image
    gray = cv.cvtColor(imageCamera, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv.threshold(blurred, CALIB_THRESHOLD, 255, cv.THRESH_BINARY) 
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Getting only the contour with the largest area
    # -> contour of the projected image
    contour = None
    areas = []

    for elem in contours:
        areas.append(cv.contourArea(elem))

    for index, elem in enumerate(areas):
        if elem == max(areas):
            contour = contours[index]

    # Once a contour is found:
    if len(contours) > 0:
        # Calculate the perimeter of the contour
        # Approximate the contour with a polygon (epsilon controls the approximation accuracy)
        perimeter = cv.arcLength(contour, True)
        epsilon = 0.02 * perimeter  # Adjust epsilon to control the approximation accuracy
        approxContour = cv.approxPolyDP(contour, epsilon, True)
        cv.drawContours(imageContours, [approxContour], 0, (0, 255, 0), 3)
    else:
        approxContour = []

    cv.imshow("Contours", imageContours)
    cv.imshow("Thresh", thresh)

    # Get corners in correct type
    if len(approxContour) == 4:
        for index, point in enumerate(approxContour):
            captedCornerPoints[index][0], captedCornerPoints[index][1] = point[0][0], point[0][1]

    return captedCornerPoints, cornerPoints

def camLoop(alignedFrames, H, refDepth):
    """
    Core of the image treatment

    :alignedFrames: Camera feed
    :H: Perspective matrix
    :refDepth: Reference depth image for comparison and differences
    """
    depthFrame = alignedFrames.get_depth_frame()
    depthImage = np.asanyarray(depthFrame.get_data())*5
    depthImage = cv.rotate(depthImage, cv.ROTATE_180)
    depthImage = cv.warpPerspective(depthImage, H, (IMG_W, IMG_H))

    depthDiff = cv.absdiff(refDepth, depthImage)*DEPTH_FACTOR

    colorFrame = alignedFrames.get_color_frame()
    colorImage = np.asanyarray(colorFrame.get_data())
    colorImage = cv.rotate(colorImage, cv.ROTATE_180)
    colorImage = cv.cvtColor(colorImage, cv.COLOR_RGB2BGR)
    colorImage = cv.warpPerspective(colorImage, H, (IMG_W, IMG_H))

    # Proceed to calibration and get reference depth
    # If done a second time, stops the loop
    # if cv.pollKey() != -1 and delta > LIMIT:
    #     keyInput += 1
    #     referenceDepth = depthImage
    #     H = calibration(colorImage)
    #     cv.destroyWindow("Marqueurs")
    
    # if keyInput == 1:
    #     depthImage = cv.absdiff(depthImage, referenceDepth)

    cv.imshow("RenderImage", colorImage)
    cv.imshow("RenderDepth", depthImage)
    cv.imshow("Ref Depth", refDepth)
    cv.imshow("Depth diff", )

if __name__=="__main__":
    # marqueur()
    camLoop()
