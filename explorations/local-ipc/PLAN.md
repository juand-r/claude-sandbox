# Local IPC Communication Between Claude Instances

## Goal
Two Claude instances on the same machine communicate via local IPC, without using disk files or the web.

## Approach
Unix domain sockets on a shared filesystem path. Data flows through kernel memory, never touches disk.
(Originally tried TCP on localhost, but that doesn't work across containers with separate network namespaces.)

## Architecture
- A **relay server** creates a Unix domain socket at a known path on the shared filesystem
- Both Claude instances connect as clients
- Messages from one client are relayed to the other
- Protocol: simple line-based text messages (newline-delimited)

## Why Unix domain sockets?
- TCP localhost: doesn't work across containers (separate network namespaces)
- Named pipes: unidirectional, need two for bidirectional
- Shared memory: more complex, harder to coordinate
- Unix domain sockets: use filesystem path (shared across containers), data stays in kernel memory

## Components
1. `relay_server.py` - Accepts two connections, relays messages between them
2. `send_msg.py` - Send a message to the relay
3. `recv_msg.py` - Receive messages from the relay
4. `chat.sh` - Convenience wrapper

## Status
- [x] Build TCP relay server (v1 -- doesn't work across containers)
- [x] Pivot to Unix domain sockets (v2 -- works across containers)
- [x] Build send/receive utilities
- [x] Test (bidirectional communication confirmed)
- [ ] Start relay and have actual conversation with Claude 2
