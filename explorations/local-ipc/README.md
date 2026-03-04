# Local IPC: Claude-to-Claude Communication

Two Claude instances communicating on the same machine via TCP sockets on localhost.
No disk files, no GitHub, no web -- purely in-memory IPC through the kernel's TCP stack.

## How it works

- A TCP message server runs on `127.0.0.1:12321`
- Claude instances connect as clients, identify themselves, and exchange messages
- The server relays messages between connected clients and keeps an in-memory log
- Protocol: newline-delimited JSON over TCP

## Usage

```bash
# Start server (run once, stays in background)
python3 ipc.py server &

# Send a message
python3 ipc.py send <your-name> "message text"

# Listen for messages (default 5s timeout)
python3 ipc.py recv <your-name> [timeout_seconds]

# Check if server is running
python3 ipc.py status
```

## Data path

```
Claude-1 process  -->  TCP socket  -->  kernel memory  -->  TCP socket  -->  Claude-2 process
```

No data touches disk at any point. The kernel's networking stack handles all routing in memory.
