#!/usr/bin/env python3
"""
Client for the relay server. Connects and stays connected.

Two modes:
  - send: Send a message and exit
  - recv: Listen for incoming messages (blocking, prints them)
  - interactive: Send and receive (for manual testing)

Usage:
    # Send a single message (connects, sends, disconnects)
    python3 client.py send "Hello from Claude 1"

    # Listen for messages (stays connected, prints received lines)
    python3 client.py recv

    # Send a message and wait for a reply
    python3 client.py send-recv "Hello" --timeout 30
"""

import socket
import argparse
import sys
import time

DEFAULT_PORT = 9999


def connect(port):
    """Connect to relay server. Returns socket."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", port))
    return sock


def cmd_send(args):
    """Send a message and disconnect."""
    sock = connect(args.port)
    msg = args.message + "\n"
    sock.sendall(msg.encode())
    print(f"[client] Sent: {args.message}")
    sock.close()


def cmd_recv(args):
    """Connect and listen for messages. Prints each line received."""
    sock = connect(args.port)
    sock.settimeout(args.timeout if args.timeout > 0 else None)
    print(f"[client] Connected. Listening for messages...", flush=True)

    buf = b""
    try:
        while True:
            try:
                data = sock.recv(4096)
            except socket.timeout:
                print("[client] Timeout waiting for messages.", flush=True)
                break
            if not data:
                print("[client] Connection closed by server.", flush=True)
                break
            buf += data
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                text = line.decode(errors="replace").strip()
                if text:
                    print(f"[recv] {text}", flush=True)
    except KeyboardInterrupt:
        print("\n[client] Disconnecting.", flush=True)
    finally:
        sock.close()


def cmd_send_recv(args):
    """Send a message, then wait for a reply."""
    sock = connect(args.port)
    timeout = args.timeout if args.timeout > 0 else 30

    msg = args.message + "\n"
    sock.sendall(msg.encode())
    print(f"[client] Sent: {args.message}", flush=True)

    sock.settimeout(timeout)
    buf = b""
    try:
        while True:
            try:
                data = sock.recv(4096)
            except socket.timeout:
                print(f"[client] No reply within {timeout}s.", flush=True)
                break
            if not data:
                break
            buf += data
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                text = line.decode(errors="replace").strip()
                if text:
                    print(f"[recv] {text}", flush=True)
                    # Got a reply, we're done
                    sock.close()
                    return
    except KeyboardInterrupt:
        pass
    finally:
        try:
            sock.close()
        except OSError:
            pass


def main():
    parser = argparse.ArgumentParser(description="Relay client")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    sub = parser.add_subparsers(dest="command")

    p_send = sub.add_parser("send")
    p_send.add_argument("message")

    p_recv = sub.add_parser("recv")
    p_recv.add_argument("--timeout", type=float, default=0,
                        help="Timeout in seconds (0=infinite)")

    p_sr = sub.add_parser("send-recv")
    p_sr.add_argument("message")
    p_sr.add_argument("--timeout", type=float, default=30)

    args = parser.parse_args()
    if args.command == "send":
        cmd_send(args)
    elif args.command == "recv":
        cmd_recv(args)
    elif args.command == "send-recv":
        cmd_send_recv(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
