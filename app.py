import os
os.environ["CUDA_VISIBLE_DEVICES"]="True"
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'
import numpy as np
import pickle
import pandas as pd
from flask import Flask, request, render_template

from flask import Flask, render_template, request
from flask_sqlalchemy  import SQLAlchemy
from flask import *


from werkzeug.utils import secure_filename
from PIL import Image
import pyttsx3
import easyocr
reader = easyocr.Reader(['en','hi'])

app = Flask(__name__)


def model_predict(img_path):
    parsed = reader.readtext(img_path)
    result = ' '.join(map(lambda x: x[1], parsed))
    return result
def text_to_speech(text):
    """
    Function to convert text to speech
    :param text: text
    :param gender: gender
    :return: None
    """
    voice_dict = {'Male': 1, 'Female': 0}
    code = voice_dict['Male']

    engine = pyttsx3.init()

    engine.setProperty('rate', 125)

    engine.setProperty('volume', 0.8)

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[code].id)

    engine.say(text)
    engine.runAndWait()



@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        
        f = request.files['file']

       
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

       
        preds = model_predict(file_path)
        result = preds
        text_to_speech(result)
        return result
    
    return None

    
if __name__ == '__main__':
    app.run(debug=True)
