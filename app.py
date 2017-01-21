from flask import Flask, send_file, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route("/")
def index():
    return send_file("views/index.html")


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
