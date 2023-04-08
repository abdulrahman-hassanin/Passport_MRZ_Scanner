from mrz_ori_detection import ORI_Detector
from mrz_ocr import MRZ_OCR

import argparse
import cv2

if __name__ == '__main__':
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
        help="path to input image to be OCR'd")
    args = vars(ap.parse_args())

    # Read Image
    image = cv2.imread(args["image"])

    # Detect MRZ
    ori_detector = ORI_Detector(image=image)
    ori_detector.detect_mrz_ORI()

    # Extract MRZ
    ocr = MRZ_OCR(image=ori_detector.mrz_box)
    ocr.easyOCR()
    # ocr.pytesseract_OCR()

    # Print MRZ
    text = ''.join(ocr.mrz)
    print(text[:int(len(text)/2)])
    print(text[int(len(text)/2):])

    cv2.imshow("mrz", ori_detector.mrz_box)
    cv2.waitKey(0)
    
    # Export to txt file