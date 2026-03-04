# Local IPC Communication Between Claude Instances

## Goal
Two Claude instances on the same machine communicate via local IPC, without using disk files or the web.

## Approach
TCP sockets on localhost. Data flows through kernel memory, never touches disk.

## Architecture
- A **relay server** runs as a background process on a known port (e.g., 9999)
- Both Claude instances connect as clients
- Messages from one client are relayed to the other
- Protocol: simple line-based text messages (newline-delimited)

## Why TCP over alternatives?
- Unix domain sockets: require a filesystem path (borderline "file on disk")
- Named pipes: same issue
- Shared memory: more complex, harder to coordinate
- TCP localhost: purely in-memory kernel networking, no filesystem artifacts

## Components
1. `relay_server.py` - Accepts two connections, relays messages between them
2. `send_msg.py` - Send a message to the relay
3. `recv_msg.py` - Receive messages from the relay
4. `chat.sh` - Convenience wrapper

## Status
- [x] Build relay server
- [x] Build send/receive utilities
- [x] Test (bidirectional communication confirmed)
- [ ] Start relay and have actual conversation with Claude 2
