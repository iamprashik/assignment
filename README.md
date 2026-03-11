📦 Distributed File Retrieval System (Tracker Version)
A lightweight distributed file retrieval system inspired by BitTorrent.
This version extends a tracker server, which coordinates clients and file servers. The client no longer knows where file chunks are stored — instead, it asks the tracker, which returns the correct server address.

This architecture is more realistic, scalable, and modular than the direct client‑server model used previously.

🚀 Overview
The system stores a PDF file split into two binary chunks:

Server A stores chunk 1

Server B stores chunk 2

Each chunk is identified by its SHA‑256 hash.

Before, the client connected directly to Server A and Server B.
Now, the client connects only to the tracker, which tells the client where each chunk is located.

This mirrors how BitTorrent trackers coordinate peers.

🧠 Architecture
Code
          ┌──────────────┐
          │    Tracker    │
          │ (hash lookup) │
          └───────┬──────┘
                  │
     ┌────────────┴────────────┐
     │                           │
┌───────────┐             ┌───────────┐
│  Server A │             │  Server B │
│ chunk 1   │             │ chunk 2   │
└─────┬─────┘             └─────┬─────┘
      │                           │
      └────────────┬──────────────┘
                   │
             ┌──────────┐
             │  Client   │
             │ (rebuild) │
             └──────────┘
🔑 Key Concepts
✔ Content‑Addressable Storage
Servers identify files by hash, not by name.

✔ Tracker‑Based Lookup
The client sends a hash to the tracker.
The tracker replies with the correct server’s IP and port.

✔ Distributed File Sharding
Each server stores only part of the file.

✔ Binary File Transfer
The client downloads raw bytes and reconstructs the original PDF.

📂 Project Structure
Code
assignment/
│
├── client.py
├── tracker.py
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
▶️ How It Works (Step‑by‑Step)
1. Client → Tracker
Client sends the hash of the chunk it wants.

Example:

Code
b13732c6...
2. Tracker → Client
Tracker checks its internal hash table and replies:

Code
127.0.0.1 5000
Meaning:

“Chunk 1 is on Server A.”

3. Client → Server A
Client connects to the server returned by the tracker and downloads the chunk.

4. Repeat for chunk 2
Tracker returns Server B → client downloads chunk 2.

5. Client rebuilds the PDF
Chunks are concatenated in order and written to:

Code
output.pdf
🛠️ Running the System
Open three terminals for the servers and tracker, and one for the client.

1. Start the Tracker
Code
python tracker.py
2. Start Server A
Code
cd serverA
python server.py
3. Start Server B
Code
cd serverB
python server.py
4. Run the Client
Code
python client.py
If everything is correct, you’ll see:

Code
Tracker says: 127.0.0.1 5000
Received 9523 bytes
Tracker says: 127.0.0.1 5001
Received 9524 bytes
Wrote reassembled file to output.pdf
🧪 Example Output
Code
Client sent hash to tracker: b13732c6...
Tracker returned: 127.0.0.1 5000
Server response: gotfile
Received 9523 bytes

Client sent hash to tracker: 9d64b30c...
Tracker returned: 127.0.0.1 5001
Server response: gotfile
Received 9524 bytes

Reassembled file written to output.pdf
Feature	OLD PART	NEW PART
Client knows server IPs	✔ Yes	❌ No
Tracker exists	❌ No	✔ Yes
Client → Server directly	✔ Yes	❌ No
Client → Tracker → Server	❌ No	✔ Yes
Scalable architecture	❌ Limited	✔ Much better
Realistic distributed design	❌ No	✔ Yes
This model is a strict upgrade of the old one.
It keeps all functionality but adds a tracker, making the system more modular and closer to real distributed systems.

🎯 Learning Outcomes
By completing this project, you learn:

How trackers coordinate distributed systems

How to implement content‑addressable storage

How to transfer binary data over sockets

How to design modular, scalable architectures

How BitTorrent‑style systems locate file pieces
