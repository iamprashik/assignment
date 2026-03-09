from socket import *

TRACKER_HOST = "127.0.0.1"
TRACKER_PORT = 6000

part1 = "b13732c67903031abcd006a4c02bc4fe778692d2d640758cea93846997b2a367"
part2 = "9d64b30c3d2047a1c0c77733134491c8a2dddc9354997038244ea9bd41bfc42f"


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

        else:
            print("Server does not have the file.")
            return None

    finally:
        s.close()


def main():
    finaldata = bytearray()

    # Chunk 1
    server_info = ask_tracker_for_server(part1)
    if server_info is None:
        return
    chunk1 = download_chunk(server_info[0], server_info[1], part1)
    finaldata.extend(chunk1)

    # Chunk 2
    server_info = ask_tracker_for_server(part2)
    if server_info is None:
        return
    chunk2 = download_chunk(server_info[0], server_info[1], part2)
    finaldata.extend(chunk2)

    # Write final PDF
    with open("output.pdf", "wb") as f:
        f.write(finaldata)

    print("Reassembled file written to output.pdf")


if __name__ == "__main__":
    main()
