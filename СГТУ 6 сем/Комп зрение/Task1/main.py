from flask import Flask, render_template, request, jsonify, url_for, redirect, send_from_directory # Импортируем необходимые модули Flask. Добавлены ⓃredirectⓃ и Ⓝsend_from_directoryⓃ
import cv2  # Для обработки изображений
import numpy as np  # Для числовых операций (хотя в этом коде не используется напрямую)
import os  # Для работы с файловой системой
import base64  # Для кодирования данных изображения
from werkzeug.utils import secure_filename  # Для безопасной обработки имен файлов

# Инициализация приложения Flask
app = Flask(__name__) 
app.config['UPLOAD_FOLDER'] = 'uploads'  # Задаем директорию для загрузок
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Задаем максимальный размер загружаемого файла (16MB)

# Создаем директорию для загрузок, если она не существует
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Разрешенные расширения файлов изображений
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tiff'}

# Функция для проверки, имеет ли файл разрешенное расширение
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Маршрут для главной страницы (GET и POST запросы)
@app.route('/', methods=['GET', 'POST'])
def index():
    uploaded_filename = None  # Инициализируем переменную для имени файла
    if request.method == 'POST':
        if 'file' not in request.files: # Проверяем, был ли загружен файл
            return redirect(request.url) # Перенаправляем обратно на ту же страницу, если файла нет
        file = request.files['file']
        if file.filename == '': # Проверяем, пустое ли имя файла
            return redirect(request.url) # Перенаправляем, если имя файла пустое
        if file and allowed_file(file.filename): # Проверяем тип файла
            filename = secure_filename(file.filename) # Делаем имя файла безопасным
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename) # Создаем полный путь к файлу
            file.save(filepath) # Сохраняем загруженный файл
            uploaded_filename = filename # Сохраняем имя файла для отображения в шаблоне

    return render_template('index.html', uploaded_filename=uploaded_filename) # Рендерим шаблон и передаем имя файла


# Маршрут для обслуживания загруженных файлов
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename) # Отправляем файл из директории загрузок


# Маршрут для изменения размера изображения (POST запрос)
@app.route('/resize/<filename>', methods=['POST'])
def resize(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        img = cv2.imread(filepath)
        if img is None:
            return jsonify({'error': 'Could not read image'}), 501
        print(4)

        img = workWithSize(img)  # Your image resizing function
        print(5)
        _, buffer = cv2.imencode('.jpg', img)
        img_str = base64.b64encode(buffer).decode('utf-8')
        return jsonify({'image': img_str})

    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404  # Specific error for file not found
    except Exception as e:
        return jsonify({'error': str(e), 'details':str(type(e))}), 500  # Generic error handling with details

def workWithSize(img):
        width = int(request.form['width']) # Получаем ширину из запроса
        height = int(request.form['height']) # Получаем высоту из запроса
        interpolation = request.form.get('interpolation', 'bicubic') # Получаем метод интерполяции, по умолчанию бикубический
        resized = cv2.resize(img, (width, height), interpolation={ # Изменяем размер изображения
            'nearest': cv2.INTER_NEAREST,
            'bilinear': cv2.INTER_LINEAR,
            'bicubic': cv2.INTER_CUBIC
        }.get(interpolation, cv2.INTER_CUBIC))
        return resized

@app.route('/slice/<filename>', methods=['POST'])
def workWithSlice(filepath):
        img = cv2.imread(filepath)
        if img is None:
            return jsonify({'error': 'Could not read image'}), 501
        print(4)
        xl = int(request.form['xl']) # Получаем ширину из запроса
        xr = int(request.form['xr']) # Получаем ширину из запроса
        yl = int(request.form['yl']) # Получаем ширину из запроса
        yr = int(request.form['yr']) # Получаем ширину из запроса
        
        img =  img[yl:yr, xl:xr]
        _, buffer = cv2.imencode('.jpg', img) # Кодируем измененное изображение в формат JPEG
        img_str = base64.b64encode(buffer).decode('utf-8') # Кодируем изображение в строку base64
        return jsonify({'image': img_str}) 

app.run(port=80)