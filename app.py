from flask import Flask, request, send_from_directory
import os
import requests

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
	return 'Server is running!'

@app.route('/upload', methods=['POST'])
def upload():
	if 'file' not in request.files:
		return 'No file part', 400
	f = request.files['file']
	filename = f.filename
	filepath = os.path.join(UPLOAD_FOLDER, filename)
	f.save(filepath)

	# 🔁 Send file to your PC
	try:
		with open(filepath, 'rb') as file_data:
			resp = requests.post(
				'http://YOUR_PC_PUBLIC_IP:5001/receive',  # 🔁 Replace this!
				files={'file': (filename, file_data)}
			)
			print(f"Sent file to PC: {resp.status_code}")
	except Exception as e:
		print(f"Error sending to PC: {e}")

	return 'File uploaded and forwarded', 200

@app.route('/uploads/<filename>')
def serve_file(filename):
	return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=10000)