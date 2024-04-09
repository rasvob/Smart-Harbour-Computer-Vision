import easyocr
import time
from . import dto


class OCRModel():
    def __init__(self) -> None:
        self.reader = easyocr.Reader(['cs', 'en'], gpu=True)

    def readtext_postprocess(self, image):
        start = time.time()
        results = self.readtext(image)
        # convert the results coordinates to int
        results = [(list(map(lambda x: list(map(round, x)), result[0])), result[1], result[2]) for result in results]
        text_to_concat = list()
        for ocr_result in sorted(results, key=lambda x: x[0][0][0]):
            if ocr_result[2] > 0.1:
                text_to_concat.append(ocr_result[1])
        print(f'OCR took {time.time() - start:.2f}s')
        return dto.OCRResultModel(text=''.join(text_to_concat), ocr_recognitions=results)

    def readtext(self, image):
        return self.reader.readtext(image)
