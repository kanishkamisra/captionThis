from flask import Flask, send_file, render_template, request
from werkzeug.utils import secure_filename
from clarifai.rest import ClarifaiApp


app = ClarifaiApp("wLADJynVIqVNlpuUhS45MHkBoQ4C4RYrHqlOrLhI", "L23m2pfhwOjamIX0GCfOimH3JHDQcCx23HMnk4eR")

# get the general model
model = app.models.get("general-v1.3")

# predict with the model



app = Flask(__name__)


@app.route("/")
def index():
    print model.predict_by_url(url='https://samples.clarifai.com/metro-north.jpg')
    return send_file("views/index.html")


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
