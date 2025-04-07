from flask import Flask, request, send_from_directory
import os
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part', 400
    f = request.files['file']
    filename = f.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    f.save(file_path)

    # Log filename explicitly using Flask logging
    app.logger.info(f"✅ File received: {filename}")

    return f"Uploaded {filename}", 200


@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/')
def home():
    return 'Server is running!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)