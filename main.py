import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pyrealsense2 as rs
import time

import camera
from camera import IMG_H, IMG_W



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

    # Time delay used for calibration flow
    timeNow = time.time()
    TIME_LIMIT = 4


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
            depthImage = cv.warpPerspective(depthImage, H, (IMG_W, IMG_H))

            # Calibration
            if not calibDone:

                # Project a black image to use as a reference
                # Then, project a white image to use as a marker
                cv.imshow("", imgCalibBlack if delta < TIME_LIMIT else imgCalibWhite)

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
                    
            else:
                # Creating reference depth image
                # (non updated depth image used to check depth differences)
                if not refInit:
                    refDepth = depthImage.copy()
                    refColor = colorImage.copy()
                    refInit = True

                _, _ = camera.createDiffImages(H, depthImage, refDepth, colorImage, refColor)

                # Stop condition
                if cv.pollKey() != -1 and delta > TIME_LIMIT:
                    cv.destroyAllWindows()
                    break
        
        
        
    
    finally:
        pipeline.stop()


    

if __name__ == "__main__":
    main()