from flask import Flask, request, jsonify
import os
from collections import Counter
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'file_store_data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def file_exists(file_name):
    return os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], file_name))

@app.route('/add', methods=['POST'])
def add_file():
    uploaded_files = request.files.getlist('files')
    added_files = []
    for file in uploaded_files:
        file_name = secure_filename(file.filename)
        if file_exists(file_name):
            continue
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        added_files.append(file_name)
    if added_files:
        return jsonify({'message': f"Files added successfully: {added_files}"}), 200
    else:
        return jsonify({'message': 'No files added. Files already exist on the server.'}), 400

@app.route('/ls', methods=['GET'])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({'files': files}), 200

@app.route('/rm/<file_name>', methods=['DELETE'])
def remove_file(file_name):
    if file_exists(file_name):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        return jsonify({'message': f"File '{file_name}' removed successfully."}), 200
    else:
        return jsonify({'message': f"File '{file_name}' does not exist on the server."}), 404

@app.route('/update/<file_name>', methods=['PUT'])
def update_file(file_name):
    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return jsonify({'message': 'No file provided.'}), 400

    if file_exists(file_name):
        # Read the contents of the existing file on the server
        with open(os.path.join(app.config['UPLOAD_FOLDER'], file_name), 'r') as f:
            server_contents = f.read()

        # Read the contents of the uploaded file
        uploaded_contents = uploaded_file.read().decode('utf-8')  # Decode the byte string

        # Compare contents to see if an update is needed
        if uploaded_contents == server_contents:
            return jsonify({'message': f"File '{file_name}' on server already has the same contents."}), 200
        else:
            # Update the file on the server if contents are different
            with open(os.path.join(app.config['UPLOAD_FOLDER'], file_name), 'w') as f:
                f.write(uploaded_contents)
            return jsonify({'message': f"File '{file_name}' updated successfully."}), 200
    else:
        # Save the uploaded file to the server if it doesn't exist
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        return jsonify({'message': f"File '{file_name}' created and saved successfully."}), 200

@app.route('/wc', methods=['GET'])
def word_count():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    word_count = 0
    for file in files:
        with open(os.path.join(app.config['UPLOAD_FOLDER'], file), 'r') as f:
            word_count += len(f.read().split())
    return jsonify({'word_count': word_count}), 200

@app.route('/freq-words', methods=['GET'])
def frequent_words():
    limit = int(request.args.get('limit', 10))
    order = request.args.get('order', 'asc')

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    words = []
    for file in files:
        with open(os.path.join(app.config['UPLOAD_FOLDER'], file), 'r') as f:
            words.extend(f.read().split())

    word_counts = Counter(words)
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=(order == 'dsc'))

    return jsonify({'frequent_words': sorted_word_counts[:limit]}), 200

if __name__ == '__main__':
    app.run(debug=True,port=5002,host='0.0.0.0')