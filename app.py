from flask import Flask, render_template, request, redirect, url_for
import os
from models.image_model import detect_image_fake
from models.text_model import detect_text_fake
from models.video_model import detect_video_fake
from utils.metadata_checker import check_metadata

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'media' not in request.files:
        return redirect(request.url)
    
    file = request.files['media']
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        file_ext = file.filename.rsplit('.', 1)[1].lower()

        if file_ext in ['jpg', 'jpeg', 'png']:
            score, explanation = detect_image_fake(filepath)
        elif file_ext in ['mp4', 'avi']:
            score, explanation = detect_video_fake(filepath)
        elif file_ext == 'txt':
            score, explanation = detect_text_fake(filepath)
        else:
            score, explanation = (0, "Unsupported file type.")

        metadata_report = check_metadata(filepath)

        return render_template('results.html',
                               filename=file.filename,
                               score=score,
                               explanation=explanation,
                               metadata=metadata_report)

    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host="0.0.0.0",port=1000,debug=True)
