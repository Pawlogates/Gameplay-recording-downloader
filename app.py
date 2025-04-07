from flask import Flask, request
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part', 400
    f = request.files['file']
    f.save(os.path.join(UPLOAD_FOLDER, f.filename))
    return 'File uploaded', 200

@app.route('/')
def home():
    return 'Server is running!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
