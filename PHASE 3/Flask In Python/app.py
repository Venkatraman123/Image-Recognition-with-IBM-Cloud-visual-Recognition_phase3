from flask import Flask, render_template, request
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

app = Flask(__name__)

# IBM Visual Recognition credentials
api_key = 9vB-X3UL2OMKso53BzGxdWu6dM20Q5p3JWy67RzuLyzV
service_url = {
	"https://api.au-syd.assistant.watson.cloud.ibm.com/instances/ca87a79a-64e6-44f8-9218-0fa1166b91ae"
}

authenticator = IAMAuthenticator(api_key)
visual_recognition = VisualRecognitionV3(
    version='2018-03-19',
    authenticator=authenticator
)
visual_recognition.set_service_url(service_url)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    # Upload the image to Visual Recognition
    with open(file.filename, 'rb') as image_file:
        classes = visual_recognition.classify(
            images_file=image_file,
            threshold='0.6'
        ).get_result()

        # Extract class names from the response
        image_classes = [cls['class'] for cls in classes['images'][0]['classifiers'][0]['classes']]

    return render_template('result.html', image_classes=image_classes)

if __name__ == '__main__':
    app.run(debug=True)
