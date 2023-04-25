from flask import Flask, request, jsonify, render_template 
import shutil
import os
import requests

import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/'

def get_most_recent_image():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    if not files:
        return None

    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    files = [f for f in files if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f)) and any(ext in f.lower() for ext in image_extensions)]
    if not files:
        return None
    return os.path.join(app.config['UPLOAD_FOLDER'], max(files, key=lambda f: os.path.getctime(os.path.join(app.config['UPLOAD_FOLDER'], f))))


@app.route('/', methods=['GET'])
def index():
    image_path = get_most_recent_image()
    return render_template('index.html', image_path=image_path)

@app.route('/upload', methods=['POST'])
def upload():
    image_url = request.json.get('image_url')
    print(image_url)

    image_data = requests.get(image_url).content
    filename = "image.jpg"  # Save the downloaded image as 'image.jpg'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    with open(filepath, 'wb') as output_file:
        output_file.write(image_data)

    response = requests.get(image_url, stream=True)

    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)

        url = request.host_url + app.config['UPLOAD_FOLDER'] + '/' + filename
        return jsonify({'url': url}), 200
    else:
        return jsonify({'error': 'failed to download image'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5069)
