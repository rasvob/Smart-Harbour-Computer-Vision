import easyocr
import time

class OCRModel():
    def __init__(self) -> None:
        self.reader = easyocr.Reader(['cs', 'en'], gpu=True)

    def readtext(self, image):
        return self.reader.readtext(image)

    def readtext_postprocess(self, image):
        start = time.time()
        results = self.readtext(image)
        text_to_concat = list()
        for ocr_result in sorted(results, key=lambda x: x[0][0][0]):
            if ocr_result[2] > 0.1:
                text_to_concat.append(ocr_result[1])
        print(f'OCR took {time.time() - start:.2f}s')
        return ''.join(text_to_concat), results
