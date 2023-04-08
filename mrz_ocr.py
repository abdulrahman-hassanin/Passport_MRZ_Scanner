import cv2
import easyocr
import pytesseract

class MRZ_OCR:
    def __init__(self, image) -> None:
        self.image = image
        self.mrz = []


    def pytesseract_OCR(self):
        # OCR the MRZ region of interest using Tesseract
        mrzText = pytesseract.image_to_string(self.image,  lang='eng')

        # Remove any occurrences of spaceswhite
        mrzText = mrzText.replace(" ", "")
        self.mrz.append(mrzText)
    
    def easyOCR(self, device='gpu'):
        gpu = False
        if device == 'gpu':
            gpu = True
            
        reader = easyocr.Reader(['en'], gpu=gpu)
        results = reader.readtext(self.image)
        
        # loop over the results
        for (bbox, text, prob) in results:
            # unpack the bounding box
            (tl, tr, br, bl) = bbox
            tl = (int(tl[0]), int(tl[1]))
            tr = (int(tr[0]), int(tr[1]))
            br = (int(br[0]), int(br[1]))
            bl = (int(bl[0]), int(bl[1]))
            # cleanup the text and draw the box surrounding the text along
            # with the OCR'd text itself
            text = text.replace(" ", "")
            self.mrz.append(text)