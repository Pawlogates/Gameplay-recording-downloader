from flask import Flask, request, send_from_directory, Response, jsonify
import os
import zipfile
import io
import hashlib

LEADERBOARD_FOLDER = "leaderboard"
os.makedirs(LEADERBOARD_FOLDER, exist_ok=True)

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/leaderboard/list')
def leaderboard_list():
	result = {}

	for filename in os.listdir(LEADERBOARD_FOLDER):
		path = os.path.join(LEADERBOARD_FOLDER, filename)

		if os.path.isfile(path):
			with open(path, "rb") as f:
				result[filename] = hashlib.sha256(f.read()).hexdigest()

	return jsonify(result)


@app.route('/leaderboard/<filename>')
def leaderboard_file(filename):
	return send_from_directory(LEADERBOARD_FOLDER, filename)

# -------------------------
# Upload endpoint
# -------------------------
@app.route('/upload', methods=['POST'])
def upload():
	if 'file' not in request.files:
        return 'No file part', 400

    f = request.files['file']
    filename = f.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    f.save(file_path)

    print(f"✅ File received: {filename}")
    return f"Uploaded {filename}", 200


# -------------------------
# Serve individual files
# -------------------------
@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# -------------------------
# Download ALL files as ZIP
# -------------------------
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


# -------------------------
# Hash of ALL files (change detection)
# -------------------------
@app.route('/zip-hash')
def zip_hash():
    hash_obj = hashlib.sha256()

    # Sort ensures consistent hash order
    for filename in sorted(os.listdir(UPLOAD_FOLDER)):
        path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(path):
            with open(path, "rb") as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    hash_obj.update(chunk)

    return jsonify({"hash": hash_obj.hexdigest()})


# -------------------------
# Optional: list files + hashes
# -------------------------
@app.route('/list')
def list_files():
    result = {}
    for filename in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(path):
            with open(path, "rb") as f:
                result[filename] = hashlib.sha256(f.read()).hexdigest()
    return jsonify(result)


# -------------------------
# Health check
# -------------------------
@app.route('/')
def home():
    return 'Server is running!'


# -------------------------
# Run server
# -------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
