from flask import Flask, render_template, request, jsonify, send_file
import cv2
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        image = cv2.imread(filepath)
        if image is None:
            return jsonify({'error': 'Unsupported or corrupted file'}), 400

        preview_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
        cv2.imwrite(preview_path, image)

        return jsonify({'preview_url': f'/static/uploads/preview.jpg'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/resize', methods=['POST'])
def resize_image():
    data = request.json
    scale_factor = float(data.get('scale_factor', 1.0))
    width = int(data.get('width', 0))
    height = int(data.get('height', 0))
    interpolation_method = data.get('interpolation', 'auto')

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    image = cv2.imread(image_path)

    if image is None:
        return jsonify({'error': 'Image not found'}), 400

    if width > 0 and height > 0:
        new_size = (width, height)
    else:
        new_size = (int(image.shape[1] * scale_factor), int(image.shape[0] * scale_factor))

    if interpolation_method == 'nearest':
        interpolation = cv2.INTER_NEAREST
    elif interpolation_method == 'bilinear':
        interpolation = cv2.INTER_LINEAR
    elif interpolation_method == 'bicubic':
        interpolation = cv2.INTER_CUBIC
    else:
        if scale_factor > 1:
            interpolation = cv2.INTER_CUBIC
        else:
            interpolation = cv2.INTER_AREA

    resized_image = cv2.resize(image, new_size, interpolation=interpolation)

    resized_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    cv2.imwrite(resized_path, resized_image)

    return jsonify({'resized_url': f'/static/uploads/preview.jpg'})

@app.route('/crop', methods=['POST'])
def crop_image():
    data = request.json
    x = int(data.get('x', 0))
    y = int(data.get('y', 0))
    width = int(data.get('width', 0))
    height = int(data.get('height', 0))

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    image = cv2.imread(image_path)

    if image is None:
        return jsonify({'error': 'Image not found'}), 400

    # Проверка координат и размеров
    if x < 0 or y < 0 or width <= 0 or height <= 0:
        return jsonify({'error': 'Invalid coordinates or dimensions'}), 400

    if x + width > image.shape[1] or y + height > image.shape[0]:
        return jsonify({'error': 'Crop area is outside the image bounds'}), 400

    # Вырезка прямоугольного фрагмента
    cropped_image = image[y:y+height, x:x+width]

    cropped_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    cv2.imwrite(cropped_path, cropped_image)

    return jsonify({'cropped_url': f'/static/uploads/preview.jpg'})

@app.route('/mirror', methods=['POST'])
def mirror_image():
    data = request.json
    direction = data.get('direction', 'horizontal')  # horizontal, vertical, both

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    image = cv2.imread(image_path)

    if image is None:
        return jsonify({'error': 'Image not found'}), 400

    # Зеркальное отражение
    if direction == 'horizontal':
        mirrored_image = cv2.flip(image, 1)
    elif direction == 'vertical':
        mirrored_image = cv2.flip(image, 0)
    elif direction == 'both':
        mirrored_image = cv2.flip(image, -1)
    else:
        return jsonify({'error': 'Invalid mirror direction'}), 400

    mirrored_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    cv2.imwrite(mirrored_path, mirrored_image)

    return jsonify({'mirrored_url': f'/static/uploads/preview.jpg'})

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

app.run(port=80)