import cv2 as cv
import numpy as np

def detectDepthContours(referenceImage, depthImage):

    diffDepth = cv.absdiff(referenceImage, depthImage)
   
    threshValue = 500  # Threshold in mm 100mm = 0.1m)

    # Create a mask for all objects above the threshold (excluding 0 values)
    _, mask = cv.threshold(diffDepth, threshValue, 255, cv.THRESH_TOZERO)
    

    # Step 4: Use the mask to detect objects (i.e., find contours in the thresholded depth image)
    contours, _ = cv.findContours(mask.astype(np.uint8), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    return contours


def detectAndDrawContours(diffImage):
    """
    Detects contours of objects by calculating the difference between a captured and original image,
    then draws the contours on the captured image.
    
    Arguments:
        captured_image_path (str): Path to the captured image.
        
    
    Returns:
        tuple: List of detected contours and the image with contours drawn.
    """
   
    # diffImage = cv.cvtColor(diffImage, cv.COLOR_BGR2GRAY)
    diffImage = (diffImage/256).astype(np.uint8)
    diffImage = cv.GaussianBlur(diffImage, (5,5), sigmaX=5, sigmaY=5)

    # Apply a binary threshold to isolate the difference areas
    _, thresholded_diff = cv.threshold(diffImage, 1, 255, cv.THRESH_BINARY)

    # Optional: Apply morphological operations to clean up noise
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    cleaned_diff = cv.morphologyEx(thresholded_diff, cv.MORPH_CLOSE, kernel)

    # Find contours in the thresholded difference image
    contours, _ = cv.findContours(cleaned_diff, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Keep contours with a minimal area and make polygons
    contours = [c for c in contours if cv.contourArea(c) > 1500]
    # contoursSmooth = []
    # for i, c in enumerate(contours):
    #     perimeter = cv.arcLength(c, True)
    #     epsilon = 0.02 * perimeter  # Adjust epsilon to control the approximation accuracy
    #     approxContour = cv.approxPolyDP(c, epsilon, True)
    #     if len(approxContour) >= 4:
    #         contoursSmooth.append(approxContour)
    
    # Convert the captured image to BGR for contour drawing
    diffImage = cv.cvtColor(diffImage, cv.COLOR_GRAY2BGR)

    # Draw contours on the captured image
    # imC = np.array(cv.applyColorMap(diffImage, cv.COLORMAP_HSV))
    cv.drawContours(diffImage, contours, -1, (0, 255, 0), 2)
    
    # Color map (don't work well)
    # image = np.zeros_like(imC)
    # for i in range(len(diffImage)):
    #     for j in range(len(diffImage[0])):
    #         if not(diffImage[i][j][0] <= 2):
    #             image[i][j] = imC[i][j]
    # cv.imshow("colorMap", image)

    # cv.imshow("thresh", thresholded_diff)

    

    return contours, diffImage


def getContourCenters(cnts):
    """
    Checks all the contours given to determine which ones correspond to stable objects

    Arguments:
        cnts: all contours detected
    
    Return:
        centers: (cx, cy) coordinates of center points of contours
    """

    l = []
    for cnt in cnts:
        M = cv.moments(cnt)
        if M['m00']!=0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            l.append((cx, cy))
    return l

def getDistance(p1, p2):
    """
    Gives the euclidian between two points
    
    Arguments:
        p1, p2: points
    
    Return:
        d (float): distance between the two points
    """

    v = (p2[0]-p1[0], p2[1]-p1[1])
    return np.sqrt(v[0]**2 + v[1]**2)

def getMatches(pts1, pts2, thresh=40):
    """
    Gives all points from two lists that match
    A pair matches if their distance is lower than the threshold value

    Arguments:
        pts1: first list of points
        pts2: second list of points
        thresh: distance threshold

    Return:
        list: Elements of the first list that have matches in the second list
    """

    ret = []
    for p1 in pts1:
        for p2 in pts2:
            if getDistance(p1, p2) < thresh:
                ret.append(p1)

    return ret