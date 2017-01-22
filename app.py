import os

from flask import Flask, send_file, render_template, request, redirect
from flask import send_from_directory
from flask import url_for
from werkzeug.utils import secure_filename
from clarifai.rest import ClarifaiApp

app = ClarifaiApp("wLADJynVIqVNlpuUhS45MHkBoQ4C4RYrHqlOrLhI", "L23m2pfhwOjamIX0GCfOimH3JHDQcCx23HMnk4eR")

# get the general model
model = app.models.get("general-v1.3")

app = Flask(__name__)

UPLOAD_FOLDER = '/Users/vishnutadimeti/Developer/Python/captionThis/static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template('home.html')


@app.route('/display', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        print filename
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # return render_template('display.html')
        # return redirect(url_for('uploaded_file',
        #                         filename=filename))
        filename = 'http://0.0.0.0:5000/static/' + filename
        print filename
    return render_template('display.html', filename=filename)
        # return render_template('display.html')


# @app.route('/show')
# def uploaded_file(filename):
#     filename = 'http://0.0.0.0:5000/static/' + filename
#     print filename
#     return render_template('display.html', filename=filename)


# @app.route('/static/<filename>')
# def send_file(filename):
#     return send_from_directory(UPLOAD_FOLDER, filename)


# @app.route('/<filename>')
# def uploaded_file(filename):
#     # return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
#     return render_template('display.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
