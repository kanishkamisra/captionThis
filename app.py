import os
from twython import Twython

from flask import Flask, render_template, request
from flask import send_from_directory
from werkzeug.utils import secure_filename
from clarifai.rest import ClarifaiApp, Image as ClImage
from captionize import captionize

# Initialize ClarifaiAPI
app = ClarifaiApp("wLADJynVIqVNlpuUhS45MHkBoQ4C4RYrHqlOrLhI", "L23m2pfhwOjamIX0GCfOimH3JHDQcCx23HMnk4eR")

# Get the general model
model = app.models.get("general-v1.3")

app = Flask(__name__)

# Set directory to store images
UPLOAD_FOLDER = '/Users/vishnutadimeti/Developer/Python/captionThis/static'
# UPLOAD_FOLDER = 'C:/Users/Kanishka/captionThis/static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

twitter_photo = "name"

twitter = Twython("mcBrpMgySLjb866aTA4Sr3EbC",
                  "BB0o45dYYKSIQOyK5UyiMVUOKukXdKoN6ko2htRuROam44pbTX",
                  "215693554-gZg3b3I5NBIRfHkcq8O9om75RlIrP5ZAn3O2DuE9",
                  "mDxlFjvno3A1aKsYfOyA8sG0cTehYEMMSuq2MFnsbXeGX")


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

        print "The filename of the image uploaded is: " + filename

        # Save file to the directory
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Predict the uploaded image using Clarifai
        # test_image = ClImage(
        #     file_obj=open(UPLOAD_FOLDER + '/' + filename, 'rb'))
        # print model.predict([test_image])
        # filename = 'lake.jpg'
        # print(captionize(UPLOAD_FOLDER + '/' + filename))

        captions = [
                    'You can make your card-action always visible']

        # Return the template display.html to render, and the filename of the image saved
        return render_template('display.html', image_name=filename, captionlist = captions)


# @app.route('/photo', methods=['GET', 'POST'])
# def post_twitter():
#     print "Name of the photo: " + twitter_photo
#     photo = open(UPLOAD_FOLDER + "/" + twitter_photo, 'rb')
#     response = twitter.upload_media(media=photo)
#     twitter.update_status(status='Checkout this cool image!', media_ids=[response['media_id']])
#     return twitter_photo


@app.route('/display/<filename>', methods=['GET', 'POST'])
def send_file(filename):
    photo = open(UPLOAD_FOLDER + "/" + filename, 'rb')
    response = twitter.upload_media(media=photo)
    twitter.update_status(status='Checkout this cool image!', media_ids=[response['media_id']])
    return render_template('home.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1')
