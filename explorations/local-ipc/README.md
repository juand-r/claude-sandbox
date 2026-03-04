# Local IPC Communication Between Claude Instances

Two Claude instances in the same environment communicate via Unix domain sockets.
No message data is written to disk -- data flows through kernel socket buffers (in-memory).
The socket file is just an address endpoint, not a data store.

Works across containers that share a filesystem (e.g., Claude Code web sessions).

## How It Works

A relay server creates a Unix domain socket at a shared filesystem path.
Both Claude instances connect as clients. Messages from one are forwarded to the other.

## Usage

### Claude 1 (starts the server, then communicates)
```bash
# Start the relay (runs in background)
python3 /home/user/claude-sandbox/explorations/local-ipc/ipc.py server &

# Send a message and wait for reply
python3 /home/user/claude-sandbox/explorations/local-ipc/ipc.py talk "Hello Claude 2!" --timeout 120
```

### Claude 2 (connects and communicates)
```bash
# Listen for one message
python3 /home/user/claude-sandbox/explorations/local-ipc/ipc.py listen --once --timeout 120

# Send a reply
python3 /home/user/claude-sandbox/explorations/local-ipc/ipc.py send "Hello back!"
```

## Why Unix Domain Sockets?

TCP on localhost doesn't work across containers (separate network namespaces).
Unix domain sockets use a filesystem path as address, which IS shared across containers.
The actual data never touches disk -- it flows through kernel memory.

## Files

- `ipc.py` - All-in-one server + client tool (Unix domain sockets)
- `relay_server.py` - Standalone TCP relay server (single-container only)
- `client.py` - Standalone TCP client
- `test_ipc.py` - Self-contained test (run to verify everything works)
