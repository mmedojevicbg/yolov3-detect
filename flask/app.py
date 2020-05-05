import os
import urllib.request
import glob
import time
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from flask_basicauth import BasicAuth

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = '/home/flask/static/uploads'
app = Flask(__name__)
Bootstrap(app)
app.secret_key = "fwfhijwek13213g"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

available_weights = glob.glob("/home/yolov3/weights/*.pt")
for i, s in enumerate(available_weights):
    available_weights[i] = os.path.splitext(os.path.basename(s))[0]

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html', weights = available_weights)

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			weights_file = request.values.get('weights_file')
			filename = secure_filename(file.filename)
			filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(filepath)
			detect_cmd = 'cd /home/yolov3 && python3 detect.py --source ' + filepath + ' --cfg cfg/' + weights_file + '.cfg'
			detect_cmd = detect_cmd + ' --weights weights/' + weights_file + '.pt'
			detect_cmd = detect_cmd + ' --output /home/flask/static/uploads/output'
			os.system(detect_cmd)
			os.system('mv /home/yolov3/output/* /home/flask/static/uploads/output')

			return render_template("image.html", filename = filename, current_time = time.time())
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return redirect(request.url)

if __name__ == "__main__": 
	app.run(host ='0.0.0.0', port = 80, debug = True) 

