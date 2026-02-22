import socket
import os
import hashlib

HOST = "127.0.0.1"
PORT = 5001 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.join(BASE_DIR, "files")

# Build a map: sha256 hash (hex) -> file path
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
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)

print(f"File server listening on {HOST}:{PORT}")

while True:
    conn, addr = s.accept()
    print(f"Connection from {addr}")

    try:
        # Receive hash from client
        data = conn.recv(1024)
        if not data:
            conn.close()
            continue

        msg = data.decode().strip()
        print("Server received hash:", msg)

        if msg in hash_to_file:
            conn.send(b"gotfile")
            # Wait for client ack
            ack = conn.recv(1024)
            if not ack:
                conn.close()
                continue
            print("Client reply after gotfile:", ack.decode().strip())

            # Send file bytes
            fpath = hash_to_file[msg]
            with open(fpath, "rb") as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    conn.sendall(chunk)
            print("Finished sending file for hash", msg)
        else:
            conn.send(b"nofile")
            ack = conn.recv(1024)
            if ack:
                print("Client reply after nofile:", ack.decode().strip())
            print("No file for hash", msg)

    finally:
        conn.close()
