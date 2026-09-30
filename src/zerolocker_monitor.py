#!/usr/bin/env python3

import sys
import csv
import signal
from datetime import datetime
from bcc import BPF

# Enhanced eBPF program for ransomware-specific monitoring
bpf_code = """
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

struct syscall_data {
    u64 timestamp;
    u64 pid;
    char comm[TASK_COMM_LEN];
    int syscall_nr;
    u64 args[6];
};

BPF_PERF_OUTPUT(events);

// Trace all interesting syscalls
TRACEPOINT_PROBE(raw_syscalls, sys_enter) {
    struct syscall_data data = {};
    
    data.timestamp = bpf_ktime_get_ns();
    data.pid = bpf_get_current_pid_tgid() >> 32;
    data.syscall_nr = args->id;
    
    // Capture first few arguments for file operations
    data.args[0] = args->args[0];
    data.args[1] = args->args[1];
    data.args[2] = args->args[2];

    bpf_get_current_comm(&data.comm, sizeof(data.comm));

    // Filter for interesting processes and syscalls
    if (data.pid > 100) {
        // Focus on file operations and process creation
        if (data.syscall_nr == 2 || data.syscall_nr == 257 ||   // open, openat
            data.syscall_nr == 85 || data.syscall_nr == 133 ||  // creat, mkdir
            data.syscall_nr == 10 || data.syscall_nr == 87 ||   // unlink, unlinkat
            data.syscall_nr == 16 || data.syscall_nr == 72 ||   // lseek, fcntl
            data.syscall_nr == 57 || data.syscall_nr == 56) {   // fork, clone
            events.perf_submit(args, &data, sizeof(data));
        }
    }

    return 0;
}
"""

# Global flag for exit handling
exit_flag = False

def signal_handler(sig, frame):
    global exit_flag
    print("\n[+] Stopping ZeroLocker monitor...")
    exit_flag = True

# Process and log syscall events with ransomware-specific analysis
def print_event(cpu, data, size):
    try:
        event = b["events"].event(data)
    except Exception as e:
        return

    try:
        comm = event.comm.decode('utf-8', 'replace').strip('\x00')
    except:
        comm = "UNKNOWN"

    # Syscall mapping for readability
    syscall_names = {
        2: "open", 3: "close", 5: "fstat", 10: "unlink", 16: "lseek",
        56: "clone", 57: "fork", 85: "creat", 87: "unlinkat", 
        133: "mkdir", 257: "openat", 72: "fcntl"
    }
    
    syscall_name = syscall_names.get(event.syscall_nr, f"syscall_{event.syscall_nr}")

    # Ransomware behavior indicators
    timestamp_readable = datetime.fromtimestamp(event.timestamp / 1e9)
    
    # Check for ZeroLocker-specific patterns
    zerolocker_indicators = ['zero', 'locker', 'encrypt', 'crypt']
    is_suspicious = any(indicator in comm.lower() for indicator in zerolocker_indicators)
    
    # File operation flags
    open_val = 1 if event.syscall_nr in [2, 257] else 0  # open, openat
    create_val = 1 if event.syscall_nr in [85, 133] else 0  # creat, mkdir
    delete_val = 1 if event.syscall_nr in [10, 87] else 0  # unlink, unlinkat
    process_val = 1 if event.syscall_nr in [56, 57] else 0  # fork, clone
    
    # Log to CSV
    row = [
        event.timestamp,
        event.pid,
        comm,
        syscall_name,
        open_val,
        create_val,
        delete_val,
        process_val,
        is_suspicious
    ]

    try:
        with open('zerolocker_analysis2.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)
    except Exception as e:
        pass

    # Show suspicious activities in real-time
    if is_suspicious or event.syscall_nr in [10, 87, 257]:  # unlink, openat are common in encryption
        print(f"[{timestamp_readable}] PID:{event.pid:6} PROCESS:{comm:15} SYSCALL:{syscall_name}")

def main():
    # Handle signals gracefully
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Initialize CSV file
    try:
        with open('zerolocker_analysis2.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['TIMESTAMP_NS', 'PID', 'PROCESS', 'SYSCALL', 
                           'OPEN', 'CREATE', 'DELETE', 'PROCESS_CREATE', 'SUSPICIOUS'])
    except Exception as e:
        print(f"[!] Failed to write CSV header: {e}", file=sys.stderr)
        sys.exit(1)

    # Load eBPF program
    try:
        global b
        b = BPF(text=bpf_code)
    except Exception as e:
        print(f"[!] Failed loading BPF program: {e}", file=sys.stderr)
        sys.exit(1)

    print("timestamp,pid,process_name,syscall,event_details")
    print("[+] ZeroLocker Behavior Monitor Started")
    print("[+] Monitoring for ransomware activities...")
    print("[+] Press Ctrl+C to stop and analyze")

    # Listen for events
    try:
        b["events"].open_perf_buffer(print_event)
        while not exit_flag:
            b.perf_buffer_poll(timeout=1000)
    except Exception as e:
        print(f"\n[!] Error during monitoring: {e}")
    finally:
        print("[+] Monitoring completed")
        print("[+] Data saved to zerolocker_analysis.csv")

if __name__ == "__main__":
    main()
