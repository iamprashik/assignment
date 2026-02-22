📦 Distributed File Retrieval System
A simple content‑addressable, multi‑server file reconstruction project built with Python sockets.

📘 Overview
This project demonstrates a lightweight distributed file retrieval system. A single PDF file is split into two binary chunks, each stored on a different server. A client retrieves these chunks using content‑addressable storage — meaning the client requests each chunk by its SHA‑256 hash, not by filename.

Once both chunks are downloaded, the client reassembles them into the original PDF.

This mirrors the core ideas behind systems like:

BitTorrent

IPFS

Git object storage

Distributed file sharding

The goal is to understand how distributed systems identify and retrieve data using hashes, and how to transfer binary data reliably over TCP sockets.

🧠 How It Works
1. Server Startup
Each server:

Loads the binary file in its files/ directory

Computes its SHA‑256 hash

Stores a mapping:

Code
<hash> → <file path>
Listens for incoming TCP connections

Sends the file only if the client provides the matching hash

This makes the server content‑addressable — it doesn’t care about filenames, only the file’s fingerprint.

2. Client Behavior
The client:

Knows the expected hashes of chunk 1 and chunk 2

Connects to Server A and sends the hash for chunk 1

If the server responds "gotfile", the client downloads the binary data

Repeats the process with Server B for chunk 2

Combines both chunks

Writes the final output.pdf

The client does not compute any hashes — it simply uses the known hashes provided in the assignment.

🗂️ Project Structure
Code
assignment1/
│
├── client.py
│
├── serverA/
│   ├── server.py
│   └── files/
│       └── chunk1.bin
│
└── serverB/
    ├── server.py
    └── files/
        └── chunk2.bin


🔑 Key Concepts Demonstrated
✔ Content‑Addressable Storage
Files are identified by their SHA‑256 hash, not by name.
This ensures:

Integrity

Uniqueness

Easy verification

✔ Binary File Transfer Over TCP
The client receives raw bytes using recv() and reconstructs the file locally.

✔ Distributed File Sharding
Each server stores only part of the file.
The client must contact multiple servers to rebuild the original document.

✔ Hash‑Based Lookup
The server only sends a file if the hash matches exactly — preventing accidental or incorrect file retrieval.

▶️ Running the Project
1. Start Server A
Code
cd serverA
python server.py

2. Start Server B
Code
cd serverB
python server.py

3. Run the Client
Code
cd assignment1
python client.py

If both chunks are found, you’ll see:

Code
Received XXXX bytes for hash <chunk1>
Received XXXX bytes for hash <chunk2>
Wrote reassembled file to output.pdf
Your reconstructed PDF will appear in the assignment1 folder.

🧪 Example Output
Code
Client sent hash to 127.0.0.1:5000: b13732c6...
Client received response: gotfile
Received 9523 bytes for hash b13732c6...

Client sent hash to 127.0.0.1:5001: 9d64b30c...
Client received response: gotfile
Received 9524 bytes for hash 9d64b30c...

Wrote reassembled file to output.pdf

🎯 What You Learn From This Project
How distributed systems store and retrieve data by content, not by name

How to compute and use SHA‑256 hashes

How to send and receive binary data over sockets

How to reconstruct files from multiple sources

How to design a simple but realistic distributed architecture