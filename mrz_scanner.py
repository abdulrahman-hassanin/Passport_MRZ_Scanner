from mrz_ori_detection import ORI_Detector
from mrz_ocr import MRZ_OCR

import argparse
import cv2

if __name__ == '__main__':
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
        help="path to input image")
    ap.add_argument("-o", "--ocr", choices=['easyocr', 'pytesseract'], default='easyocr',
        help="OCR algorithm")
    ap.add_argument("-g", "--device", choices=['gpu', 'cpu'], default='gpu',
        help="Device used for processing gpu or cpu")
    args = vars(ap.parse_args())

    # Read Image
    image = cv2.imread(args["image"])

    # Detect MRZ
    ori_detector = ORI_Detector(image=image)
    ori_detector.detect_mrz_ORI()

    # Extract MRZ
    ocr = MRZ_OCR(image=ori_detector.mrz_box)
    if args["ocr"] == "easyocr":
        ocr.easyOCR(device=args["device"])
    else:
        ocr.pytesseract_OCR()

    # Print MRZ
    mrz_code = []
    text = ''.join(ocr.mrz)
    mrz_code.append(text[:int(len(text)/2)])
    mrz_code.append(text[int(len(text)/2):])

    # cv2.imshow("mrz", ori_detector.mrz_box)
    # cv2.waitKey(0)
    
    # Export to txt file
    f = open("output.txt", "w")
    f.write(mrz_code[0]+'\n')
    f.write(mrz_code[1])
    f.close()