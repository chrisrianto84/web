from app import app
from flask import render_template, Response, redirect, url_for, request, flash
import pyaudio
from datetime import datetime
import uuid
from app_settings import settings
import matplotlib
matplotlib.use('Agg')

SECRET_KEY = str(datetime.now).encode('utf8')
app.secret_key = SECRET_KEY

r = settings.get_redis_config()

upload_folder = 'app/static/user_input/input_audio/'
allowed_extensions = set(['mp3','wav'])
app.config['UPLOAD_FOLDER'] = upload_folder

rec_status = False

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in allowed_extensions

@app.route('/ping')
def index():
    return "pong"

@app.route('/')
@app.route('/home')
def home():
    ids = str(uuid.uuid1())
    r.set('session_id:',ids)
    from backend import clear_dir
    clear_dir.initiate_clear()
    return render_template('index.html', title='Landing Page')

@app.route('/chordRecognition', methods=['GET','POST'])
def chordRecognition():
    from backend import clear_dir

    # if request.method != "POST":
    #     clear_dir.initiate_clear()

    from subprocess import Popen, PIPE
    if request.method=="POST":
        for a in request.form:
            status = a
        
        print("Incoming Request for:", status)
        if status == 'select_file':
            if 'audio_file' not in request.files:
                flash('No file part')
                return render_template('chordRecognition.html', value='4')

            if "audio_file" in request.files:
                import os
                from werkzeug.utils import secure_filename
                file = request.files['audio_file']

                if not allowed_file(file.filename):
                    return render_template('chordRecognition.html', value='4')
                if file.filename == '':
                    flash('No selected file')
                    return render_template('chordRecognition.html', value='4')

                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename)))
                    r.set('input_file:',filename)
                    return redirect(url_for('output'))

        elif status == 'record_status':
            if request.form[status] == '2':
                global process 
                process = Popen(['python3 app/record.py'], stdin=PIPE, shell=True)
                return render_template('chordRecognition.html', value='2')
            elif request.form[status] == '3':
                from signal import SIGINT      
                from flask import Markup
                from backend import train
                import time

                process.send_signal(SIGINT)
                process.wait
                # filename = process.communicate()[0].decode("utf-8")
                # print(filename)
                time.sleep(5)
                train.getOnset(1)

                # r.set('input_file:', filename)
                
                return redirect(url_for('output'))
            else:
                flash('No selected file')
                # return redirect(request.url)
    return render_template('chordRecognition.html', title='Chord Recognition', value='1')

@app.route('/about')
def about():
    from backend import clear_dir
    clear_dir.initiate_clear()
    return render_template('about.html', title='About')

@app.route('/testing/upload')
def testingUpload():
    return render_template('uploads.html', title='TestingUpload')

@app.route('/output')
def output():
    from backend import make_mfcc, model_prediction

    filename = r.get('input_file:')
    print('b')
    print(filename)
    make_mfcc.make_visualization()

    string_output = model_prediction.get_prediction()

    return render_template('output.html', filename=filename, string_output = string_output)


