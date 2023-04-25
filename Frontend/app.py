from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

def get_most_recent_image():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    if not files:
        return None
    files = [f for f in files if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    if not files:
        return None
    return os.path.join(app.config['UPLOAD_FOLDER'], max(files, key=os.path.getctime))

@app.route('/', methods=['GET'])
def index():
    image_path = get_most_recent_image()
    return render_template('index.html', image_path=image_path)

@app.route('/upload', methods=['POST'])
def upload():
    # check if the POST request has an image
    if 'image' not in request.files:
        return jsonify({'error': 'no image found'})
    
    # save the image to the uploads directory
    image = request.files['image']
    filename = image.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)
    
    # return the URL of the uploaded image
    url = request.host_url + app.config['UPLOAD_FOLDER'] + '/' + filename
    return jsonify({'url': url})

if __name__ == '__main__':
    app.run(debug=True)
