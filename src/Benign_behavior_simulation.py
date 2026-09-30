import os
import time
import json
import csv
import shutil
import platform
import urllib.request

BASE = "benign_activity_demo"
os.makedirs(BASE, exist_ok=True)

def log(msg):
    print(f"[BENIGN] {msg}")

# ---------------------------------------------------------
# 1. BASIC FILE OPERATIONS
# ---------------------------------------------------------
log("Creating sample files...")
for i in range(10):
    filepath = os.path.join(BASE, f"file_{i}.txt")
    with open(filepath, "w") as f:
        f.write("This is a benign sample file.\n")

log("Reading files...")
for i in range(5):
    filepath = os.path.join(BASE, f"file_{i}.txt")
    with open(filepath, "r") as f:
        data = f.read()

log("Appending text...")
with open(os.path.join(BASE, "file_0.txt"), "a") as f:
    f.write("Appending safe data.\n")

log("Renaming file...")
shutil.copy(os.path.join(BASE, "file_1.txt"), os.path.join(BASE, "copy_of_file_1.txt"))

log("Moving file...")
shutil.move(os.path.join(BASE, "copy_of_file_1.txt"), os.path.join(BASE, "moved_file.txt"))

# ---------------------------------------------------------
# 2. DIRECTORY OPERATIONS
# ---------------------------------------------------------
log("Creating directories...")
for d in ["logs", "temp", "data"]:
    os.makedirs(os.path.join(BASE, d), exist_ok=True)

log("Listing directories...")
dirs = os.listdir(BASE)

# ---------------------------------------------------------
# 3. JSON OPERATIONS
# ---------------------------------------------------------
log("Working with JSON...")
json_path = os.path.join(BASE, "data.json")
with open(json_path, "w") as f:
    json.dump({"status": "ok", "items": [1, 2, 3]}, f)

with open(json_path, "r") as f:
    data = json.load(f)

# ---------------------------------------------------------
# 4. CSV OPERATIONS
# ---------------------------------------------------------
log("Creating CSV...")
csv_path = os.path.join(BASE, "sample.csv")
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "value"])
    for i in range(10):
        writer.writerow([f"item_{i}", i * 10])

log("Reading CSV...")
with open(csv_path, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        pass

# ---------------------------------------------------------
# 5. NETWORK (SAFE REQUEST TO example.com)
# ---------------------------------------------------------
log("Making safe network request...")
try:
    urllib.request.urlopen("http://example.com", timeout=2).read()
except:
    pass

# ---------------------------------------------------------
# 6. SYSTEM INFO
# ---------------------------------------------------------
log("Collecting system info...")
os_name = platform.system()
cpu = platform.processor()
python_ver = platform.python_version()

# ---------------------------------------------------------
# 7. CPU WORKLOAD
# ---------------------------------------------------------
log("Sorting numbers (CPU benign load)...")
arr = list(range(5000, 0, -1))
arr.sort()

log("Performing math operations...")
total = sum(i * i for i in range(10000))

# ---------------------------------------------------------
# 8. Sleep operations
# ---------------------------------------------------------
log("Sleeping...")
time.sleep(1)

log("Benign behavior simulation complete!")
