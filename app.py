import os
import re
import shutil
import subprocess
import http.server
import socketserver
import threading
import requests
from flask import Flask
import json
import time
import base64

app = Flask(__name__)

# Set environment variables
FILE_PATH = os.environ.get('FILE_PATH', './files')
PROJECT_URL = os.environ.get('URL', '')
INTERVAL_SECONDS = int(os.environ.get("TIME", 120)) 
UUID = os.environ.get('UUID', '3d3ecd10-381d-3224-9570-3f0b7df524d3')  
ARGO_AUTH = os.environ.get('ARGO_AUTH', '')            
ARGO_PORT = int(os.environ.get('ARGO_PORT', '8080'))  
PORT = int(os.environ.get('SERVER_PORT') or os.environ.get('PORT') or 3000)

# Create directory if it doesn't exist
if not os.path.exists(FILE_PATH):
    os.makedirs(FILE_PATH)
    print(f"{FILE_PATH} has been created")
else:
    print(f"{FILE_PATH} already exists")

# Clean old files
paths_to_delete = ['mouse.json']
for file in paths_to_delete:
    file_path = os.path.join(FILE_PATH, file)
    try:
        os.unlink(file_path)
        print(f"{file_path} has been deleted")
    except Exception as e:
        print(f"Skip Delete {file_path}")


# http server
class MyHandler(http.server.SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, world')
        
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')

httpd = socketserver.TCPServer(('', PORT), MyHandler)
server_thread = threading.Thread(target=httpd.serve_forever)
server_thread.daemon = True
server_thread.start()

# Download and run files
def download_files_and_run():
    

    # Authorize and run
    files_to_authorize = ['./cat', './dog']
    authorize_files(files_to_authorize)
    
    # Generate configuration file
    config ={"log":{"access":"/dev/null","error":"/dev/null","loglevel":"none",},"inbounds":[{"port":ARGO_PORT ,"listen":"0.0.0.0","protocol":"vless","settings":{"clients":[{"id":UUID }],"decryption":"none"},"streamSettings":{"network":"ws","wsSettings":{"path":"/vle123"}}}],"outbounds":[{"protocol":"freedom","settings": {}}]}
    with open(os.path.join(FILE_PATH, 'mouse.json'), 'w', encoding='utf-8') as config_file:
        json.dump(config, config_file, ensure_ascii=False, indent=2)
       
    # Run xr-ay
    command1 = f"nohup {FILE_PATH}/cat -c {FILE_PATH}/mouse.json >/dev/null 2>&1 &"
    try:
        subprocess.run(command1, shell=True, check=True)
        print('cat is running')
        subprocess.run('sleep 1', shell=True)  # Wait for 1 second
    except subprocess.CalledProcessError as e:
        print(f'cat running error: {e}')

    # Run cloud-fared
    if os.path.exists(os.path.join(FILE_PATH, 'dog')):
	# Get command line arguments for cloud-fared
        if not re.match(r'^[A-Z0-9a-z=]{120,250}$', ARGO_AUTH):
            print("ARGO_AUTH variable is empty")
            return
        else:
            args = f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 run --token {ARGO_AUTH}"

        try:
            subprocess.run(f"nohup {FILE_PATH}/dog {args} >/dev/null 2>&1 &", shell=True, check=True)
            print('dog is running')
            subprocess.run('sleep 2', shell=True)  # Wait for 2 seconds
        except subprocess.CalledProcessError as e:
            print(f'Error executing command: {e}')

    subprocess.run('sleep 3', shell=True)  # Wait for 3 seconds


# Authorize files
def authorize_files(file_paths):
    new_permissions = 0o775

    for relative_file_path in file_paths:
        absolute_file_path = os.path.join(FILE_PATH, relative_file_path)
        try:
            os.chmod(absolute_file_path, new_permissions)
            print(f"Empowerment success for {absolute_file_path}: {oct(new_permissions)}")
        except Exception as e:
            print(f"Empowerment failed for {absolute_file_path}: {e}")



download_files_and_run()


# auto visit project page
has_logged_empty_message = False

def visit_project_page():
    try:
        if not PROJECT_URL or not INTERVAL_SECONDS:
            global has_logged_empty_message
            if not has_logged_empty_message:
                print("Hello Flask")
                has_logged_empty_message = True
            return

        response = requests.get(PROJECT_URL)
        response.raise_for_status() 

        # print(f"Visiting project page: {PROJECT_URL}")
        print("Page visited successfully")
        print('\033c', end='')
    except requests.exceptions.RequestException as error:
        print(f"Error visiting project page: {error}")

if __name__ == "__main__":
    while True:
        visit_project_page()
        time.sleep(INTERVAL_SECONDS)