import base64
from flask import Flask, request, jsonify
from io import BytesIO
from PIL import Image
from model_usage import process_image

app = Flask(__name__)

@app.route('/upload-image', methods=['POST'])
def upload_image():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({"error": "No image data provided"}), 400

    try:
        image_byte = base64.b64decode(data['image'])
        image_final = Image.open(BytesIO(image_byte))
        recognized = process_image(image_final)
        print(recognized)
        return jsonify({"recognized": recognized}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
