#!/usr/bin/env python3
"""
Send a single message to the relay server.

Usage:
    python3 send_msg.py "Hello from Claude 1"
    python3 send_msg.py --port 9999 "Hello"
"""

import socket
import argparse
import sys

DEFAULT_PORT = 9999


def main():
    parser = argparse.ArgumentParser(description="Send a message via relay")
    parser.add_argument("message", help="Message to send")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", args.port))
        sock.sendall((args.message + "\n").encode())

        # Wait briefly for any response
        sock.settimeout(2.0)
        try:
            response = sock.recv(4096)
            if response:
                print(response.decode().strip())
        except socket.timeout:
            pass

        sock.close()
        print(f"[send] Message sent: {args.message}")
    except ConnectionRefusedError:
        print("[send] ERROR: Cannot connect to relay. Is relay_server.py running?", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
