# Local IPC Communication Between Claude Instances

Two Claude instances on the same machine communicate via TCP sockets on localhost.
No files on disk are used for message passing -- data flows through kernel memory only.

## How It Works

A relay server runs on `127.0.0.1:9999`. Both Claude instances connect as TCP clients.
Messages from one client are forwarded to the other.

## Usage

### Claude 1 (starts the server, then communicates)
```bash
# Start the relay (runs in background)
python3 explorations/local-ipc/ipc.py server &

# Send a message
python3 explorations/local-ipc/ipc.py send "Hello Claude 2!"

# Or send and wait for a reply
python3 explorations/local-ipc/ipc.py talk "What is 2+2?" --timeout 120
```

### Claude 2 (connects and communicates)
```bash
# Listen for messages (blocks until one arrives)
python3 explorations/local-ipc/ipc.py listen --once --timeout 120

# Send a reply
python3 explorations/local-ipc/ipc.py send "The answer is 4"
```

## Files

- `ipc.py` - All-in-one server + client tool
- `relay_server.py` - Standalone relay server
- `client.py` - Standalone client with send/recv/send-recv modes
- `test_ipc.py` - Self-contained test (run to verify everything works)
