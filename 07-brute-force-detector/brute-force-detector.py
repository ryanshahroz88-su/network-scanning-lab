#!/usr/bin/env python3
"""
Brute-Force Detector - defence-side, lab-only, beginner version.

Plain words: it reads an SSH log file, counts "Failed password"
lines for each IP, and flags any IP with 5 or more failures.

It also understands syslog's "message repeated N times" lines,
so repeated failures that syslog compressed into one line are
still counted properly.

It only READS the log. It does not attack anything.

How to run (on Kali, with a copied log file):
  python3 brute-force-detector.py sample-auth.log
  python3 brute-force-detector.py /path/to/your-auth.log
"""

import re
import sys
from collections import Counter

# A failed SSH login line looks like:
# Failed password for vagrant from 192.168.10.5 port 22 ssh2
PATTERN = re.compile(r"Failed password .* from (\d+\.\d+\.\d+\.\d+)")

# Syslog sometimes compresses repeats into one line like:
# message repeated 2 times: [ Failed password for vagrant from 192.168.10.5 port 22 ssh2 ]
# That line means the failure happened 2 MORE times after the first
# logged line, so it counts as 2, not 1.
REPEAT_PATTERN = re.compile(
    r"message repeated (\d+) times:.*Failed password .* from (\d+\.\d+\.\d+\.\d+)"
)

def main():
    if len(sys.argv) != 2:
        print("Use: python3 brute-force-detector.py <log-file>")
        sys.exit(1)

    log_file = sys.argv[1]
    counts = Counter()
    try:
        with open(log_file) as f:
            for line in f:
                rm = REPEAT_PATTERN.search(line)
                if rm:
                    counts[rm.group(2)] += int(rm.group(1))
                    continue
                m = PATTERN.search(line)
                if m:
                    counts[m.group(1)] += 1
    except FileNotFoundError:
        print(f"File not found: {log_file}")
        sys.exit(1)

    print("Brute-Force Detector - lab log check")
    print(f"Log file: {log_file}")
    print()
    if not counts:
        print("No failed logins found. Good news - nothing suspicious.")
        return

    print("IP address       Failed logins  Result")
    suspicious = []
    for ip, n in counts.most_common():
        flag = "SUSPICIOUS" if n >= 5 else "ok"
        if n >= 5:
            suspicious.append(ip)
        print(f"{ip:<18} {n:<15} {flag}")

    print()
    if suspicious:
        print(f"Flagged: {', '.join(suspicious)} (5 or more failed logins)")
    else:
        print("No IP reached 5 failed logins.")

    with open("brute-force-report.txt", "w") as out:
        out.write("Brute-Force Detector report\n")
        out.write(f"Log file: {log_file}\n\n")
        for ip, n in counts.most_common():
            out.write(f"{ip}: {n} failed logins\n")
        out.write(f"\nFlagged: {', '.join(suspicious) or 'none'}\n")
    print("Small report saved to brute-force-report.txt")

if __name__ == "__main__":
    main()
