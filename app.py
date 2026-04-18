from flask import Flask, request, send_from_directory
import os

import zipfile
from flask import Response
import io

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

    # Explicitly print to stdout for Render logs
    print(f"✅ File received: {filename}")  # This should now show in the logs

    return f"Uploaded {filename}", 200

@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/download-all')
def download_all():
    memory_file = io.BytesIO()

    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                zf.write(file_path, arcname=filename)

    memory_file.seek(0)

    return Response(
        memory_file,
        mimetype='application/zip',
        headers={
            'Content-Disposition': 'attachment; filename=all_replays.zip'
        }
    )

@app.route('/')
def home():
    return 'Server is running!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
