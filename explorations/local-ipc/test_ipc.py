#!/usr/bin/env python3
"""
Self-contained test: starts relay, connects two clients, exchanges messages.
"""

import socket
import threading
import time
import sys

PORT = 9998  # Use a different port to avoid conflicts

results = []
errors = []


def relay_server(ready_event, stop_event):
    """Minimal relay server for testing."""
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", PORT))
    srv.listen(2)
    srv.settimeout(1.0)
    ready_event.set()

    clients = []
    try:
        # Accept two clients
        while len(clients) < 2 and not stop_event.is_set():
            try:
                conn, addr = srv.accept()
                conn.setblocking(True)
                conn.settimeout(5.0)
                clients.append(conn)
            except socket.timeout:
                continue

        if len(clients) < 2:
            return

        # Simple relay loop: read from each, forward to other
        # Run two relay threads
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

        t1 = threading.Thread(target=relay, args=(clients[0], clients[1], "0->1"))
        t2 = threading.Thread(target=relay, args=(clients[1], clients[0], "1->0"))
        t1.daemon = True
        t2.daemon = True
        t1.start()
        t2.start()

        # Wait until test is done
        stop_event.wait(timeout=10)

    finally:
        for c in clients:
            try:
                c.close()
            except OSError:
                pass
        srv.close()


def client_a(ready_event):
    """Client A: waits for both connected, sends message, reads reply."""
    ready_event.wait(timeout=5)
    time.sleep(0.5)
    try:
        s = socket.socket()
        s.connect(("127.0.0.1", PORT))
        s.settimeout(5)
        time.sleep(1)  # Let client B connect too
        s.sendall(b"Hello from A\n")
        data = s.recv(4096)
        results.append(("A_received", data.decode().strip()))
        s.close()
    except Exception as e:
        errors.append(f"client_a: {e}")


def client_b(ready_event):
    """Client B: connects, reads message from A, sends reply."""
    ready_event.wait(timeout=5)
    time.sleep(0.5)
    try:
        s = socket.socket()
        s.connect(("127.0.0.1", PORT))
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

    server_thread = threading.Thread(target=relay_server, args=(ready, stop))
    server_thread.daemon = True
    server_thread.start()

    ta = threading.Thread(target=client_a, args=(ready,))
    tb = threading.Thread(target=client_b, args=(ready,))
    ta.start()
    tb.start()

    ta.join(timeout=15)
    tb.join(timeout=15)

    stop.set()
    server_thread.join(timeout=3)

    print("=== TEST RESULTS ===")
    if errors:
        print(f"ERRORS: {errors}")
    for label, msg in results:
        print(f"  {label}: {msg}")

    # Verify
    b_got_a = any(label == "B_received" and "Hello from A" in msg for label, msg in results)
    a_got_b = any(label == "A_received" and "Reply from B" in msg for label, msg in results)

    if b_got_a and a_got_b:
        print("\nSUCCESS: Bidirectional communication works!")
        sys.exit(0)
    else:
        print(f"\nFAILURE: b_got_a={b_got_a}, a_got_b={a_got_b}")
        sys.exit(1)


if __name__ == "__main__":
    main()
