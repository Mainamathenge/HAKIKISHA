from flask import Flask, render_template, request, session, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String , Sequence
import cv2
import easyocr
from matplotlib import pyplot as plt
import numpy as np
import os
from werkzeug.utils import secure_filename
paths = "D:/projects/VS_CODE/little_cabs/code_files/KCE620B.png"

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def detect_plate(path):
        reader = easyocr.Reader(['en'],gpu=False)
        result = reader.readtext(path)
        #print(result)
        text = result[0][1]
        n_p = text.replace("]","")
        #print(n_p)
        return n_p 

# #print(detect_plate(paths))
app = Flask(__name__,template_folder = 'templateFiles',static_folder='staticFiles')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'This is my secrete key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///little_cabs.db'
app.config['SQLALCHMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class car_details(db.Model):
        CAR_registration = Column(String,primary_key=True)
        NAME = Column(String)
        id_number = Column(String)
        insuarance_provider = Column(String)
        insuarance_validity = Column(String)
        driver_pic = Column(String)
        def __repr__(self) :
                lit_cab = {}
                lit_det = {}
                lit_det["Name"] = self.NAME
                lit_det["ID_NUMBER"] = self.id_number
                lit_det["insuarance_provider"] = self.insuarance_provider
                lit_det["insuarance_validity"] = self.insuarance_validity
                lit_cab[self.CAR_registration] = lit_det
                return f'{lit_cab}'
                


@app.route('/')
def detect_image():
        #number_plate = detect_plate(paths)

        return render_template('index_upload_disp.html')

@app.route('/',methods=['GET','POST'])
def uploadimage():
        if request.method == 'POST':
                if request.files:
                        print("received")
                        image = request.files['uploaded-file']
                        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
                        print("received_saved")
                        # uploaded_image.save(os.path.join(app.config['UPLOAD_FOLDER'],img_filname))
                        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],image)

        return render_template('show_uploaded_img2.html')

@app.route('/show_image')
def displayImage():
        img_file = session.get('uploaded_img_file_path',None)

        return render_template('show_image.html',user_image = img_file )


if __name__ == '__main__':
        app.run()
