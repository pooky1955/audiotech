import os
#import magic
import urllib.request
from flask import Flask, request
from werkzeug.utils import secure_filename
from util import extract_attention_video, INTERVAL
import json
from flask_cors import CORS
import time
import numpy as np

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./uploads"
CORS(app)

ALLOWED_EXTENSIONS = set(["mp4","webm"])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
def error(text):
    return text, 400


@app.route('/', methods=['POST'])
def upload_file():
    start = time.time()
    if request.method == 'POST':
    # check if the post request has the file part
        if 'video' not in request.files:
            return error("No file selected for uploading")

        video = request.files['video']
        if video.filename == '':
            return error('No file selected for uploading')
        if video and allowed_file(video.filename):
            filename = secure_filename(video.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            video.save(filepath)
            attention_nums = extract_attention_video(filepath)
            if attention_nums is None:
                return error("An error occured while playing the video")
            else:
                end = time.time()
                print(f"Took {end - start}")
                return json.dumps(dict(numbers=attention_nums,interval=INTERVAL,average=np.mean(attention_nums)))

        else:

            return error('Allowed file types are mp4')

if __name__ == "__main__":
    app.run(threaded=False)
