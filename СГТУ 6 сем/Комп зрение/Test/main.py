from flask import Flask, render_template, request, jsonify, url_for
import cv2
import numpy as np
import os
import base64
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tiff'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    uploaded_filename = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            uploaded_filename = filename #Pass filename to template

    return render_template('index.html', uploaded_filename=uploaded_filename)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/resize/<filename>', methods=['POST'])
def resize(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        width = int(request.form['width'])
        height = int(request.form['height'])
        interpolation = request.form.get('interpolation', 'bicubic')

        img = cv2.imread(filepath)
        if img is None:
            return jsonify({'error': 'Could not read image'}), 500

        resized = cv2.resize(img, (width, height), interpolation={
            'nearest': cv2.INTER_NEAREST,
            'bilinear': cv2.INTER_LINEAR,
            'bicubic': cv2.INTER_CUBIC
        }.get(interpolation, cv2.INTER_CUBIC))

        _, buffer = cv2.imencode('.jpg', resized)
        img_str = base64.b64encode(buffer).decode('utf-8')
        return jsonify({'image': img_str})

    except Exception as e:
        return jsonify({'error': str(e)}), 500



app.run(port=80)