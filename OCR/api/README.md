# Example Tesseract OCR with Python 

Tutorial: https://pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/

- Create a Python virtual env

```python
    - python3 -m venv env
    - source bin/activate
```
- Install the library:

```python
    -  pip install -r requirements.txt
```
- You need to install for pdf2image: sudo apt-get install poppler-utils

- Check the example of a run 

```python
    - python app.py
```
- Postman

    -Select form-data.
    -In the Key field, type file and in the field on the right select File.
    -Click Choose Files and select the file (image or PDF).


You can see the JSON Response with the text extracted from the file.

- Test with image
![image](https://github.com/Msabalza730/ChatBot_Python/assets/55921624/42661d5a-a73a-4ff6-b933-fe97e49b1d04)

  
- Test  PDF file
  ![image](https://github.com/Msabalza730/ChatBot_Python/assets/55921624/c5c32720-16b6-4820-ae32-b9dd438be8f2)

