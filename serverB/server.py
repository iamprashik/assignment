import socket
import os
import hashlib

HOST = "127.0.0.1"
PORT = 5001   # change to 5001 for serverB

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.join(BASE_DIR, "files")

hash_to_file = {}

for fname in os.listdir(FILES_DIR):
    fpath = os.path.join(FILES_DIR, fname)
    if not os.path.isfile(fpath):
        continue
    with open(fpath, "rb") as f:
        data = f.read()
    h = hashlib.sha256(data).hexdigest()
    hash_to_file[h] = fpath
    print(f"Indexed file {fname} with hash {h}")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print(f"Server listening on {HOST}:{PORT}")

while True:
    conn, addr = s.accept()
    print("Connection from:", addr)

    try:
        data = conn.recv(1024)
        if not data:
            conn.close()
            continue

        msg = data.decode().strip()
        print("Received hash:", msg)

        if msg in hash_to_file:
            conn.send(b"gotfile")
            ack = conn.recv(1024)

            with open(hash_to_file[msg], "rb") as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    conn.sendall(chunk)

            print("Finished sending file.")

        else:
            conn.send(b"nofile")

    finally:
        conn.close()
