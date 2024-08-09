import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from ultralytics import YOLO
import cv2


app = Flask(__name__)


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
model = YOLO("model/final.pt")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/upload_image', methods=['POST'])

def upload_image():
    if 'image' not in request.files:
        return render_template('index.html', error='No file part')
    
    file = request.files['image']
    
    if file.filename == '':
        return render_template('index.html', error='No selected file')
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        image = cv2.imread(file_path)
        results = model(image, conf=0.6)
        highest_confidence = 0
        best_class_name = ""
        for r in results:
            for idx, class_idx in enumerate(r.probs.top5):
                class_name = r.names[class_idx]
                confidence = float(r.probs.top5conf[idx])
                if confidence > highest_confidence:
                    highest_confidence = confidence
                    best_class_name = class_name
        return render_template('index.html', 
                               best_class_name=best_class_name,
                               highest_confidence=highest_confidence)
        
    else:
        return render_template('index.html', error='Invalid file type')
    
    

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)