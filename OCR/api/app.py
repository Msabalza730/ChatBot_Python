import os

import cv2
import numpy as np
import pytesseract
from flask import Flask, jsonify, request
from pdf2image import convert_from_path, pdfinfo_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError
from PIL import Image

app = Flask(__name__)


def allowed_file(filename):
    """This function is to upload files (images or pdf)"""
    allowed_extensions = {'png', 'jpg', 'jpeg', 'tiff', 'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


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

    text = pytesseract.image_to_string(Image.open(filename))

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

    if 'file' not in request.files:
        return jsonify({'message': 'No file provided'}), 400

    file = request.files['file']
    
    if not allowed_file(file.filename):
        return jsonify({'message': 'File type not allowed'}), 400
    
    file_path = os.path.join('/tmp', file.filename)
    file.save(file_path)

    preprocess = request.form.get('preprocess', 'thresh')
    text = ""

    if file.filename.lower().endswith('.pdf'):
        try:
            images = convert_from_path(file_path)
            for i, image in enumerate(images):
                temp_image_path = f"/tmp/page_{i}.png"
                image.save(temp_image_path, 'PNG')
                text += ocr_image(temp_image_path, preprocess) + "\n"
                os.remove(temp_image_path)
        except (PDFInfoNotInstalledError, PDFPageCountError) as e:
            return jsonify({'message': str(e)}), 500
    else:
        text = ocr_image(file_path, preprocess)


    os.remove(file_path)

    response = {'message': 'success', 'text': text}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)