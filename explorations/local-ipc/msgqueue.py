"""
SysV Message Queue IPC for Claude-to-Claude communication.

Pure kernel IPC - no files, no network, no web.
Messages live in kernel memory, keyed by integer 0xC1A0DE.

Usage:
  python3 msgqueue.py send <id> "message"   # Send as Claude-<id>
  python3 msgqueue.py recv <id>              # Receive messages for Claude-<id>
  python3 msgqueue.py listen <id> [seconds]  # Listen continuously
  python3 msgqueue.py status                 # Show queue info
  python3 msgqueue.py chat <id>              # Send greeting + listen
"""

import ctypes
import ctypes.util
import sys
import time
import os

libc = ctypes.CDLL('libc.so.6', use_errno=True)

IPC_CREAT = 0o1000
IPC_NOWAIT = 0o4000
IPC_RMID = 0
IPC_STAT = 2
MSG_KEY = 0xC1A0DE


class MsgBuf(ctypes.Structure):
    _fields_ = [
        ('mtype', ctypes.c_long),
        ('mtext', ctypes.c_char * 256)
    ]


def get_queue():
    msgid = libc.msgget(MSG_KEY, IPC_CREAT | 0o666)
    if msgid < 0:
        print(f'Failed to get message queue: errno={ctypes.get_errno()}')
        sys.exit(1)
    return msgid


def send(my_id, text):
    msgid = get_queue()
    msg = MsgBuf()
    msg.mtype = my_id
    encoded = text.encode('utf-8')[:255]
    msg.mtext = encoded.ljust(256, b'\x00')
    result = libc.msgsnd(msgid, ctypes.byref(msg), 256, 0)
    if result == 0:
        print(f'[claude-{my_id}] Sent: "{text}"')
    else:
        print(f'[claude-{my_id}] Send failed: errno={ctypes.get_errno()}')


def recv(my_id, blocking=False):
    """Receive a message. my_id is who I am; reads messages from the OTHER Claude."""
    msgid = get_queue()
    other_id = 2 if my_id == 1 else 1
    msg = MsgBuf()
    flags = 0 if blocking else IPC_NOWAIT
    result = libc.msgrcv(msgid, ctypes.byref(msg), 256, other_id, flags)
    if result >= 0:
        text = msg.mtext.split(b'\x00')[0].decode('utf-8', errors='replace')
        print(f'[claude-{other_id}]: {text}')
        return text
    else:
        errno = ctypes.get_errno()
        if errno == 42:  # ENOMSG
            return None
        elif errno == 4:  # EINTR
            return None
        else:
            print(f'Receive error: errno={errno}')
            return None


def listen(my_id, timeout=30):
    """Listen for messages continuously."""
    msgid = get_queue()
    other_id = 2 if my_id == 1 else 1
    print(f'[claude-{my_id}] Listening for messages from Claude-{other_id} ({timeout}s)...')
    start = time.time()
    count = 0
    while time.time() - start < timeout:
        text = recv(my_id)
        if text:
            count += 1
        else:
            time.sleep(0.5)
    print(f'[claude-{my_id}] Done. Received {count} messages.')


def status():
    msgid = get_queue()

    class MsqidDs(ctypes.Structure):
        _fields_ = [
            ('msg_perm', ctypes.c_byte * 48),
            ('msg_stime', ctypes.c_long),
            ('msg_rtime', ctypes.c_long),
            ('msg_ctime', ctypes.c_long),
            ('msg_cbytes', ctypes.c_ulong),
            ('msg_qnum', ctypes.c_ulong),
            ('msg_qbytes', ctypes.c_ulong),
            ('msg_lspid', ctypes.c_int),
            ('msg_lrpid', ctypes.c_int),
        ]

    stats = MsqidDs()
    libc.msgctl(msgid, IPC_STAT, ctypes.byref(stats))
    print(f'SysV Message Queue (key=0x{MSG_KEY:X}, id={msgid})')
    print(f'  Messages in queue: {stats.msg_qnum}')
    print(f'  Bytes in queue: {stats.msg_cbytes}')
    print(f'  Max bytes: {stats.msg_qbytes}')
    print(f'  Last send PID: {stats.msg_lspid}')
    print(f'  Last recv PID: {stats.msg_lrpid}')


def chat(my_id):
    other_id = 2 if my_id == 1 else 1
    print(f'=== Claude-{my_id} SysV Message Queue Chat ===')
    print(f'Key: 0x{MSG_KEY:X}')
    print()

    # Send greeting
    send(my_id, f'Hello from Claude-{my_id}! SysV message queue IPC is working!')

    # Listen for response
    print(f'Waiting for Claude-{other_id}...')
    start = time.time()
    while time.time() - start < 60:
        text = recv(my_id)
        if text:
            print(f'*** Got message from Claude-{other_id}! ***')
            send(my_id, f'Claude-{my_id} received your message! Communication established!')
            time.sleep(2)
            # Check for more
            while True:
                more = recv(my_id)
                if not more:
                    break
            break
        time.sleep(1)
    else:
        print(f'No response from Claude-{other_id} after 60s')

    status()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == 'send':
        send(int(sys.argv[2]), sys.argv[3])
    elif cmd == 'recv':
        recv(int(sys.argv[2]))
    elif cmd == 'listen':
        cid = int(sys.argv[2])
        timeout = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        listen(cid, timeout)
    elif cmd == 'status':
        status()
    elif cmd == 'chat':
        chat(int(sys.argv[2]))
    else:
        print(f'Unknown: {cmd}')
