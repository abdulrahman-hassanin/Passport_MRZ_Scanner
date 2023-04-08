import cv2
import numpy as np
import sys
import imutils
from imutils.contours import sort_contours

class ORI_Detector():
    def __init__(self, image) -> None:
        self.image = image
        self.gray = None
        self.mrz_box_coordinates = None
        self.mrz_box = None

        # initialize a rectangular and square structuring kernel
        self.rectKernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, 
            (25, 7)
        )
        self.sqKernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, 
            (21, 21)
        )

    def image_to_gray(self):
        """
        Convert image to the gray scale
        """
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def smooth(self, kernel_size=3):
        """
        Smooth the image using  Gaussian blur
        """
        self.gray = cv2.GaussianBlur(self.gray, (kernel_size, kernel_size), 0)

    def find_dark_regions(self):
        """
        Apply blackhat morpholigical operator to find dark regions on a light
        background
        """
        blackhat = cv2.morphologyEx(self.gray, cv2.MORPH_BLACKHAT, self.rectKernel)
        return blackhat
    
    def apply_threshold(self, blackhat):
        # compute the Scharr gradient of the blackhat image and scale the
        # result into the range [0, 255]
        grad = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
        grad = np.absolute(grad)
        (minVal, maxVal) = (np.min(grad), np.max(grad))
        grad = (grad - minVal) / (maxVal - minVal)
        grad = (grad * 255).astype("uint8")

        # apply a closing operation using the rectangular kernel to close
        # gaps in between letters -- then apply Otsu's thresholding method
        grad = cv2.morphologyEx(grad, cv2.MORPH_CLOSE, self.rectKernel)
        thresh = cv2.threshold(grad, 0, 255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # cv2.imshow("Rect Close", thresh)

        # perform another closing operation, this time using the square
        # kernel to close gaps between lines of the MRZ, then perform a
        # series of erosions to break apart connected components
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, self.sqKernel)
        thresh = cv2.erode(thresh, None, iterations=2)
        # cv2.imshow("Square Close", thresh)
        
        return thresh

    def find_coordinates(self, thresh):
        """
        Find coordinates of the mrz code area
        """
        
        # find contours in the thresholded image and sort them from bottom
        # to top (since the MRZ will always be at the bottom of the passport)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sort_contours(cnts, method="bottom-to-top")[0]

        # initialize the bounding box associated with the MRZ
        mrzBox = None

        # loop over the contours
        (H, W) = self.gray.shape
        for c in cnts:
            # compute the bounding box of the contour and then derive the
            # how much of the image the bounding box occupies in terms of
            # both width and height
            (x, y, w, h) = cv2.boundingRect(c)
            percentWidth = w / float(W)
            percentHeight = h / float(H)
            
            # if the bounding box occupies > 80% width and > 4% height of the
            # image, then assume we have found the MRZ
            if percentWidth > 0.5 and percentHeight > 0.04:
                mrzBox = (x, y, w, h)
                break
            
        # if the MRZ was not found, exit the script
        if mrzBox is None:
            print("[INFO] MRZ could not be found")
            sys.exit(0)
            
        # pad the bounding box since we applied erosions and now need to
        # re-grow it
        (x, y, w, h) = mrzBox
        pX = int((x + w) * 0.03)
        pY = int((y + h) * 0.03)
        (x, y) = (x - pX, y - pY)
        (w, h) = (w + (pX * 2), h + (pY * 2))

        self.mrz_box_coordinates =  (x, y, w, h)
        self.mrz_box = self.image[y:y + h, x:x + w]

    def detect_mrz_ORI(self):
        self.image_to_gray()
        self.smooth()
        blackhat = self.find_dark_regions()
        thresh = self.apply_threshold(blackhat)
        self.find_coordinates(thresh)