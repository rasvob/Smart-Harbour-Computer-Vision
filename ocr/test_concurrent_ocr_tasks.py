import requests
import json
import base64
import time
import cv2
from concurrent.futures import ProcessPoolExecutor

def get_ocr_text(image, port):
    url = f'http://localhost:{port}/serve'
    encoded_image = base64.b64encode(image).decode('utf-8')
    headers = {'Content-Type': 'application/json'}
    data = {'image': encoded_image}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return json.loads(response.text)['text']

def validate_ocr(image, expected_text, port):    
    for x_min_crop, y_min_crop in [(0, 0), (100, 100), (300, 300), (128, 32), (200, 300)]:
        image_cropped = image[x_min_crop:, y_min_crop:, :]
        retval, buffer = cv2.imencode('.jpg', image_cropped)
        result = get_ocr_text(buffer, port=port)
        if expected_text != result:
            print(f"Expected: {expected_text}, got: {result}")
    return result

def test_service(port):
    test_data = [(cv2.imread('data_test/test1.png'), 'Test EesyOCR'), (cv2.imread('data_test/test2.png'), 'Příliš žluťoučký kůň')]
    start_time = time.time()    
    for _ in range(10):
        for image, expected_text in test_data:  
            validate_ocr(image, expected_text, port)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds. Port {port}.")
    

if __name__ == '__main__':
    ports = [5000, 5001]
    start_time = time.time()
    with ProcessPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(test_service, ports))
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time} seconds, ({(end_time - start_time)*1000} ms)")

"""
Experiments notes:

Single OCR service allocated ~2 GB GPU RAM.

In single running OCR service scenario for two workers the ~260ms per request was measured.
When the two OCR services were running, the time was ~180ms per request. 

During the optimization process the TensorRT of the OCR model was used with another approx 30% speedup. However the OCR module will needs to deal with various input dimensions and the TensorRT optimization is not straightforward.
"""