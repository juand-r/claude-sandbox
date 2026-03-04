#!/usr/bin/env python3
"""
All-in-one IPC tool for Claude instances to communicate.

Uses Unix domain sockets so it works across containers that share a filesystem.
The socket file is just an address endpoint -- no message data is written to disk.
All data flows through the kernel's socket buffers (in-memory).

Commands:
    python3 ipc.py server          Start the relay server
    python3 ipc.py listen           Connect and listen for messages
    python3 ipc.py send "message"   Connect, send a message, disconnect
    python3 ipc.py talk "message"   Connect, send message, wait for reply, disconnect

How to use:
  Claude 1: python3 ipc.py server &         (start relay in background)
  Claude 1: python3 ipc.py send "Hello!"     (send a message)
  Claude 2: python3 ipc.py listen --once     (get one message)
  Claude 2: python3 ipc.py send "Hi back!"   (reply)

Socket path: /home/user/claude-sandbox/explorations/local-ipc/.ipc.sock (default)
"""

import socket
import selectors
import sys
import os
import time
import argparse

DEFAULT_SOCK = "/home/user/claude-sandbox/explorations/local-ipc/.ipc.sock"


# ===========================================================================
# RELAY SERVER
# ===========================================================================

def run_server(sock_path):
    """Accept two persistent connections, relay between them."""
    # Clean up stale socket file
    if os.path.exists(sock_path):
        os.unlink(sock_path)

    sel = selectors.DefaultSelector()
    srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    srv.bind(sock_path)
    srv.listen(2)
    srv.setblocking(False)

    print(f"[server] Listening on {sock_path}", flush=True)
    print("[server] Waiting for two clients...", flush=True)

    clients = []  # [[sock, label, buffer]]

    def accept(sock, mask):
        conn, _ = sock.accept()
        conn.setblocking(False)
        idx = len(clients)
        clients.append([conn, f"client_{idx}", b""])
        sel.register(conn, selectors.EVENT_READ, relay)
        print(f"[server] Client {idx} connected.", flush=True)
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
            print(f"[server] Client {idx} disconnected. Re-listening.", flush=True)
            sel.unregister(sock)
            sock.close()
            clients.pop(idx)
            # Re-accept new connections
            try:
                sel.register(srv, selectors.EVENT_READ, accept)
            except (KeyError, ValueError):
                pass
            return

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
        if os.path.exists(sock_path):
            os.unlink(sock_path)


# ===========================================================================
# CLIENT OPERATIONS
# ===========================================================================

def connect(sock_path, retries=10, delay=1.0):
    """Connect to relay server via Unix domain socket, with retries."""
    for attempt in range(retries):
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(sock_path)
            return sock
        except (FileNotFoundError, ConnectionRefusedError) as e:
            if attempt < retries - 1:
                print(f"[client] Waiting for server... (attempt {attempt+1}/{retries})", flush=True)
                time.sleep(delay)
            else:
                print(f"[client] ERROR: Cannot connect to {sock_path}: {e}", file=sys.stderr)
                sys.exit(1)


def do_listen(sock_path, once=False, timeout=60):
    """Connect to relay and print received messages."""
    sock = connect(sock_path)
    sock.settimeout(timeout if timeout > 0 else None)
    print(f"[listen] Connected. Waiting for messages...", flush=True)

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


def do_send(sock_path, message):
    """Connect, send one message, disconnect."""
    sock = connect(sock_path)
    sock.sendall((message + "\n").encode())
    print(f"[send] Sent: {message}", flush=True)
    sock.settimeout(0.5)
    try:
        sock.recv(4096)
    except socket.timeout:
        pass
    sock.close()


def do_talk(sock_path, message, timeout=60):
    """Connect, send message, wait for one reply, disconnect."""
    sock = connect(sock_path)

    # Read and discard server greeting
    try:
        sock.settimeout(2)
        sock.recv(4096)
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
        description="IPC tool for Claude-to-Claude communication via Unix domain sockets"
    )
    parser.add_argument("--sock", default=DEFAULT_SOCK,
                        help=f"Socket path (default: {DEFAULT_SOCK})")
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
        run_server(args.sock)
    elif args.command == "listen":
        do_listen(args.sock, once=args.once, timeout=args.timeout)
    elif args.command == "send":
        do_send(args.sock, args.message)
    elif args.command == "talk":
        do_talk(args.sock, args.message, timeout=args.timeout)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
