#app.py
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String , Sequence
import cv2
import easyocr
from matplotlib import pyplot as plt
import numpy as np
import os
from werkzeug.utils import secure_filename
from flask import Flask ,jsonify
import time
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String , Sequence
from datetime import datetime
import ast
 
app = Flask(__name__)

app.app_context().push

 
UPLOAD_FOLDER = 'static/uploads/'
P_IMAGES = 'static/p_image/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['P_IMAGES'] = P_IMAGES
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'This is my secrete key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///little_cabs.db'
app.config['SQLALCHMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_plate(path,file_name):
    print("processing")
    width = 300
    height = 200

    reader = easyocr.Reader(['en'],gpu=False)
    result = reader.readtext(path)
    #print(result)
    text = result[0][1]
    n_p = text.replace("]","")
    top_left = tuple(result[0][0][0])
    bottom_right = tuple(result[0][0][2])
    text = result[0][1]
    print(text)
    font =cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.imread(path)
    img = cv2.rectangle(img ,top_left,bottom_right,(0,255,0),5)
    img = cv2.putText(img,text,top_left,font, 0.5 ,(255,255,255),2,cv2.LINE_AA)
    img_resized = cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA)
    output_image_path = os.path.join(app.config['P_IMAGES'],file_name)
    cv2.imwrite(output_image_path,img_resized)
    print(output_image_path)
    return(output_image_path)

def search_car (path):
    print("processing_car Details")
    reader = easyocr.Reader(['en'],gpu=False)
    result = reader.readtext(path)
    text = result[0][1]
    n_p = text.replace("]","")
    top_left = tuple(result[0][0][0])
    bottom_right = tuple(result[0][0][2])
    text = result[0][1]

    cardet = str(car_details.query.filter_by(Reg_no=n_p).first())
    print(cardet)   
    return(cardet)    


class car_details(db.Model):
        identity = Column(Integer,primary_key=True)
        Reg_no = Column(String)
        Dvr_name = Column(String)
        Car_Color = Column(String)
        ip = Column(String)
        #driver_pic = Column(String)
        def __repr__(self) :
                lit_cab =[]
                test_list =[]
                lit_det = {}
                lit_det["Driver_Name"] = self.Dvr_name
                lit_det["Number_plate"] = self.Reg_no
                lit_det["Color"]= self.Car_Color
                lit_det["Insuarance"] = self.ip
                lit_cab.append(lit_det)
                env_json = json.dumps(lit_det,indent=4)
                return env_json
        # def __repr__(self) :
        #     return '<Car_details %r>' % self.Reg_no
     
 
@app.route('/')
def home():
    return render_template('index.html')

 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        y = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        flash('Image successfully uploaded and displayed below')
        print("the processed image")
        print(y)
        car_data = search_car (y)
        res = json.loads(car_data)
        # print(res["Driver_Name"])
        # print(res["Number_plate"])

        return render_template('index.html', filename= detect_plate(y,filename),item = res)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/<filename>')
def display_image(filename):
    print(filename)
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='p_image/' + filename), code=301)

    #return redirect(url_for(filename), code=301)
 
if __name__ == "__main__":
    app.run()