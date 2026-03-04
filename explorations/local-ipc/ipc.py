#!/usr/bin/env python3
"""
All-in-one IPC tool for Claude instances to communicate.

Commands:
    python3 ipc.py server          Start the relay server (Claude 1 does this)
    python3 ipc.py listen           Connect and listen for messages
    python3 ipc.py send "message"   Connect, send a message, disconnect
    python3 ipc.py talk "message"   Connect, send message, wait for reply, disconnect

Port: 9999 (default), override with --port

How to use:
  Claude 1: python3 ipc.py server           (start relay, keeps running)
  Claude 1: python3 ipc.py send "Hello!"     (send a message)
  Claude 2: python3 ipc.py listen            (listen for messages)
  Claude 2: python3 ipc.py send "Hi back!"   (reply)

For a conversation:
  Claude 1: python3 ipc.py talk "Hello Claude 2, what is 2+2?"
  Claude 2: python3 ipc.py listen --once     (get one message, print it)
  Claude 2: python3 ipc.py talk "The answer is 4"
  Claude 1: (gets the reply from the talk command)
"""

import socket
import selectors
import sys
import time
import argparse
import threading

DEFAULT_PORT = 9999


# ===========================================================================
# RELAY SERVER
# ===========================================================================

def run_server(port):
    """Accept two persistent connections, relay between them."""
    sel = selectors.DefaultSelector()
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", port))
    srv.listen(2)
    srv.setblocking(False)

    print(f"[server] Listening on 127.0.0.1:{port}", flush=True)
    print("[server] Waiting for two clients...", flush=True)

    clients = []  # [(sock, addr, buffer)]

    def accept(sock, mask):
        conn, addr = sock.accept()
        conn.setblocking(False)
        idx = len(clients)
        clients.append([conn, addr, b""])
        sel.register(conn, selectors.EVENT_READ, relay)
        print(f"[server] Client {idx} connected from {addr}", flush=True)
        if len(clients) >= 2:
            sel.unregister(srv)
            print("[server] Both clients connected. Relaying.", flush=True)
            for c in clients:
                try:
                    c[0].sendall(b"[server] Connected. You can exchange messages now.\n")
                except OSError:
                    pass

    def relay(sock, mask):
        idx = next((i for i, c in enumerate(clients) if c[0] is sock), None)
        if idx is None:
            return
        try:
            data = sock.recv(4096)
        except (ConnectionResetError, OSError):
            data = b""
        if not data:
            print(f"[server] Client {idx} disconnected. Accepting new connection.", flush=True)
            sel.unregister(sock)
            sock.close()
            # Allow reconnection: remove and re-listen
            clients.pop(idx)
            if srv.fileno() != -1:
                try:
                    sel.register(srv, selectors.EVENT_READ, accept)
                except (KeyError, ValueError):
                    pass
            return

        # Append to buffer, forward complete lines
        clients[idx][2] += data
        while b"\n" in clients[idx][2]:
            line, clients[idx][2] = clients[idx][2].split(b"\n", 1)
            peer_idx = 1 - idx
            if peer_idx < len(clients):
                try:
                    clients[peer_idx][0].sendall(line + b"\n")
                except (OSError, BrokenPipeError):
                    print(f"[server] Failed to relay to client {peer_idx}", flush=True)

    sel.register(srv, selectors.EVENT_READ, accept)

    try:
        while True:
            events = sel.select(timeout=1)
            for key, mask in events:
                key.data(key.fileobj, mask)
    except KeyboardInterrupt:
        print("\n[server] Shutdown.", flush=True)
    finally:
        sel.close()
        srv.close()


# ===========================================================================
# CLIENT OPERATIONS
# ===========================================================================

def do_listen(port, once=False, timeout=60):
    """Connect to relay and print received messages."""
    sock = socket.socket()
    sock.connect(("127.0.0.1", port))
    sock.settimeout(timeout if timeout > 0 else None)
    print(f"[listen] Connected to relay on port {port}. Waiting for messages...", flush=True)

    buf = b""
    try:
        while True:
            try:
                data = sock.recv(4096)
            except socket.timeout:
                print("[listen] Timeout.", flush=True)
                break
            if not data:
                print("[listen] Connection closed.", flush=True)
                break
            buf += data
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                text = line.decode(errors="replace").strip()
                if text and not text.startswith("[server]"):
                    print(f"[message] {text}", flush=True)
                    if once:
                        sock.close()
                        return
    except KeyboardInterrupt:
        pass
    finally:
        try:
            sock.close()
        except OSError:
            pass


def do_send(port, message):
    """Connect, send one message, disconnect."""
    sock = socket.socket()
    sock.connect(("127.0.0.1", port))
    sock.sendall((message + "\n").encode())
    print(f"[send] Sent: {message}", flush=True)
    # Read any immediate server notification (discard)
    sock.settimeout(0.5)
    try:
        sock.recv(4096)
    except socket.timeout:
        pass
    sock.close()


def do_talk(port, message, timeout=60):
    """Connect, send message, wait for one reply, disconnect."""
    sock = socket.socket()
    sock.connect(("127.0.0.1", port))
    sock.settimeout(timeout if timeout > 0 else None)

    # Read and discard server greeting
    try:
        sock.settimeout(2)
        greeting = sock.recv(4096)
    except socket.timeout:
        pass

    sock.settimeout(timeout if timeout > 0 else None)
    sock.sendall((message + "\n").encode())
    print(f"[talk] Sent: {message}", flush=True)
    print(f"[talk] Waiting for reply (timeout={timeout}s)...", flush=True)

    buf = b""
    try:
        while True:
            try:
                data = sock.recv(4096)
            except socket.timeout:
                print("[talk] Timeout waiting for reply.", flush=True)
                break
            if not data:
                print("[talk] Connection closed.", flush=True)
                break
            buf += data
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                text = line.decode(errors="replace").strip()
                if text and not text.startswith("[server]"):
                    print(f"[reply] {text}", flush=True)
                    sock.close()
                    return
    except KeyboardInterrupt:
        pass
    finally:
        try:
            sock.close()
        except OSError:
            pass


# ===========================================================================
# MAIN
# ===========================================================================

def main():
    parser = argparse.ArgumentParser(
        description="IPC tool for Claude-to-Claude communication via TCP relay"
    )
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("server", help="Start relay server")

    p_listen = sub.add_parser("listen", help="Listen for messages")
    p_listen.add_argument("--once", action="store_true", help="Exit after one message")
    p_listen.add_argument("--timeout", type=float, default=60)

    p_send = sub.add_parser("send", help="Send a message")
    p_send.add_argument("message")

    p_talk = sub.add_parser("talk", help="Send message, wait for reply")
    p_talk.add_argument("message")
    p_talk.add_argument("--timeout", type=float, default=60)

    args = parser.parse_args()

    if args.command == "server":
        run_server(args.port)
    elif args.command == "listen":
        do_listen(args.port, once=args.once, timeout=args.timeout)
    elif args.command == "send":
        do_send(args.port, args.message)
    elif args.command == "talk":
        do_talk(args.port, args.message, timeout=args.timeout)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
