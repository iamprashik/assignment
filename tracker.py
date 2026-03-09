import socket

TRACKER_HOST = "127.0.0.1"
TRACKER_PORT = 6000

# Hard-coded server info
SERVER_A = ("127.0.0.1", 5000)
SERVER_B = ("127.0.0.1", 5001)

# Hard-coded hash → server mapping
HASH_MAP = {
    "b13732c67903031abcd006a4c02bc4fe778692d2d640758cea93846997b2a367": SERVER_A,
    "9d64b30c3d2047a1c0c77733134491c8a2dddc9354997038244ea9bd41bfc42f": SERVER_B
}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TRACKER_HOST, TRACKER_PORT))
s.listen(5)

print(f"Tracker running on {TRACKER_HOST}:{TRACKER_PORT}")

while True:
    conn, addr = s.accept()
    print("Client connected:", addr)

    hash_req = conn.recv(1024).decode().strip()
    print("Tracker received hash:", hash_req)

    if hash_req in HASH_MAP:
        ip, port = HASH_MAP[hash_req]
        conn.send(f"{ip} {port}".encode())
    else:
        conn.send(b"NOTFOUND")

    conn.close()
