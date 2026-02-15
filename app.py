import os
import re
import json
import time
import asyncio
import platform
import subprocess
import threading
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

# Environment variables
FILE_PATH = os.environ.get('FILE_PATH', './files')   
UUID = os.environ.get('UUID', '3d3ecd10-381d-3224-9570-3f0b7df524d3')  
ARGO_AUTH = os.environ.get('ARGO_AUTH', '')            
ARGO_PORT = int(os.environ.get('ARGO_PORT', '8080'))   
PORT = int(os.environ.get('SERVER_PORT') or os.environ.get('PORT') or 3000) 

# Create running folder
def create_directory():
    print('\033c', end='')
    if not os.path.exists(FILE_PATH):
        os.makedirs(FILE_PATH)
        print(f"{FILE_PATH} is created")
    else:
        print(f"{FILE_PATH} already exists")


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Hello World')
                
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


# Authorize files with execute permission
def authorize_files(file_paths):
    for relative_file_path in file_paths:
        absolute_file_path = os.path.join(FILE_PATH, relative_file_path)
        if os.path.exists(absolute_file_path):
            try:
                os.chmod(absolute_file_path, 0o775)
                print(f"Empowerment success for {absolute_file_path}: 775")
            except Exception as e:
                print(f"Empowerment failed for {absolute_file_path}: {e}")

# Execute shell command and return output
def exec_cmd(command):
    try:
        process = subprocess.Popen(
            command, 
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        return stdout + stderr
    except Exception as e:
        print(f"Error executing command: {e}")
        return str(e)

# Download and run necessary files
async def download_files_and_run():
    global private_key, public_key
    
    # Authorize files
    files_to_authorize = ['cat', 'dog'] 
    authorize_files(files_to_authorize)
    
    # Generate configuration file
    config ={"log":{"access":"/dev/null","error":"/dev/null","loglevel":"none",},"inbounds":[{"port":ARGO_PORT ,"listen":"0.0.0.0","protocol":"vless","settings":{"clients":[{"id":UUID }],"decryption":"none"},"streamSettings":{"network":"ws","wsSettings":{"path":"/vle123"}}}],"outbounds":[{"protocol":"freedom","settings": {}}]}
    with open(os.path.join(FILE_PATH, 'mouse.json'), 'w', encoding='utf-8') as config_file:
        json.dump(config, config_file, ensure_ascii=False, indent=2)
    
       
    # Run 
    command = f"nohup {os.path.join(FILE_PATH, 'cat')} -c {os.path.join(FILE_PATH, 'mouse.json')} >/dev/null 2>&1 &"
    try:
        exec_cmd(command)
        print('cat is running')
        time.sleep(1)
    except Exception as e:
        print(f"cat running error: {e}")
    
    # Run cloud
    if os.path.exists(os.path.join(FILE_PATH, 'dog')):
        if not re.match(r'^[A-Z0-9a-z=]{120,250}$', ARGO_AUTH):
            print("ARGO_AUTH variable is empty")
            return
        else:
            args = f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 run --token {ARGO_AUTH}"
        
        try:
            exec_cmd(f"nohup {os.path.join(FILE_PATH, 'dog')} {args} >/dev/null 2>&1 &")
            print('dog is running')
            time.sleep(2)
        except Exception as e:
            print(f"Error executing command: {e}")
    
    time.sleep(5)
    
   
# Main function to start the server
async def start_server():
    create_directory()
    await download_files_and_run()
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()   
    
def run_server():
    server = HTTPServer(('0.0.0.0', PORT), RequestHandler)
    print(f"Server is running on port {PORT}")
    print(f"Running done！")
    print(f"\nLogs will be delete in 90 seconds")
    server.serve_forever()
    
def run_async():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_server()) 
    
    while True:
        time.sleep(3600)
        
if __name__ == "__main__":
    run_async()
