import os
import requests
import openai
from gtts import gTTS
from flask import Flask, request, jsonify, render_template, send_file
from pydub import AudioSegment
from pydub.playback import play
from playsound import playsound
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def transcribe(audio_output_file_path, openAI_API_key):
    openai.api_key = openAI_API_key

    with open(audio_output_file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

    transcribed_text = transcript['text']
    return transcribed_text

def send_string_to_endpoint(endpoint, text):
    try:
        response = requests.post(endpoint, json={'data': text})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Failed to send string to endpoint: {e}')
        return False
    except ValueError as e:
        print(f'Response body is not valid JSON: {e}')
        return False
    return True

@app.route('/get-audio-timestamp')
def get_audio_timestamp():
    audio_file_path = 'static/uploads/speak.wav'
    if os.path.exists(audio_file_path):
        last_modified = os.path.getmtime(audio_file_path)
        return {'timestamp': last_modified}
    return {'timestamp': None}, 404

@app.route('/upload-image', methods=['POST'])
def image_handler():
    # Get the URL of the image from the request JSON payload
    try:
        image_url = request.json.get('image_url')
        if not image_url:
            raise ValueError('Invalid request: missing image_url field')
    except ValueError as e:
        return str(e), 400

    # Download the image from the specified URL
    response = requests.get(image_url)
    if response.status_code != 200:
        return 'Failed to download image file', 500

    # Save the image to the static/uploads directory, overwriting any existing images with the same name
    image_filename = "image_to_display.jpg"
    image_filepath = os.path.join('static', 'uploads', image_filename)
    with open(image_filepath, 'wb') as f:
        f.write(response.content)

    # Return a success message
    return 'Image file saved successfully', 200

@app.route('/upload-audio-to-self', methods=['POST'])
def speech_to_text():
    # Define the path to where the audio file should be saved
    audio_output_file_path = 'static/uploads/audio_file.wav'

    # Retrieve OpenAI API key and Think endpoint from environment variables
    openAI_API_key = os.environ.get('OPENAI_API_KEY') or "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"
    think_endpoint = os.environ.get('THINK_SERVICE') or "http://think_service:5080/think"

    # Check if the audio_url field is present in the request JSON payload
    if 'file' not in request.files:
        return 'No file part in the request', 400
    audio_file = request.files['file']
    if not audio_file:
        return 'No file selected for upload', 400

    # Download the audio file from the specified URL
    audio_file.save(audio_output_file_path)
    # Save the downloaded audio file to disk
    
    
    # Transcribe the audio file using OpenAI and send the query to the Think endpoint
    query_for_think = transcribe(audio_output_file_path, openAI_API_key)
    send_string_to_endpoint(think_endpoint, query_for_think)
    
    # Return a success message
    return 'Audio file saved successfully', 200
    

@app.route('/rosie-speak', methods=['POST'])
def text_to_speech():
    try:
        data_string = request.json.get('data')
        if not data_string:
            raise ValueError('Invalid request: missing data field')
    except ValueError as e:
        return str(e), 400

    language = request.args.get('lang', 'en')

    tts = gTTS(text=data_string, lang=language)
    tts.save("static/uploads/speak.wav")

    return jsonify({"response": "Audio file saved successfully"}), 200
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
