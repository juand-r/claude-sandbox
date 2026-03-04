#!/usr/bin/env python3
"""
Git-based IPC for Claude-to-Claude communication across containers.

Since containers don't share network or filesystem kernel state,
the only shared resource is the git remote. This tool uses git commits
as a message transport:
- Messages are encoded in commit messages (not in file contents)
- Each Claude polls the other's branch for new commits
- The commit message format: [IPC] <message>
- A small beacon file is updated to create valid commits

Usage:
    python3 git_ipc.py send "Hello from Claude 1!"
    python3 git_ipc.py recv --branch origin/claude/local-ipc-communication-rlxIr
    python3 git_ipc.py poll --branch origin/claude/local-ipc-communication-rlxIr --interval 10
"""

import subprocess
import sys
import time
import argparse
import os

REPO = "/home/user/claude-sandbox"
BEACON_FILE = "explorations/local-ipc/.beacon"
IPC_PREFIX = "[IPC]"


def git(*args, check=True):
    """Run a git command and return output."""
    result = subprocess.run(
        ["git", "-C", REPO] + list(args),
        capture_output=True, text=True, timeout=30
    )
    if check and result.returncode != 0:
        print(f"git error: {result.stderr.strip()}", flush=True)
    return result


def send_message(message, push_branch):
    """Send a message by creating a commit and pushing."""
    beacon_path = os.path.join(REPO, BEACON_FILE)

    # Update beacon file with timestamp to create a valid commit
    with open(beacon_path, "w") as f:
        f.write(f"{time.time()}\n")

    git("add", BEACON_FILE)

    commit_msg = f"{IPC_PREFIX} {message}"
    result = git("commit", "-m", commit_msg)
    if result.returncode != 0:
        print(f"[send] Commit failed: {result.stderr}", flush=True)
        return False

    # Push with retries
    for attempt in range(4):
        result = git("push", "-u", "origin", push_branch)
        if result.returncode == 0:
            print(f"[send] Message sent: {message}", flush=True)
            return True
        wait = 2 ** (attempt + 1)
        print(f"[send] Push failed, retrying in {wait}s...", flush=True)
        time.sleep(wait)

    print("[send] Failed to push after 4 attempts.", flush=True)
    return False


def get_ipc_messages(branch):
    """Get all IPC messages from a branch."""
    result = git("log", branch, "--oneline", "--grep", IPC_PREFIX, check=False)
    if result.returncode != 0:
        return []

    messages = []
    for line in result.stdout.strip().split("\n"):
        if line and IPC_PREFIX in line:
            # Extract message after [IPC]
            idx = line.index(IPC_PREFIX)
            msg = line[idx + len(IPC_PREFIX):].strip()
            commit_hash = line[:idx].strip()
            messages.append((commit_hash, msg))
    return messages


def recv_messages(branch):
    """Fetch and display IPC messages from the other branch."""
    # Fetch latest
    branch_name = branch.replace("origin/", "")
    result = git("fetch", "origin", branch_name)

    messages = get_ipc_messages(branch)
    if messages:
        print(f"[recv] Found {len(messages)} IPC message(s):", flush=True)
        for commit_hash, msg in reversed(messages):
            print(f"  [{commit_hash}] {msg}", flush=True)
    else:
        print("[recv] No IPC messages found.", flush=True)
    return messages


def poll_messages(branch, interval=10, timeout=300):
    """Poll for new IPC messages from the other branch."""
    seen = set()
    branch_name = branch.replace("origin/", "")
    start = time.time()

    print(f"[poll] Watching {branch} for IPC messages (interval={interval}s, timeout={timeout}s)", flush=True)

    while time.time() - start < timeout:
        # Fetch
        git("fetch", "origin", branch_name, check=False)

        messages = get_ipc_messages(branch)
        for commit_hash, msg in messages:
            if commit_hash not in seen:
                seen.add(commit_hash)
                print(f"[new message] {msg}", flush=True)

        time.sleep(interval)

    print("[poll] Timeout reached.", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Git-based IPC")
    sub = parser.add_subparsers(dest="command")

    p_send = sub.add_parser("send")
    p_send.add_argument("message")
    p_send.add_argument("--branch", default=None,
                        help="Branch to push to (auto-detected from current branch)")

    p_recv = sub.add_parser("recv")
    p_recv.add_argument("--branch", required=True, help="Remote branch to read from")

    p_poll = sub.add_parser("poll")
    p_poll.add_argument("--branch", required=True, help="Remote branch to watch")
    p_poll.add_argument("--interval", type=int, default=10)
    p_poll.add_argument("--timeout", type=int, default=300)

    args = parser.parse_args()

    if args.command == "send":
        branch = args.branch
        if not branch:
            result = git("branch", "--show-current")
            branch = result.stdout.strip()
        send_message(args.message, branch)
    elif args.command == "recv":
        recv_messages(args.branch)
    elif args.command == "poll":
        poll_messages(args.branch, args.interval, args.timeout)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
