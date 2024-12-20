import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pyrealsense2 as rs
import time

import camera
from camera import IMG_H, IMG_W
from contourdetect import *


def main():
    
    # Create a context object. This object owns the handles to all connected realsense devices
    pipeline = rs.pipeline()
    pipeline.start()
    align = rs.align(rs.stream.color)

    # Variable initialisation
    calibDone = False # Checks if calibration is done
    H = None


    # Static images used for calibration
    imgCalibWhite = camera.flatImage(255)
    imgCalibBlack = camera.flatImage(0)
    # Blank image to get correct data type
    refImage = imgCalibBlack.copy()
    refDepth = imgCalibBlack.copy()
    refInit = False

    # Blank list of contour centers
    centers, oldCenters = [], []

    # Time delay used for calibration flow
    timeNow = time.time() # Ref for calibration
    TIME_LIMIT = 4 # Time after which the calibration goes to the next step

    # Time delay for object detection update
    centerRef = time.time()
    centerDelta = 0
    CENTER_UPDATE_INTERVAL = 3


    try:
        # DEBUG breaks manually once calibration is done
        while True:

            # Get time difference for calibration steps
            delta = time.time() - timeNow

            # Create a pipeline object. This object configures the streaming camera and owns it's handle
            frames = pipeline.wait_for_frames()
            depth = frames.get_depth_frame()
            if not depth: continue

            alignedFrames = align.process(frames)

            # Get color feed from camera
            colorFrame = alignedFrames.get_color_frame()
            colorImage = np.asanyarray(colorFrame.get_data())
            colorImage = cv.rotate(colorImage, cv.ROTATE_180)
            colorImage = cv.cvtColor(colorImage, cv.COLOR_RGB2BGR)

            # Get depth feed from camera
            depthFrame = alignedFrames.get_depth_frame()
            depthImage = np.asanyarray(depthFrame.get_data())*5
            depthImage = cv.rotate(depthImage, cv.ROTATE_180)

            # Calibration
            if not calibDone:

                # Project a black image to use as a reference
                # Then, project a white image to use as a marker
                cv.imshow("", imgCalibBlack if delta < TIME_LIMIT else imgCalibWhite)
                cv.setWindowProperty("", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

                # Get reference image once the camera feed is settled
                if delta >= TIME_LIMIT - 1 and delta <= TIME_LIMIT:
                    refImage = colorImage.copy()

                # Shows difference between ref image and camera feed after TIME_LIMIT
                srcPts, dstPts = camera.calibration(cv.absdiff(colorImage, refImage) if delta > TIME_LIMIT else colorImage)

                # Once everything is in the right position, we can calibrate
                if cv.pollKey() != -1:
                    calibDone = not calibDone
                    # print('\n\n', srcPts, '\n\n', dstPts, '\n\n')
                    # print(len(srcPts))
                    H = cv.getPerspectiveTransform(srcPts, dstPts)
                    # print(H)
                    cv.destroyAllWindows()
                    timeNow = time.time()




            # Once calib is done, we wait for a second to give the program time to settle  
            elif delta > 1:
                centerDelta = time.time() - centerRef # Updating delta
                oldCenters = centers.copy() # Saving the object centers of last frame

                # Warping images
                depthImage = cv.warpPerspective(depthImage, H, (IMG_W, IMG_H))
                colorImage = cv.warpPerspective(colorImage, H, (IMG_W, IMG_H))

                # Creating reference depth image
                # (non updated depth image used to check depth differences)
                if not refInit:
                    refDepth = depthImage.copy()
                    print(refDepth)
                    refColor = colorImage.copy()
                    refInit = True 

                depthDiff, colorDiff = camera.createDiffImages(H, depthImage, refDepth, colorImage, refColor)
                contours, ImageObjectContours = detectAndDrawContours(depthDiff)
                # contours = detectDepthContours(refDepth, depthImage)

                # Draw contours on the captured image
                cv.drawContours(ImageObjectContours, contours, -1, (0, 0, 255), thickness=cv.FILLED)

                # Get corresponding contours
                # Update regularly to take in new contours
                if int(centerDelta) % CENTER_UPDATE_INTERVAL+1 == CENTER_UPDATE_INTERVAL:
                    oldCenters = []
                    centerRef = time.time()

                # If we don't have any saved points, we take new ones
                # It allows for updating and checking if new points are to be added
                centers = getContourCenters(contours)
                if len(oldCenters) != 0:
                    centers = getMatches(oldCenters, centers)

                # DEBUG: Show centers of kept contours
                for c in centers:
                    cv.circle(ImageObjectContours, c, 10, (255, 150, 0), -1)
                for c in oldCenters:
                    cv.circle(ImageObjectContours, c, 5, (0, 255, 150), -1)
                

                cv.namedWindow("detectObjet", cv.WINDOW_NORMAL)
                # cv.setWindowProperty("detectObjet", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
                cv.imshow("detectObjet",ImageObjectContours)

               
                # Stop condition
                if cv.pollKey() != -1 and delta > TIME_LIMIT:
                    cv.destroyAllWindows()
                    break 
        
        
        
    
    finally:
        pipeline.stop()


    

if __name__ == "__main__":
    main()