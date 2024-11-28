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
    contours = [c for c in contours if cv.contourArea(c) > 600]
    contoursSmooth = []
    for i, c in enumerate(contours):
        perimeter = cv.arcLength(c, True)
        epsilon = 0.02 * perimeter  # Adjust epsilon to control the approximation accuracy
        approxContour = cv.approxPolyDP(c, epsilon, True)
        if len(approxContour) >= 4:
            contoursSmooth.append(approxContour)
    
    # Convert the captured image to BGR for contour drawing
    diffImage = cv.cvtColor(diffImage, cv.COLOR_GRAY2BGR)

    # Draw contours on the captured image
    cv.drawContours(diffImage, contours, -1, (0, 255, 0), 2)

    cv.imshow("thresh", thresholded_diff)

    

    return contours, diffImage


