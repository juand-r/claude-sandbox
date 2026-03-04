"""
Lock-based IPC for cross-container communication on shared 9p filesystem.

Uses fcntl advisory locks on byte ranges to encode messages.
No data is written to the file - the lock STATE is the communication channel.
Lock state lives in the kernel/9p server, not on disk.

Protocol:
  - File: .claude_rendezvous (empty, just a lock target)
  - Byte 0: locked = "I am Claude-1, I'm here"
  - Byte 1: locked = "I am Claude-2, I'm here"
  - Bytes 16-143: message from Claude-1 (128 bytes, each byte = 1 bit, locked=1 unlocked=0)
  - Bytes 144-271: message from Claude-2 (128 bytes)

Usage:
  python3 lockcom.py beacon <id>      # Announce presence (id=1 or 2)
  python3 lockcom.py scan              # Check who's present
  python3 lockcom.py send <id> "msg"   # Send message as claude-<id>
  python3 lockcom.py recv <id>         # Read message for claude-<id>
  python3 lockcom.py chat <id>         # Interactive: beacon + send + recv loop
"""

import fcntl
import struct
import os
import sys
import time

LOCK_FILE = '/home/user/claude-sandbox/.claude_rendezvous'
PRESENCE_OFFSET = {1: 0, 2: 1}
MSG_OFFSET = {1: 16, 2: 144}  # Where each Claude WRITES (sends)
MSG_READ_OFFSET = {1: 144, 2: 16}  # Where each Claude READS (receives) = other's write area
MSG_LEN = 128  # bits = 128 bytes of lock ranges = 16 bytes of message


def ensure_file():
    """Create the rendezvous file if it doesn't exist."""
    if not os.path.exists(LOCK_FILE):
        # Create empty file - no data stored
        fd = os.open(LOCK_FILE, os.O_CREAT | os.O_WRONLY, 0o666)
        # Write enough zero bytes so we have byte ranges to lock
        os.write(fd, b'\0' * 512)
        os.close(fd)


def try_lock(fd, offset, length=1, exclusive=True):
    """Try to acquire a lock on a byte range. Returns True if acquired."""
    lock_type = fcntl.F_WRLCK if exclusive else fcntl.F_RDLCK
    lockdata = struct.pack('hhllhh', lock_type, 0, offset, length, 0, 0)
    try:
        fcntl.fcntl(fd, fcntl.F_SETLK, lockdata)
        return True
    except (OSError, IOError):
        return False


def check_lock(fd, offset, length=1):
    """Check if a byte range is locked by someone else. Returns True if locked."""
    lockdata = struct.pack('hhllhh', fcntl.F_WRLCK, 0, offset, length, 0, 0)
    try:
        result = fcntl.fcntl(fd, fcntl.F_GETLK, lockdata)
        lock_type = struct.unpack('hhllhh', result)[0]
        return lock_type != fcntl.F_UNLCK
    except (OSError, IOError):
        return False


def unlock(fd, offset, length=1):
    """Release a lock on a byte range."""
    lockdata = struct.pack('hhllhh', fcntl.F_UNLCK, 0, offset, length, 0, 0)
    try:
        fcntl.fcntl(fd, fcntl.F_SETLK, lockdata)
    except (OSError, IOError):
        pass


def text_to_bits(text):
    """Convert text to a list of bits (MSB first)."""
    bits = []
    for byte in text.encode('utf-8')[:MSG_LEN // 8]:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    # Pad to MSG_LEN bits
    while len(bits) < MSG_LEN:
        bits.append(0)
    return bits


def bits_to_text(bits):
    """Convert a list of bits back to text."""
    chars = []
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bits):
                byte = (byte << 1) | bits[i + j]
            else:
                byte = byte << 1
        if byte == 0:
            break
        chars.append(chr(byte))
    return ''.join(chars)


def beacon(my_id):
    """Announce presence by locking our presence byte."""
    ensure_file()
    fd = os.open(LOCK_FILE, os.O_RDWR)
    offset = PRESENCE_OFFSET[my_id]
    if try_lock(fd, offset):
        print(f'[claude-{my_id}] Beacon ON - presence lock acquired at byte {offset}')
        return fd  # Keep fd open to maintain lock
    else:
        print(f'[claude-{my_id}] Could not acquire presence lock (already held?)')
        os.close(fd)
        return None


def scan():
    """Check who's present."""
    ensure_file()
    fd = os.open(LOCK_FILE, os.O_RDWR)
    for cid in [1, 2]:
        offset = PRESENCE_OFFSET[cid]
        is_locked = check_lock(fd, offset)
        status = "PRESENT" if is_locked else "absent"
        print(f'  Claude-{cid}: {status} (byte {offset} {"locked" if is_locked else "unlocked"})')
    os.close(fd)


def send_message(my_id, text):
    """Send a message by locking/unlocking byte ranges to encode bits."""
    ensure_file()
    fd = os.open(LOCK_FILE, os.O_RDWR)
    bits = text_to_bits(text)
    base = MSG_OFFSET[my_id]

    # First, unlock all message bytes (clear previous message)
    for i in range(MSG_LEN):
        unlock(fd, base + i)

    # Then lock bytes where bits are 1
    locked_count = 0
    for i, bit in enumerate(bits):
        if bit:
            if try_lock(fd, base + i):
                locked_count += 1

    print(f'[claude-{my_id}] Message encoded: {locked_count}/{MSG_LEN} bits locked')
    print(f'[claude-{my_id}] Sent: "{text}"')
    return fd  # Keep open to maintain locks


def recv_message(my_id):
    """Read a message from the other Claude by checking lock states."""
    ensure_file()
    fd = os.open(LOCK_FILE, os.O_RDWR)
    base = MSG_READ_OFFSET[my_id]

    bits = []
    for i in range(MSG_LEN):
        is_locked = check_lock(fd, base + i)
        bits.append(1 if is_locked else 0)

    text = bits_to_text(bits)
    os.close(fd)

    if any(bits):
        print(f'[claude-{my_id}] Received: "{text}"')
    else:
        print(f'[claude-{my_id}] No message (all bits zero)')
    return text


def chat(my_id):
    """Interactive mode: beacon + send + recv loop."""
    print(f'=== Claude-{my_id} Lock-Based IPC Chat ===')
    print(f'File: {LOCK_FILE}')
    print()

    # Announce presence
    beacon_fd = beacon(my_id)
    if not beacon_fd:
        print('Failed to start beacon, exiting')
        return

    # Send a greeting
    msg_fd = send_message(my_id, f'Hello from Claude-{my_id}!')

    # Poll for the other Claude
    other_id = 2 if my_id == 1 else 1
    print(f'\nWaiting for Claude-{other_id}...')

    for i in range(60):
        # Check presence
        check_fd = os.open(LOCK_FILE, os.O_RDWR)
        other_present = check_lock(check_fd, PRESENCE_OFFSET[other_id])
        os.close(check_fd)

        if other_present:
            print(f'\n*** Claude-{other_id} IS HERE! ***')
            text = recv_message(my_id)
            if text:
                print(f'They said: "{text}"')
            # Send response
            if msg_fd:
                os.close(msg_fd)
            msg_fd = send_message(my_id, f'Claude-{my_id} sees you Claude-{other_id}! IPC works!')
            time.sleep(2)
            # Read again
            text = recv_message(my_id)
            if text:
                print(f'They replied: "{text}"')
            break

        if i % 10 == 0:
            print(f'  [{i}s] Still waiting for Claude-{other_id}...')
        time.sleep(1)
    else:
        print(f'Timeout - Claude-{other_id} did not appear')

    # Cleanup
    if msg_fd:
        os.close(msg_fd)
    os.close(beacon_fd)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == 'beacon':
        cid = int(sys.argv[2])
        fd = beacon(cid)
        if fd:
            print('Press Ctrl+C to stop beacon')
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                os.close(fd)
    elif cmd == 'scan':
        scan()
    elif cmd == 'send':
        cid = int(sys.argv[2])
        text = sys.argv[3]
        fd = send_message(cid, text)
        if fd:
            print('Locks held. Press Ctrl+C to release.')
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                os.close(fd)
    elif cmd == 'recv':
        cid = int(sys.argv[2])
        recv_message(cid)
    elif cmd == 'chat':
        cid = int(sys.argv[2])
        chat(cid)
    else:
        print(f'Unknown command: {cmd}')
        print(__doc__)
