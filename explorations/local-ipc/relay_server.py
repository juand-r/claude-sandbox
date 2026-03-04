#!/usr/bin/env python3
"""
TCP relay server for local IPC between two Claude instances.

Listens on localhost:PORT. Accepts exactly two connections.
Messages from client A are forwarded to client B and vice versa.
Each message is a newline-delimited line of text.

Usage:
    python3 relay_server.py [--port PORT]

Default port: 9999
"""

import socket
import selectors
import argparse
import sys
import time

DEFAULT_PORT = 9999


def main():
    parser = argparse.ArgumentParser(description="TCP relay for Claude IPC")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()

    sel = selectors.DefaultSelector()

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("127.0.0.1", args.port))
    server_sock.listen(2)
    server_sock.setblocking(False)

    print(f"[relay] Listening on 127.0.0.1:{args.port}", flush=True)

    # Track connected clients: list of (socket, addr, buffer)
    clients = []  # [(sock, addr, recv_buffer)]

    def accept_connection(sock, mask):
        conn, addr = sock.accept()
        conn.setblocking(False)
        client_id = len(clients)
        clients.append((conn, addr, b""))
        print(f"[relay] Client {client_id} connected from {addr}", flush=True)

        sel.register(conn, selectors.EVENT_READ, read_client)

        if len(clients) == 2:
            # Stop accepting new connections
            sel.unregister(server_sock)
            print("[relay] Both clients connected. Relaying messages.", flush=True)
            # Notify both clients
            try:
                clients[0][0].sendall(b"[relay] Both clients connected. You can now chat.\n")
                clients[1][0].sendall(b"[relay] Both clients connected. You can now chat.\n")
            except OSError:
                pass

    def read_client(sock, mask):
        # Find which client this is and who the peer is
        client_idx = None
        for i, (s, a, buf) in enumerate(clients):
            if s is sock:
                client_idx = i
                break

        if client_idx is None:
            return

        try:
            data = sock.recv(4096)
        except ConnectionResetError:
            data = b""

        if not data:
            print(f"[relay] Client {client_idx} disconnected.", flush=True)
            sel.unregister(sock)
            sock.close()
            return

        # Append to buffer and process complete lines
        _, addr, buf = clients[client_idx]
        buf += data
        clients[client_idx] = (sock, addr, buf)

        # Forward complete lines to the other client
        while b"\n" in buf:
            line, buf = buf.split(b"\n", 1)
            clients[client_idx] = (sock, addr, buf)

            peer_idx = 1 - client_idx
            if peer_idx < len(clients):
                peer_sock = clients[peer_idx][0]
                try:
                    peer_sock.sendall(line + b"\n")
                except (OSError, BrokenPipeError):
                    print(f"[relay] Failed to send to client {peer_idx}", flush=True)

    sel.register(server_sock, selectors.EVENT_READ, accept_connection)

    print("[relay] Waiting for two clients to connect...", flush=True)

    try:
        while True:
            events = sel.select(timeout=1)
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
    except KeyboardInterrupt:
        print("\n[relay] Shutting down.", flush=True)
    finally:
        sel.close()
        server_sock.close()
        for s, _, _ in clients:
            try:
                s.close()
            except OSError:
                pass


if __name__ == "__main__":
    main()
