from socket import *

TRACKER_HOST = "127.0.0.1"
TRACKER_PORT = 6000

part1 = "67fe4ecc5ef935d80e5a71ea1e22ade75344da4ae7187e9fda9fbb00f86de629"
part2 = "ec4d161d1bc1f007c4ac0ef807850a5fc43b16572a2ec8d2fdc836ac4ef54b1a"


def ask_tracker_for_server(part_hash):
    t = socket(AF_INET, SOCK_STREAM)
    t.connect((TRACKER_HOST, TRACKER_PORT))
    t.send(part_hash.encode())

    resp = t.recv(1024).decode().strip()
    t.close()

    if resp == "NOTFOUND":
        print("Tracker does not know this hash.")
        return None

    ip, port = resp.split()
    return ip, int(port)


def download_chunk(host, port, part_hash):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port))

    try:
        s.send(part_hash.encode())
        resp = s.recv(1024).decode().strip()
        print("Server response:", resp)

        if resp == "gotfile":
            s.send(b"ackfile")
            chunk_data = bytearray()

            while True:
                data = s.recv(4096)
                if not data:
                    break
                chunk_data.extend(data)

            print(f"Received {len(chunk_data)} bytes from {host}:{port}")
            return bytes(chunk_data)

        print("Server does not have the file.")
        return None

    finally:
        s.close()


def main():
    print("\n[DISTRIBUTED FILE RETRIEVAL CLIENT]\n")

    finaldata = bytearray()

    print("[TRACKER] Looking up Chunk 1...")
    server_info = ask_tracker_for_server(part1)

    if server_info is None:
        return

    print(f"[FOUND] Chunk 1 -> {server_info[0]}:{server_info[1]}")
    print("[DOWNLOAD] Retrieving Chunk 1...")

    chunk1 = download_chunk(
        server_info[0],
        server_info[1],
        part1
    )

    if chunk1 is None:
        return

    finaldata.extend(chunk1)
    print("[SUCCESS] Chunk 1 received\n")

    print("[TRACKER] Looking up Chunk 2...")
    server_info = ask_tracker_for_server(part2)

    if server_info is None:
        return

    print(f"[FOUND] Chunk 2 -> {server_info[0]}:{server_info[1]}")
    print("[DOWNLOAD] Retrieving Chunk 2...")

    chunk2 = download_chunk(
        server_info[0],
        server_info[1],
        part2
    )

    if chunk2 is None:
        return

    finaldata.extend(chunk2)
    print("[SUCCESS] Chunk 2 received\n")

    print("[REASSEMBLY] Combining downloaded chunks...")

    with open("reconstructed-file.pdf", "wb") as f:
        f.write(finaldata)

    print("\n[SUCCESS] File reconstructed successfully.")
    print("Output: reconstructed-file.pdf")


if __name__ == "__main__":
    main()