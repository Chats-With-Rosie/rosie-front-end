from flask import Flask, request, jsonify, render_template
import os
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['DATABASE'] = 'database.db'
app.config['SECRET_KEY'] = 'secretkey'

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.execute('CREATE TABLE IF NOT EXISTS images (filename TEXT)')
    conn.commit()
    return conn

def get_most_recent_image():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT filename FROM images ORDER BY rowid DESC LIMIT 1')
    result = cursor.fetchone()
    if result is None:
        return None
    filename = result[0]
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)

def save_image_to_db(filename):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO images VALUES (?)', (filename,))
    conn.commit()

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
    
    # save the filename to the database
    save_image_to_db(filename)
    
    # return the URL of the uploaded image
    url = request.host_url + app.config['UPLOAD_FOLDER'] + '/' + filename
    return jsonify({'url': url})

if __name__ == '__main__':
    app.run(debug=True)
