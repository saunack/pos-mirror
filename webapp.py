import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from text import get_amount
from keypad import get_keypad
import cv2

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/

@app.route("/")
def home():
    return render_template("UI.html")

@app.route('/result', methods = ['Get','POST'])
def upload_file():
    if request.method == 'POST':
        # parse amount
        f = request.files['file']
        cost = get_amount(f)
        f.stream.seek(0)
        f.save("data/temp.png")

        # PIN translation
        PIN = request.form['PIN']
        conversion_table, img = get_keypad('data/temp.png',PIN)
        translated_pin = ''
        cv2.imwrite("static/temp.png",img)
        for p in PIN:
            translated_pin += str(conversion_table[int(p)])
        return render_template("result.html", original=PIN, prediction = cost, translated_pin=translated_pin)
    else:
        return render_template("result.html", prediction = "404 Error")

if __name__ == "__main__":
    app.run(debug=True)
