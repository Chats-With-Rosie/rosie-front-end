from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, world!'

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['audio']
    if file and file.filename.endswith('.wav'):
        # Save the file to disk
        file.save(file.filename)
        return jsonify({'message': 'File uploaded successfully.'}), 200
    else:
        return jsonify({'error': 'Invalid file format.'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8082)

