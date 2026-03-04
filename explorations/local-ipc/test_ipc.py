#!/usr/bin/env python3
"""
Self-contained test for Unix domain socket IPC.
"""

import socket
import threading
import time
import os
import sys

SOCK_PATH = "/home/user/claude-sandbox/explorations/local-ipc/.test.sock"

results = []
errors = []


def relay_server(ready_event, stop_event):
    """Minimal relay for testing."""
    if os.path.exists(SOCK_PATH):
        os.unlink(SOCK_PATH)
    srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    srv.bind(SOCK_PATH)
    srv.listen(2)
    srv.settimeout(1.0)
    ready_event.set()

    clients = []
    try:
        while len(clients) < 2 and not stop_event.is_set():
            try:
                conn, _ = srv.accept()
                conn.setblocking(True)
                conn.settimeout(5.0)
                clients.append(conn)
            except socket.timeout:
                continue

        if len(clients) < 2:
            return

        def relay(src, dst, label):
            try:
                while not stop_event.is_set():
                    try:
                        data = src.recv(4096)
                        if not data:
                            break
                        dst.sendall(data)
                    except socket.timeout:
                        continue
                    except OSError:
                        break
            except Exception as e:
                errors.append(f"relay_{label}: {e}")

        t1 = threading.Thread(target=relay, args=(clients[0], clients[1], "0->1"), daemon=True)
        t2 = threading.Thread(target=relay, args=(clients[1], clients[0], "1->0"), daemon=True)
        t1.start()
        t2.start()
        stop_event.wait(timeout=10)
    finally:
        for c in clients:
            try:
                c.close()
            except OSError:
                pass
        srv.close()
        if os.path.exists(SOCK_PATH):
            os.unlink(SOCK_PATH)


def client_a(ready_event):
    ready_event.wait(timeout=5)
    time.sleep(0.5)
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(SOCK_PATH)
        s.settimeout(5)
        time.sleep(1)
        s.sendall(b"Hello from A\n")
        data = s.recv(4096)
        results.append(("A_received", data.decode().strip()))
        s.close()
    except Exception as e:
        errors.append(f"client_a: {e}")


def client_b(ready_event):
    ready_event.wait(timeout=5)
    time.sleep(0.5)
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(SOCK_PATH)
        s.settimeout(5)
        data = s.recv(4096)
        results.append(("B_received", data.decode().strip()))
        s.sendall(b"Reply from B\n")
        time.sleep(0.5)
        s.close()
    except Exception as e:
        errors.append(f"client_b: {e}")


def main():
    ready = threading.Event()
    stop = threading.Event()

    threads = [
        threading.Thread(target=relay_server, args=(ready, stop), daemon=True),
        threading.Thread(target=client_a, args=(ready,)),
        threading.Thread(target=client_b, args=(ready,)),
    ]
    for t in threads:
        t.start()
    for t in threads[1:]:
        t.join(timeout=15)

    stop.set()
    threads[0].join(timeout=3)

    print("=== TEST RESULTS ===")
    if errors:
        print(f"ERRORS: {errors}")
    for label, msg in results:
        print(f"  {label}: {msg}")

    b_got_a = any(label == "B_received" and "Hello from A" in msg for label, msg in results)
    a_got_b = any(label == "A_received" and "Reply from B" in msg for label, msg in results)

    if b_got_a and a_got_b:
        print("\nSUCCESS: Unix domain socket IPC works!")
        sys.exit(0)
    else:
        print(f"\nFAILURE: b_got_a={b_got_a}, a_got_b={a_got_b}")
        sys.exit(1)


if __name__ == "__main__":
    main()
