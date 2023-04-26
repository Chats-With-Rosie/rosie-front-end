import os
import requests
from gtts import gTTS
from flask import Flask, request, jsonify, render_template
from pydub import AudioSegment
from pydub.playback import play
from playsound import playsound
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

def get_most_recent_image():
    #FIX THIS TO DISPLAY IMAGE
    # files = os.listdir(app.config['UPLOAD_FOLDER'])
    # if not files:
    #     return None
    # files = [f for f in files if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    # if not files:
    #     return None
    # return os.path.join(app.config['UPLOAD_FOLDER'], max(files, key=os.path.getctime))
    return "/static/uploads/aaa.png"

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
def send_audio_to_endpoint(audio_filename, endpoint_url):
    audio_filepath = os.path.abspath(audio_filename)

    if not os.path.exists(audio_filepath):
        print("Error: audio file not found.")
        return None

    with open(audio_filepath, 'rb') as audio_file:
        files = {'file': (audio_filename, audio_file, 'audio/wav')}
        response = requests.post(endpoint_url, files=files)

    if response.status_code == 200:
        print("Audio file sent successfully!")
        print(f"Response content: {response.content}")
        return response.json()["response"]
    else:
        print(f"Error sending audio file. Status code: {response.status_code}")
        return None

def text_to_speech(text, endpoint_url):
    # Set language to English
    language = 'en'

    # Create gTTS object and save audio file to disk
    tts = gTTS(text=text, lang=language)
    tts.save("static/uploads/speak.wav")
    
@app.route('/speak', methods=['POST'])
def think():
    data_string = request.json.get('data')
    endpoint_url = os.environ.get('FRONT_END_AUDIO_URL')
    if data_string:
        print(f"Received string: {data_string}")
        response = data_string
        text_to_speech(data_string, endpoint_url)
        return jsonify({"response": response})
    else:
        return jsonify({"result": "error", "message": "No data received"}), 400


if __name__ == '__main__':
    app.run(debug=True)