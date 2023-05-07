from flask import Flask , render_template  , request , send_file
import os
from keras.models import  load_model
import tensorflow as tf
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)

# configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(BASE_DIR , 'model.h5'))

ALLOWED_EXTENSIONS = {'jpg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

new_dict = {
    0: 'Melanocytic nevi',
    1: 'Melanoma',
    2: 'Benign keratosis-like lesions ',
    3: 'Basal cell carcinoma',
    4: 'Actinic keratoses',
    5: 'Vascular lesions',
    6: 'Dermatofibroma'
}

def predict(image_path , model):
    img = tf.keras.preprocessing.image.load_img(image_path)
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = tf.image.resize(img, size=(100, 125))
    img = np.expand_dims(img, axis=0)
    pred = model.predict(img)
    pred = np.argmax(pred, axis=1)
    print(pred[0])
    result = new_dict[pred[0]]

    return result


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success', methods = ['POST'])
def success():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='Please select an image.')

        file = request.files['file']

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print(file_path)
        res = predict(file_path, model)
        return  render_template('success.html' , filename=filename, res=res)


@app.route('/display/<filename>')
def display_image(filename):
    return send_file(os.path.join('uploads', filename))

if __name__ == '__main__':
    app.run(debug=True)