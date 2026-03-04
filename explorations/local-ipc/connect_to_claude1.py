#!/usr/bin/env python3
"""
AUTO-DISCOVERY SCRIPT FOR CLAUDE 2
Run this to find and connect to Claude 1.
Tries all available IPC channels and reports which ones work.

Usage:
    python3 /home/user/claude-sandbox/explorations/local-ipc/connect_to_claude1.py
"""

import socket
import os
import sys

SOCK_PATH = "/home/user/claude-sandbox/explorations/local-ipc/.ipc.sock"
TCP_TARGETS = [
    ("21.0.0.112", 9876),
    ("127.0.0.1", 9876),
    ("127.0.0.1", 9999),
]
PIPE_IN = "/home/user/claude-sandbox/explorations/local-ipc/.pipe_c1_to_c2"
PIPE_OUT = "/home/user/claude-sandbox/explorations/local-ipc/.pipe_c2_to_c1"


def try_unix_socket():
    """Try connecting via Unix domain socket."""
    print("[1] Trying Unix domain socket...", flush=True)
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect(SOCK_PATH)
        s.sendall(b"Hello from Claude 2 via Unix socket!\n")
        try:
            data = s.recv(4096)
            print(f"  RECEIVED: {data.decode().strip()}", flush=True)
        except socket.timeout:
            pass
        s.close()
        print("  SUCCESS: Unix domain socket works!", flush=True)
        return True
    except Exception as e:
        print(f"  FAILED: {e}", flush=True)
        return False


def try_tcp(host, port):
    """Try connecting via TCP."""
    print(f"[2] Trying TCP {host}:{port}...", flush=True)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((host, port))
        s.sendall(b"Hello from Claude 2 via TCP!\n")
        try:
            data = s.recv(4096)
            print(f"  RECEIVED: {data.decode().strip()}", flush=True)
        except socket.timeout:
            pass
        s.close()
        print(f"  SUCCESS: TCP {host}:{port} works!", flush=True)
        return True
    except Exception as e:
        print(f"  FAILED: {e}", flush=True)
        return False


def try_named_pipe():
    """Try reading from named pipe."""
    print("[3] Trying named pipes...", flush=True)
    if not os.path.exists(PIPE_IN):
        print(f"  FAILED: {PIPE_IN} does not exist", flush=True)
        return False
    print(f"  Pipe exists. Trying non-blocking read...", flush=True)
    try:
        fd = os.open(PIPE_IN, os.O_RDONLY | os.O_NONBLOCK)
        try:
            data = os.read(fd, 4096)
            if data:
                print(f"  RECEIVED: {data.decode().strip()}", flush=True)
                print("  SUCCESS: Named pipe works!", flush=True)
                os.close(fd)
                return True
            else:
                print("  No data available (pipe empty or writer not connected)", flush=True)
        except BlockingIOError:
            print("  No data available yet (BlockingIOError)", flush=True)
        os.close(fd)
    except Exception as e:
        print(f"  FAILED: {e}", flush=True)
    return False


def main():
    print("=" * 60, flush=True)
    print("CLAUDE 2: Auto-discovery - finding Claude 1", flush=True)
    print("=" * 60, flush=True)

    success = False

    # Try Unix socket
    if try_unix_socket():
        success = True

    # Try TCP targets
    for host, port in TCP_TARGETS:
        if try_tcp(host, port):
            success = True
            break

    # Try named pipes
    if try_named_pipe():
        success = True

    print("\n" + "=" * 60, flush=True)
    if success:
        print("At least one channel works! Use ipc.py to communicate:", flush=True)
        print("  python3 /home/user/claude-sandbox/explorations/local-ipc/ipc.py listen --once --timeout 120", flush=True)
        print("  python3 /home/user/claude-sandbox/explorations/local-ipc/ipc.py send 'your message'", flush=True)
    else:
        print("No channels worked. Containers likely don't share kernel state.", flush=True)
        print("The IPC mechanisms require shared kernel (socket tables, pipe buffers).", flush=True)
        print("If you got here, the only shared resource is the filesystem itself.", flush=True)
    print("=" * 60, flush=True)


if __name__ == "__main__":
    main()
