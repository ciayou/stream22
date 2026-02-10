import os
import re
import json
import time
import asyncio
import platform
import subprocess

# Environment variables
FILE_PATH = os.environ.get('FILE_PATH', './files')   
UUID = os.environ.get('UUID', '01010101-0101-0101-0101-010101010101')  
ARGO_DOMAIN = os.environ.get('ARGO_DOMAIN', '123.abc.com')       
ARGO_AUTH = os.environ.get('ARGO_AUTH', 'eyJhIjoiNWMwNGE0MTY3OTFkOTg2MDY2MjE1Yzc2MTQ2MGZlZDIiLCJ0IjoiNWFlMmY0MzMtZDgwOS00YzlhLWIzNGItMmQ0NjllN2QyNjJhIiwicyI6Ik1tRTNZMlZoTkdJdE56ZGxNeTAwWXpka0xUZzVPV010TnpBMVlXSmtZVEF4TlRFNCJ9')            
ARGO_PORT = int(os.environ.get('ARGO_PORT', '8080'))   

# Create running folder
def create_directory():
    print('\033c', end='')
    if not os.path.exists(FILE_PATH):
        os.makedirs(FILE_PATH)
        print(f"{FILE_PATH} is created")
    else:
        print(f"{FILE_PATH} already exists")

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
    config ={"log":{"access":"/dev/null","error":"/dev/null","loglevel":"none",},"inbounds":[{"port":ARGO_PORT ,"protocol":"vless","settings":{"clients":[{"id":UUID }],"decryption":"none"},"streamSettings":{"network":"ws","wsSettings":{"path":"/"}}}],"outbounds":[{"protocol":"freedom","settings": {}}]}
    with open(os.path.join(FILE_PATH, 'mouse.json'), 'w', encoding='utf-8') as config_file:
        json.dump(config, config_file, ensure_ascii=False, indent=2)
    
       
    # Run sbX
    command = f"nohup {os.path.join(FILE_PATH, 'cat')} -c {os.path.join(FILE_PATH, 'mouse.json')} >/dev/null 2>&1 &"
    try:
        exec_cmd(command)
        print('cat is running')
        time.sleep(1)
    except Exception as e:
        print(f"cat running error: {e}")
    
    # Run cloudflared
    if os.path.exists(os.path.join(FILE_PATH, 'dog')):
        if re.match(r'^[A-Z0-9a-z=]{120,250}$', ARGO_AUTH):
            args = f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 run --token {ARGO_AUTH}"
        elif "TunnelSecret" in ARGO_AUTH:
            args = f"tunnel --edge-ip-version auto --config {os.path.join(FILE_PATH, 'tunnel.yml')} run"
        else:
            args = f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 --logfile {os.path.join(FILE_PATH, 'boot.log')} --loglevel info --url http://localhost:{ARGO_PORT}"
        
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

     
def run_async():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_server()) 
    
    while True:
        time.sleep(3600)
        
if __name__ == "__main__":
    run_async()
