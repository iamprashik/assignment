import socket
import os
import hashlib

HOST = "127.0.0.1"
PORT = 5000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.join(BASE_DIR, "files")

hash_to_file = {}

print("[SERVER A] Indexing files...\n")

for fname in os.listdir(FILES_DIR):
    fpath = os.path.join(FILES_DIR, fname)

    if not os.path.isfile(fpath):
        continue

    with open(fpath, "rb") as f:
        data = f.read()

    h = hashlib.sha256(data).hexdigest()
    hash_to_file[h] = fpath

    print(f"[INDEXED] {fname}")
    print(f"[SHA-256] {h}\n")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print(f"[SERVER A STARTED] {HOST}:{PORT}")

while True:
    conn, addr = s.accept()

    print("\n[CLIENT CONNECTED]", addr)

    try:
        data = conn.recv(1024)

        if not data:
            conn.close()
            continue

        msg = data.decode().strip()

        print("[HASH REQUEST]", msg)

        if msg in hash_to_file:
            conn.send(b"gotfile")

            conn.recv(1024)

            with open(hash_to_file[msg], "rb") as f:
                while True:
                    chunk = f.read(4096)

                    if not chunk:
                        break

                    conn.sendall(chunk)

            print("[SUCCESS] Chunk sent.")

        else:
            conn.send(b"nofile")
            print("[NOT FOUND] Requested chunk unavailable.")

    finally:
        conn.close()