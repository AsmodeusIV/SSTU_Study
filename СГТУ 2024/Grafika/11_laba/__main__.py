from flask import Flask, render_template, request, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/resize')
def second():
    return render_template('resize.html')

@app.route('/convert')
def third():
    return render_template('convert.html')

@app.route('/resize', methods=['POST'])
def resize_image():
    if request.method == 'POST':
        image = request.files['image']
        width = int(request.form['width'])
        height = int(request.form['height'])

        image = Image.open(image)
        image = image.resize((width, height))
        image_filename = 'resized_image.jpg'
        image.save(image_filename)

        return send_file(image_filename, as_attachment=True)

@app.route('/convert', methods=['POST'])
def convert():
    image_file = request.files['image']
    image = Image.open(image_file)
    image = image.convert('L')

    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='converted-image.png')


if __name__ == '__main__':
    app.run()