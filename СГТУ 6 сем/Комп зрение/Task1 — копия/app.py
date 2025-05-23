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

    # Сохраняем оригинал
    original_path = os.path.join(app.config['UPLOAD_FOLDER'], 'original.jpg')
    file.save(original_path)

    try:
        image = cv2.imread(original_path)
        if image is None:
            return jsonify({'error': 'Unsupported or corrupted file'}), 400

        # Создаем превью (рабочую копию)
        preview_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
        cv2.imwrite(preview_path, image)

        return jsonify({
            'preview_url': f'/static/uploads/preview.jpg',
            'original_url': f'/static/uploads/original.jpg'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rotate', methods=['POST'])
def rotate_image():
    data = request.json
    angle = float(data.get('angle', 0))
    center_x = int(data.get('center_x', -1))
    center_y = int(data.get('center_y', -1))
    image_url = data.get('image_url', '')

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')

    image = cv2.imread(image_path)
    if image is None:
        return jsonify({'error': 'Image not found'}), 400

    (h, w) = image.shape[:2]
    if center_x == -1 or center_y == -1:
        center_x, center_y = w // 2, h // 2

    # Поворот изображения
    M = cv2.getRotationMatrix2D((center_x, center_y), angle, 1.0)
    rotated_image = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR)

    rotated_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    cv2.imwrite(rotated_path, rotated_image)

    return jsonify({'rotated_url': f'/static/uploads/preview.jpg'})

@app.route('/reset_image', methods=['POST'])
def reset_image():
    original_path = os.path.join(app.config['UPLOAD_FOLDER'], 'original.jpg')
    preview_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    
    # Проверяем существует ли оригинальное изображение
    if not os.path.exists(original_path):
        return jsonify({'error': 'Original image not found'}), 400
    
    # Копируем оригинал в preview
    import shutil
    shutil.copyfile(original_path, preview_path)
    
    return jsonify({'reset_url': f'/static/uploads/preview.jpg'})

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

@app.route('/adjust_brightness_contrast', methods=['POST'])
def adjust_brightness_contrast():
    data = request.json
    brightness = int(data.get('brightness', 0))
    contrast = float(data.get('contrast', 1.0))
    image_url = data.get('image_url', '')

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')

    image = cv2.imread(image_path)
    if image is None:
        return jsonify({'error': 'Image not found'}), 400

    # Изменение яркости и контрастности
    adjusted_image = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)

    adjusted_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    cv2.imwrite(adjusted_path, adjusted_image)

    return jsonify({'adjusted_url': f'/static/uploads/preview.jpg'})

@app.route('/adjust_color_balance', methods=['POST'])
def adjust_color_balance():
    data = request.json
    red = float(data.get('red', 1.0))
    green = float(data.get('green', 1.0))
    blue = float(data.get('blue', 1.0))
    image_url = data.get('image_url', '')
    
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')

    image = cv2.imread(image_path)
    if image is None:
        return jsonify({'error': 'Image not found'}), 400

    # Изменение цветового баланса
    b, g, r = cv2.split(image)
    r = cv2.multiply(r, red)
    g = cv2.multiply(g, green)
    b = cv2.multiply(b, blue)
    balanced_image = cv2.merge([b, g, r])

    balanced_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    cv2.imwrite(balanced_path, balanced_image)

    return jsonify({'balanced_url': f'/static/uploads/preview.jpg'})

@app.route('/add_noise', methods=['POST'])
def add_noise():
    data = request.json
    noise_type = data.get('noise_type', 'gaussian')
    image_url = data.get('image_url', '')

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')

    image = cv2.imread(image_path)
    if image is None:
        return jsonify({'error': 'Image not found'}), 400

    # Добавление шума
    if noise_type == 'gaussian':
        mean = 0
        stddev = 50
        noise = np.random.normal(mean, stddev, image.shape).astype(np.uint8)
        noisy_image = cv2.add(image, noise)
    elif noise_type == 'salt_pepper':
        prob = 0.05
        noisy_image = np.copy(image)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                rdn = random.random()
                if rdn < prob:
                    noisy_image[i][j] = 0
                elif rdn > 1 - prob:
                    noisy_image[i][j] = 255
    else:
        return jsonify({'error': 'Invalid noise type'}), 400

    noisy_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    cv2.imwrite(noisy_path, noisy_image)

    return jsonify({'noisy_url': f'/static/uploads/preview.jpg'})

@app.route('/save', methods=['POST'])
def save_image():
    data = request.json
    format = data.get('format', 'jpeg')
    quality = int(data.get('quality', 95))  # Качество для JPEG (0-100)
    image_url = data.get('image_url', '')

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    image = cv2.imread(image_path)
    if image is None:
        return jsonify({'error': 'Image not found'}), 400

    # Определяем параметры сохранения
    if format == 'jpeg':
        params = [cv2.IMWRITE_JPEG_QUALITY, quality]
        ext = '.jpg'
    elif format == 'png':
        params = [cv2.IMWRITE_PNG_COMPRESSION, 9]  # Сжатие для PNG (0-9)
        ext = '.png'
    elif format == 'tiff':
        params = []
        ext = '.tiff'
    else:
        return jsonify({'error': 'Unsupported format'}), 400

    # Сохраняем изображение
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], f'saved{ext}')
    success = cv2.imwrite(save_path, image, params)

    if not success:
        return jsonify({'error': 'Failed to save image'}), 500

    return jsonify({'saved_url': f'/static/uploads/saved{ext}'})

@app.route('/blur', methods=['POST'])
def blur_image():
    data = request.json
    blur_type = data.get('blur_type', 'gaussian')
    kernel_size = int(data.get('kernel_size', 5))
    image_url = data.get('image_url', '')

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    image = cv2.imread(image_path)
    if image is None:
        return jsonify({'error': 'Image not found'}), 400

    # Размытие изображения
    if blur_type == 'average':
        blurred_image = cv2.blur(image, (kernel_size, kernel_size))
    elif blur_type == 'gaussian':
        blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    elif blur_type == 'median':
        blurred_image = cv2.medianBlur(image, kernel_size)
    else:
        return jsonify({'error': 'Invalid blur type'}), 400

    blurred_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    cv2.imwrite(blurred_path, blurred_image)

    return jsonify({'blurred_url': f'/static/uploads/preview.jpg'})

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/change_color_space', methods=['POST'])
def change_color_space():
    data = request.json
    color_space = data.get('color_space', 'rgb')  # rgb, hsv, grayscale
    image_url = data.get('image_url', '')

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    image = cv2.imread(image_path)
    if image is None:
        return jsonify({'error': 'Image not found'}), 400

    # Изменение цветового пространства
    if color_space == 'hsv':
        converted_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    elif color_space == 'grayscale':
        converted_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        converted_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # По умолчанию RGB

    converted_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    cv2.imwrite(converted_path, converted_image)

    return jsonify({'converted_url': f'/static/uploads/preview.jpg'})

@app.route('/find_object_by_hsv', methods=['POST'])
def find_object_by_hsv():
    data = request.json
    color_low = tuple(data.get('color_low', [25, 60, 80]))  # Нижняя граница HSV
    color_high = tuple(data.get('color_high', [60, 255, 255]))  # Верхняя граница HSV
    action = data.get('action', 'draw_box')  # draw_box или crop
    image_url = data.get('image_url', '')
    print(color_low, color_high )
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')

    image = cv2.imread(image_path)
    if image is None:
        return jsonify({'error': 'Image not found'}), 400

    # Преобразуем изображение в HSV
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Создаем маску для указанного диапазона цветов
    only_object = cv2.inRange(hsv_img, color_low, color_high)

    # Находим контуры
    contours, _ = cv2.findContours(only_object, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return jsonify({'error': 'No object found with the specified color range'}), 400

    # Берем самый большой контур
    largest_contour = max(contours, key=cv2.contourArea)

    # Определяем ограничивающий прямоугольник
    x, y, w, h = cv2.boundingRect(largest_contour)

    if action == 'crop':
        # Обрезаем изображение по найденным координатам
        cropped_image = image[y:y+h, x:x+w]
        result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
        cv2.imwrite(result_path, cropped_image)
        return jsonify({'result_url': f'/static/uploads/preview.jpg', 'coordinates': [x, y, w, h]})
    else:
        # Рисуем ограничивающую рамку
        output_image = image.copy()
        cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
        cv2.imwrite(result_path, output_image)
        return jsonify({'result_url': f'/static/uploads/preview.jpg', 'coordinates': [x, y, w, h]})
    
    
@app.route('/threshold', methods=['POST'])
def apply_threshold():
    data = request.json
    threshold_value = int(data.get('threshold_value', 127))
    max_value = int(data.get('max_value', 255))
    threshold_type = data.get('threshold_type', 'binary')
    image_url = data.get('image_url', '')

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return jsonify({'error': 'Image not found'}), 400

    # Определяем тип порога
    if threshold_type == 'binary':
        thresh_type = cv2.THRESH_BINARY
    elif threshold_type == 'binary_inv':
        thresh_type = cv2.THRESH_BINARY_INV
    elif threshold_type == 'trunc':
        thresh_type = cv2.THRESH_TRUNC
    elif threshold_type == 'tozero':
        thresh_type = cv2.THRESH_TOZERO
    elif threshold_type == 'tozero_inv':
        thresh_type = cv2.THRESH_TOZERO_INV
    else:
        return jsonify({'error': 'Invalid threshold type'}), 400

    # Применяем пороговую обработку
    _, thresholded = cv2.threshold(image, threshold_value, max_value, thresh_type)

    thresholded_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    cv2.imwrite(thresholded_path, thresholded)

    return jsonify({'thresholded_url': f'/static/uploads/preview.jpg'})

@app.route('/adaptive_threshold', methods=['POST'])
def apply_adaptive_threshold():
    data = request.json
    max_value = int(data.get('max_value', 255))
    adaptive_method = data.get('adaptive_method', 'mean')
    threshold_type = data.get('threshold_type', 'binary')
    block_size = int(data.get('block_size', 11))
    constant = int(data.get('constant', 2))
    image_url = data.get('image_url', '')

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return jsonify({'error': 'Image not found'}), 400

    # Определяем метод адаптации
    if adaptive_method == 'mean':
        adapt_method = cv2.ADAPTIVE_THRESH_MEAN_C
    elif adaptive_method == 'gaussian':
        adapt_method = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
    else:
        return jsonify({'error': 'Invalid adaptive method'}), 400

    # Определяем тип порога
    if threshold_type == 'binary':
        thresh_type = cv2.THRESH_BINARY
    elif threshold_type == 'binary_inv':
        thresh_type = cv2.THRESH_BINARY_INV
    else:
        return jsonify({'error': 'Invalid threshold type'}), 400

    # Применяем адаптивную пороговую обработку
    thresholded = cv2.adaptiveThreshold(image, max_value, adapt_method, 
                                      thresh_type, block_size, constant)

    thresholded_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    cv2.imwrite(thresholded_path, thresholded)

    return jsonify({'thresholded_url': f'/static/uploads/preview.jpg'})

@app.route('/edge_detection', methods=['POST'])
def edge_detection():
    data = request.json
    method = data.get('method', 'canny')
    threshold1 = int(data.get('threshold1', 100))
    threshold2 = int(data.get('threshold2', 200))
    aperture_size = int(data.get('aperture_size', 3))
    sobel_kernel = int(data.get('sobel_kernel', 3))
    image_url = data.get('image_url', '')

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return jsonify({'error': 'Image not found'}), 400

    if method == 'canny':
        # Детектор границ Кэнни
        edges = cv2.Canny(image, threshold1, threshold2, apertureSize=aperture_size)
    elif method == 'sobel':
        # Оператор Собеля
        sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
        sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
        edges = cv2.magnitude(sobel_x, sobel_y)
        edges = cv2.normalize(edges, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    else:
        return jsonify({'error': 'Invalid edge detection method'}), 400

    edges_path = os.path.join(app.config['UPLOAD_FOLDER'], 'preview.jpg')
    cv2.imwrite(edges_path, edges)

    return jsonify({'edges_url': f'/static/uploads/preview.jpg'})

app.run(port=80)