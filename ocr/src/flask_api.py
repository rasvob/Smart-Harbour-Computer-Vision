from flask import Flask, request, jsonify
import base64
import ocr_model

app = Flask(__name__)

model = ocr_model.OCRModel()

@app.route('/serve', methods=['POST'])
def serve():
    
    data = request.get_json(force=True)
    image_data = base64.b64decode(data['image'])
    image = image_data
    text, results = model.readtext_postprocess(image)

    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True)


# TODO: lets think about concurrence and how to handle with locks or using pool of models