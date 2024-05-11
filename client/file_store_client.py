import requests
import os
import argparse

SERVER_URL = 'http://127.0.0.1:5002'

def create_file(file_name):
    with open(file_name, 'w') as f:
        f.write('')  # Create an empty file

def add_files(files):
    existing_files = list_files()
    files_to_send = []
    for file_path in files:
        if not os.path.exists(file_path):
            create_file(file_path)
            print(f"File '{file_path}' created.")
        if os.path.basename(file_path) in existing_files:
            print(f"File '{file_path}' already exists on the server. Skipping...")
            continue
        files_to_send.append(('files', (os.path.basename(file_path), open(file_path, 'rb'))))
    if not files_to_send:
        print("No valid files to send.")
        return
    response = requests.post(f'{SERVER_URL}/add', files=files_to_send)
    if response.status_code == 200:
        print(response.json().get('message', ''))
    else:
        print("Failed to add files.")
        print(response.text)

def list_files():
    response = requests.get(f'{SERVER_URL}/ls')
    if response.status_code == 200:
        files = response.json().get('files', [])
        print("Files on server:")
        for file in files:
            print(file)
        return files
    else:
        print("Failed to list files.")
        print(response.text)
        return []

def remove_file(file_name='file1.txt'):
    try:
        print(f'{SERVER_URL}/rm/{file_name}')
        response = requests.delete(f'{SERVER_URL}/rm/{file_name}')
        if response.status_code == 200:
            print(response.json().get('message', ''))
        else:
            print(f"Failed to remove file '{file_name}'. Status code: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to the server: {e}")

def update_file(file_name):
    if not os.path.exists(file_name):
        print(f"File '{file_name}' does not exist.")
        return
    file_to_send = {'file': open(file_name, 'rb')}
    response = requests.put(f'{SERVER_URL}/update/{file_name}', files=file_to_send)
    if response.status_code == 200:
        print(response.json().get('message', ''))
    else:
        print(f"Failed to update file '{file_name}'.")
        print(response.text)

def word_count():
    response = requests.get(f'{SERVER_URL}/wc')
    if response.status_code == 200:
        word_count = response.json().get('word_count', 0)
        print(f"Total word count in all files: {word_count}")
    else:
        print("Failed to get word count.")
        print(response.text)

def frequent_words(limit=10, order='asc'):
    response = requests.get(f'{SERVER_URL}/freq-words?limit={limit}&order={order}')
    if response.status_code == 200:
        frequent_words = response.json().get('frequent_words', [])
        print(f"Most frequent words:")
        for word, count in frequent_words:
            print(f"{word}: {count}")
    else:
        print("Failed to get frequent words.")
        print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='File Store Client')
    parser.add_argument('command', help='Command (add, ls, rm, update, wc, freq-words)')
    parser.add_argument('files', nargs='*', help='List of files (for add command)')
    parser.add_argument('--file', help='File name (for rm, update commands)')
    parser.add_argument('--limit', type=int, default=10, help='Limit for frequent words (for freq-words command)')
    parser.add_argument('--order', choices=['asc', 'dsc'], default='asc', help='Order for frequent words (for freq-words command)')
    parser.add_argument('--infile', help='Input file to print out')
    args = parser.parse_args()

    command = args.command
    files = args.files
    #print(args)
    #print(files)# Loop through each file for removal
        
    file_name = args.files
    limit = args.limit
    order = args.order

    if command == 'add':
        add_files(files)
    elif command == 'ls':
        list_files()
    elif command == 'rm' and files:
        for file in files:
            remove_file(file)
    elif command == 'update' and files:
        for file in files:
            update_file(file)
    elif command == 'wc':
        word_count()
    elif command == 'freq-words':
        frequent_words(limit, order)