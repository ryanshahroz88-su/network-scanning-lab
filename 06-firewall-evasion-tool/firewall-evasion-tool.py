#!/usr/bin/env python3
"""
Lab-only firewall evasion tester (like PNY Project 4).

What it does, in plain words:
  1. Runs a normal Nmap scan on your lab target.
  2. Runs the same scan 3 tricky ways: small pieces, fake friends, slow.
  3. Counts the open doors in each scan and shows a small table.
  4. Saves every scan + one summary report file.

Use ONLY on your own lab VMs (example: 192.168.10.91).
It refuses public internet IPs on purpose.
It does NOT break through a firewall - it only tests and compares.

How to run on Kali:
  python3 firewall-evasion-tool.py 192.168.10.91
  python3 firewall-evasion-tool.py 192.168.10.91 --only fragment
"""

import argparse
import datetime
import ipaddress
import re
import shutil
import subprocess
import sys


def is_lab_ip(target):
    """Only allow private lab IPs like 192.168.x.x or 10.x.x.x."""
    try:
        ip = ipaddress.ip_address(target)
    except ValueError:
        return False
    return ip.is_private


def run_scan(name, command):
    """Run one nmap scan, save it, and count open ports."""
    print(f"\n--- {name} ---")
    print("Running:", " ".join(command))
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout + result.stderr
    filename = f"{name}.txt"
    with open(filename, "w") as f:
        f.write(output)
    # Find lines like "80/tcp  open"
    open_ports = re.findall(r"(\d+)/tcp\s+open", output)
    print(f"Open ports found: {len(open_ports)} -> {', '.join(open_ports) or 'none'}")
    print(f"Saved to {filename}")
    return open_ports


def main():
    parser = argparse.ArgumentParser(description="Lab-only firewall evasion tester")
    parser.add_argument("target", help="Lab target IP, example: 192.168.10.91")
    parser.add_argument(
        "--only",
        choices=["baseline", "fragment", "decoy", "timing"],
        help="Run just one test instead of all four",
    )
    args = parser.parse_args()

    if shutil.which("nmap") is None:
        print("Error: nmap is not installed on this machine.")
        sys.exit(1)

    if not is_lab_ip(args.target):
        print("Stopped: this tool only works on private lab IPs")
        print("(like 192.168.x.x or 10.x.x.x). Public IPs are not allowed.")
        sys.exit(1)

    print("Lab-only firewall evasion tester")
    print(f"Target: {args.target}")
    print("Note: this tests and compares. It does not break a firewall.")

    # name -> nmap command
    scans = {
        "baseline": ["nmap", args.target],
        "fragment": ["nmap", "-f", args.target],
        "decoy": ["nmap", "-D", "RND:5", args.target],
        "timing": ["nmap", "-T2", "--top-ports", "100", args.target],
    }

    if args.only:
        scans = {args.only: scans[args.only]}

    results = {}
    for name, command in scans.items():
        results[name] = run_scan(name, command)

    # Small comparison table
    print("\n=== Comparison ===")
    print(f"{'Test':<12} {'Open ports':<12} Ports")
    for name, ports in results.items():
        print(f"{name:<12} {len(ports):<12} {', '.join(ports) or 'none'}")

    # Save one summary report
    report = "evasion-report.txt"
    with open(report, "w") as f:
        f.write("Lab-only firewall evasion test\n")
        f.write(f"Target: {args.target}\n")
        f.write(f"Date: {datetime.datetime.now()}\n\n")
        for name, ports in results.items():
            f.write(f"{name}: {len(ports)} open -> {', '.join(ports) or 'none'}\n")
    print(f"\nSummary saved to {report}")
    print("Done!")


if __name__ == "__main__":
    main()
