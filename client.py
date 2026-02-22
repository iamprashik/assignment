from socket import *

host1 = "127.0.0.1"
port1 = 5000

host2 = "127.0.0.1"
port2 = 5001

part1 = "b13732c67903031abcd006a4c02bc4fe778692d2d640758cea93846997b2a367"
part2 = "9d64b30c3d2047a1c0c77733134491c8a2dddc9354997038244ea9bd41bfc42f"


def download_chunk(host, port, part_hash):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port))

    try:
        # Send hash
        msg = part_hash
        s.send(msg.encode())
        print(f"Client sent hash to {host}:{port}: {msg}")

        # Get server response
        resp = s.recv(1024)
        if not resp:
            print("No response from server")
            return None

        resp_str = resp.decode()
        print("Client received response:", resp_str)

        if resp_str == "gotfile":
            s.send(b"ackfile")
            chunk_data = bytearray()
            # Receive file bytes until server closes connection
            while True:
                data = s.recv(4096)
                if not data:
                    break
                chunk_data.extend(data)
            print(f"Received {len(chunk_data)} bytes for hash {part_hash}")
            return bytes(chunk_data)

        elif resp_str == "nofile":
            s.send(b"acknone")
            print("Server does not have requested file part.")
            return None

        else:
            print("Unexpected response from server:", resp_str)
            return None

    finally:
        s.close()


def main():
    finaldata = bytearray()

    # Get file chunk from server 1
    chunk1 = download_chunk(host1, port1, part1)
    if chunk1 is None:
        print("Failed to download chunk 1, exiting.")
        return
    finaldata.extend(chunk1)

    # Get file chunk from server 2
    chunk2 = download_chunk(host2, port2, part2)
    if chunk2 is None:
        print("Failed to download chunk 2, exiting.")
        return
    finaldata.extend(chunk2)

    # Reassemble and write out the final PDF
    output_filename = "output.pdf"
    with open(output_filename, "wb") as f:
        f.write(finaldata)

    print(f"Wrote reassembled file to {output_filename}")


if __name__ == "__main__":
    main()
