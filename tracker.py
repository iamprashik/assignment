import socket

TRACKER_HOST = "127.0.0.1"
TRACKER_PORT = 6000

SERVER_A = ("127.0.0.1", 5000)
SERVER_B = ("127.0.0.1", 5001)

HASH_MAP = {
    "67fe4ecc5ef935d80e5a71ea1e22ade75344da4ae7187e9fda9fbb00f86de629": SERVER_A,
    "ec4d161d1bc1f007c4ac0ef807850a5fc43b16572a2ec8d2fdc836ac4ef54b1a": SERVER_B
}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TRACKER_HOST, TRACKER_PORT))
s.listen(5)

print(f"[TRACKER STARTED] {TRACKER_HOST}:{TRACKER_PORT}")

while True:
    conn, addr = s.accept()

    print("\n[CLIENT CONNECTED]", addr)

    hash_req = conn.recv(1024).decode().strip()

    print("[HASH REQUEST]", hash_req)

    if hash_req in HASH_MAP:
        ip, port = HASH_MAP[hash_req]

        print(f"[FOUND] {ip}:{port}")
        conn.send(f"{ip} {port}".encode())

    else:
        print("[NOT FOUND]")
        conn.send(b"NOTFOUND")

    conn.close()