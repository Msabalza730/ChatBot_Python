import os

import cv2
import pytesseract
from flask import Flask, jsonify, request
from pdf2image import convert_from_path
from PIL import Image
import requests
import tempfile

app = Flask(__name__)


ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}


def ocr_image(image_path, preprocess='thresh'):
    """This function is to proccess images into gray scale"""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if preprocess == 'thresh':
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    elif preprocess == 'blur':
        gray = cv2.medianBlur(gray, 3)

    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    text = pytesseract.image_to_string(Image.open(filename), lang='spa')

    os.remove(filename)

    return text


@app.route('/api/ocr', methods=['POST'])
def get_text():
    """
    This function is for extracting the text from a file and returning the response in a JSON.
    This is the step-by-step of the function:
        -Check if the request contains an file
        -Check if the file has an allowed extension
        -Save the file temporarily
        -Apply preprocessing
        -Convert PDF to images
        -Apply OCR using Tesseract
        -Delete the temporary file
        -Return the extracted text as a JSON response
    """
    if not request.json or 'file_url' not in request.json:
        return jsonify({'message': 'No URL provided'}), 400

    file_url = request.json['file_url']
    preprocess = request.json.get('preprocess', 'thresh')

    try:
        response = requests.get(file_url)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({'message': str(e)}), 400

    _, file_extension = os.path.splitext(file_url)
    file_extension = file_extension.lower().strip('.')

    if file_extension not in ALLOWED_EXTENSIONS:
        return jsonify({'message': 'File type not allowed'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
        temp_file.write(response.content)
        temp_file_path = temp_file.name

    text = ""

    if file_extension == 'pdf':
        try:
            images = convert_from_path(temp_file_path)
            for i, image in enumerate(images):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image_file:
                    image.save(temp_image_file.name, 'PNG')
                    text += ocr_image(temp_image_file.name, preprocess) + "\n"
                    os.remove(temp_image_file.name)
        except Exception as e:
            os.remove(temp_file_path)
            return jsonify({'message': str(e)}), 500
    else:
        text = ocr_image(temp_file_path, preprocess)

    os.remove(temp_file_path)

    response = {'message': 'success', 'text': text}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')