#!/usr/bin/env python3
import os
import random
import subprocess
import time
import socket
import hashlib
from datetime import datetime

LOG_FILE = "benign_behavior.log"

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(msg)

# ------------------------------------------------------------
#  BENIGN ACTIONS
# ------------------------------------------------------------

def create_temp_files():
    """Create many small random files."""
    folder = "benign_temp"
    os.makedirs(folder, exist_ok=True)

    for i in range(random.randint(5, 15)):
        filename = os.path.join(folder, f"file_{i}.txt")
        with open(filename, "w") as f:
            f.write("This is a benign test file.\n" * random.randint(1, 5))
        log(f"Created temp file {filename}")

def read_various_files():
    """Read harmless files from /usr, /etc."""
    paths = [
        "/etc/hostname",
        "/etc/passwd",
        "/etc/services",
        "/usr/share/dict/words",
    ]

    for p in paths:
        if os.path.exists(p):
            try:
                with open(p) as f:
                    f.read(200)
                log(f"Read file {p}")
            except:
                pass

def run_common_commands():
    """Run normal Linux utilities."""
    commands = [
        ["ls", "-l"],
        ["whoami"],
        ["id"],
        ["uname", "-a"],
        ["df", "-h"],
        ["ps", "aux"],
        ["uptime"],
    ]

    cmd = random.choice(commands)
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log(f"Executed command: {' '.join(cmd)}")
    except:
        pass

def network_dns_lookup():
    """Do a safe DNS lookup."""
    try:
        socket.gethostbyname("example.com")
        log("Performed DNS lookup for example.com")
    except:
        pass

def network_http_request():
    """Open a simple socket connection to generate benign net activity."""
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect(("example.com", 80))
        s.send(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
        s.close()
        log("Made simple HTTP request to example.com")
    except:
        pass

def hash_files():
    """Compute harmless SHA256 hashes of small files."""
    folder = "benign_temp"
    if not os.path.exists(folder):
        return
    
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        try:
            with open(path, "rb") as f:
                hashlib.sha256(f.read()).hexdigest()
            log(f"Computed SHA256 hash for {path}")
        except:
            pass

def write_random_logs():
    """Write some log-like entries."""
    for _ in range(5):
        with open("benign_custom_log.txt", "a") as f:
            f.write(f"Log entry {random.randint(1000,9999)}\n")
        log("Wrote random log entry")

def simulate_user_editing():
    """Pretend user edits a file."""
    fname = "notes.txt"
    with open(fname, "a") as f:
        f.write(f"User typed something at {datetime.now()}\n")
    log(f"Edited file {fname}")

def simulate_python_process():
    """Run a small python sub‑process."""
    script = "print('benign sub-process')"
    try:
        subprocess.run(["python3", "-c", script], stdout=subprocess.DEVNULL)
        log("Executed small Python sub-process")
    except:
        pass

def list_large_dirs():
    """List large system directories."""
    dirs = ["/usr/bin", "/etc", "/home"]
    d = random.choice(dirs)
    try:
        os.listdir(d)
        log(f"Listed directory {d}")
    except:
        pass

# ------------------------------------------------------------
#  MAIN LOOP
# ------------------------------------------------------------
ACTIONS = [
    create_temp_files,
    read_various_files,
    run_common_commands,
    network_dns_lookup,
    network_http_request,
    hash_files,
    write_random_logs,
    simulate_user_editing,
    simulate_python_process,
    list_large_dirs,
]

def run_benign_generator(iterations=50):
    log("=== Starting Benign Behavior Generator ===")

    for i in range(iterations):
        action = random.choice(ACTIONS)
        log(f"Running action #{i+1}: {action.__name__}")
        
        action()
        time.sleep(random.uniform(0.05, 0.4))  # fast but varied

    log("=== Finished Generating Benign Activity ===")

if __name__ == "__main__":
    run_benign_generator(iterations=150)
