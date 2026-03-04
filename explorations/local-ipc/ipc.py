"""
Local IPC for Claude-to-Claude communication via TCP on localhost.
No disk I/O involved - all data flows through kernel memory.

Usage:
    Server (first Claude):  python3 ipc.py server
    Client (second Claude): python3 ipc.py client
    Send a message:         python3 ipc.py send "hello from Claude 1"
    Read messages:          python3 ipc.py recv
    Check status:           python3 ipc.py status

Protocol: TCP on localhost:12321, newline-delimited JSON messages.
"""

import socket
import json
import sys
import threading
import time
import select

PORT = 12321
HOST = '0.0.0.0'
BUFSIZE = 4096


def make_message(sender, text):
    return json.dumps({
        "sender": sender,
        "text": text,
        "timestamp": time.time()
    }) + "\n"


def parse_message(raw):
    try:
        return json.loads(raw.strip())
    except (json.JSONDecodeError, ValueError):
        return None


class MessageServer:
    """TCP server that relays messages between connected Claude instances."""

    def __init__(self):
        self.clients = {}  # socket -> name
        self.lock = threading.Lock()
        self.messages = []  # message log (in memory only)

    def broadcast(self, msg_dict, exclude=None):
        """Send a message to all connected clients except the sender."""
        raw = json.dumps(msg_dict) + "\n"
        with self.lock:
            for sock, name in list(self.clients.items()):
                if sock is not exclude:
                    try:
                        sock.sendall(raw.encode())
                    except (BrokenPipeError, ConnectionResetError, OSError):
                        self._remove_client(sock)

    def _remove_client(self, sock):
        name = self.clients.pop(sock, "unknown")
        print(f"[server] Client '{name}' disconnected")
        try:
            sock.close()
        except OSError:
            pass

    def handle_client(self, conn, addr):
        """Handle a single client connection."""
        buffer = ""
        name = f"client-{addr[1]}"

        with self.lock:
            self.clients[conn] = name

        print(f"[server] New connection from {addr}, assigned name '{name}'")

        # Send welcome + any buffered messages
        welcome = make_message("server", f"Welcome, {name}. You are connected. Send 'IDENTIFY <name>' to set your name.")
        conn.sendall(welcome.encode())

        # Send message history
        with self.lock:
            for msg in self.messages:
                conn.sendall((json.dumps(msg) + "\n").encode())

        try:
            while True:
                ready, _, _ = select.select([conn], [], [], 1.0)
                if not ready:
                    continue

                data = conn.recv(BUFSIZE)
                if not data:
                    break

                buffer += data.decode()
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    msg = parse_message(line)
                    if msg is None:
                        # Treat as plain text
                        msg = {"sender": name, "text": line.strip(), "timestamp": time.time()}

                    # Handle IDENTIFY command
                    if msg.get("text", "").startswith("IDENTIFY "):
                        old_name = name
                        name = msg["text"].split(" ", 1)[1]
                        with self.lock:
                            self.clients[conn] = name
                        print(f"[server] '{old_name}' identified as '{name}'")
                        ack = make_message("server", f"You are now known as '{name}'")
                        conn.sendall(ack.encode())
                        continue

                    # Store and broadcast
                    msg["sender"] = name
                    with self.lock:
                        self.messages.append(msg)
                    print(f"[server] [{name}]: {msg.get('text', '')}")
                    self.broadcast(msg, exclude=conn)

                    # Send ack back to sender
                    ack = make_message("server", f"Message received: '{msg.get('text', '')}'")
                    conn.sendall(ack.encode())

        except (ConnectionResetError, BrokenPipeError, OSError) as e:
            print(f"[server] Client '{name}' error: {e}")
        finally:
            with self.lock:
                self._remove_client(conn)

    def run(self):
        """Start the server."""
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(5)
        print(f"[server] Listening on {HOST}:{PORT}")
        print(f"[server] Waiting for Claude instances to connect...")

        try:
            while True:
                conn, addr = srv.accept()
                t = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print("\n[server] Shutting down")
        finally:
            srv.close()


def send_message(sender, text):
    """Connect, send one message, print response, disconnect."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
        # Read welcome
        welcome = sock.recv(BUFSIZE).decode()
        for line in welcome.strip().split("\n"):
            msg = parse_message(line)
            if msg:
                print(f"[{msg['sender']}]: {msg['text']}")

        # Identify
        sock.sendall(make_message(sender, f"IDENTIFY {sender}").encode())
        time.sleep(0.1)
        ack_data = sock.recv(BUFSIZE).decode()
        for line in ack_data.strip().split("\n"):
            msg = parse_message(line)
            if msg:
                print(f"[{msg['sender']}]: {msg['text']}")

        # Send the actual message
        sock.sendall(make_message(sender, text).encode())
        time.sleep(0.2)

        # Read response
        sock.settimeout(1.0)
        try:
            resp = sock.recv(BUFSIZE).decode()
            for line in resp.strip().split("\n"):
                msg = parse_message(line)
                if msg:
                    print(f"[{msg['sender']}]: {msg['text']}")
        except socket.timeout:
            pass

        print(f"[{sender}] Message sent successfully.")
    except ConnectionRefusedError:
        print(f"[error] No server running on {HOST}:{PORT}. Start the server first.")
        sys.exit(1)
    finally:
        sock.close()


def recv_messages(name, timeout=5):
    """Connect and listen for messages for `timeout` seconds."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
        # Read welcome + history
        time.sleep(0.2)
        data = sock.recv(BUFSIZE).decode()
        for line in data.strip().split("\n"):
            msg = parse_message(line)
            if msg:
                print(f"[{msg['sender']}]: {msg['text']}")

        # Identify
        sock.sendall(make_message(name, f"IDENTIFY {name}").encode())
        time.sleep(0.1)
        try:
            ack = sock.recv(BUFSIZE).decode()
            for line in ack.strip().split("\n"):
                msg = parse_message(line)
                if msg:
                    print(f"[{msg['sender']}]: {msg['text']}")
        except Exception:
            pass

        # Listen for new messages
        print(f"[{name}] Listening for messages ({timeout}s timeout)...")
        sock.settimeout(1.0)
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                data = sock.recv(BUFSIZE).decode()
                if not data:
                    break
                for line in data.strip().split("\n"):
                    msg = parse_message(line)
                    if msg:
                        print(f"[{msg['sender']}]: {msg['text']}")
            except socket.timeout:
                continue
        print(f"[{name}] Done listening.")
    except ConnectionRefusedError:
        print(f"[error] No server running on {HOST}:{PORT}.")
        sys.exit(1)
    finally:
        sock.close()


def check_status():
    """Check if the server is running."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.settimeout(1.0)
        sock.connect((HOST, PORT))
        data = sock.recv(BUFSIZE).decode()
        print(f"Server is running on {HOST}:{PORT}")
        for line in data.strip().split("\n"):
            msg = parse_message(line)
            if msg:
                print(f"  {msg['text']}")
        sock.close()
        return True
    except (ConnectionRefusedError, socket.timeout, OSError):
        print(f"No server running on {HOST}:{PORT}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "server":
        MessageServer().run()
    elif cmd == "send":
        sender = sys.argv[2] if len(sys.argv) > 3 else "claude-2"
        text = sys.argv[3] if len(sys.argv) > 3 else sys.argv[2]
        send_message(sender, text)
    elif cmd == "recv":
        name = sys.argv[2] if len(sys.argv) > 2 else "claude-2"
        timeout = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        recv_messages(name, timeout)
    elif cmd == "status":
        check_status()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)
