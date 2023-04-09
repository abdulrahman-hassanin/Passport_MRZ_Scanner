# Passport_MRZ_Scanner
Scan MRZ code of the passport card and extract the text.

MRZ code contains some information of the passport owner like name, surname, date of birth, etc.

# Approach
The algorithm has two main stages:

### MRZ Detection
Detect the MRZ code section using image processing algorithms.

### MRZ OCR
Feed MRZ into OCR algorithm to extract the text. In this approach you can use any of two OCR algorithms [EasyOCR](https://github.com/JaidedAI/EasyOCR) and [Tesseract](https://github.com/tesseract-ocr/tesseract).

| EasyOCR  | Tesseract |
| :-------------: | :-------------: |
| preferable for GPU  | preferable for CPU  |
| better job on words  | better on character level |

# Usage
```bash
python mrz_ocr.py --image images\0.jpg --ocr easyocr --device gpu
```

# Output

* Sample Input passport ID

<p align="center">
  <img alt="sample input" height=300 src="images/0.jpg">
</p>


* Detect the MRZ Region

<p align="center">
  <img alt="MRZ Region" width=450 src="assets/mrz_code.jpg">
</p>


* Extract MRZ code into text

<p align="center">
  <img alt="MRZ text" width=450 src="assets/mrz_text.jpg">
</p>