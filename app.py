import os

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from clarifai.rest import ClarifaiApp

app = ClarifaiApp("wLADJynVIqVNlpuUhS45MHkBoQ4C4RYrHqlOrLhI", "L23m2pfhwOjamIX0GCfOimH3JHDQcCx23HMnk4eR")

# Get the general model
model = app.models.get("general-v1.3")

app = Flask(__name__)

# Set directory to store images
UPLOAD_FOLDER = '/Users/vishnutadimeti/Developer/Python/captionThis/static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template('home.html')


@app.route('/display', methods=['GET', 'POST'])
def upload_file():

    # Check if request method of the form is a POST
    if request.method == 'POST':
        f = request.files['file']
        # Create a filename of the file uploaded (Currently using the original name)
        filename = secure_filename(f.filename)
        print filename

        # Save file to the directory
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Return the template display.html to render, and the filename of the image saved
        return render_template('display.html', image_name=filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
