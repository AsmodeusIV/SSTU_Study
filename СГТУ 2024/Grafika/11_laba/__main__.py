from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

with open("index.html", "r") as f:
    html = f.read()

print(html)

if __name__ == '__main__':
    #app.run()
    pass