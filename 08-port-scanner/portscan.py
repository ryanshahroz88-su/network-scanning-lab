#!/usr/bin/env python3
"""PortScan - Your own TCP port scanner.

Scans a target for open TCP ports, grabs service banners,
names the service, and saves a report.

Usage:
    python3 portscan.py 192.168.10.91
    python3 portscan.py 192.168.10.91 -p 1-1000
    python3 portscan.py 192.168.10.91 -p 80
    python3 portscan.py 192.168.10.91 --quick
    python3 portscan.py 192.168.10.91 -p 1-100 -o my-report.txt

Lab use only: scan only machines you own or have permission to test.
"""

import argparse
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    631: "IPP",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Proxy",
}

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 631, 3306, 3389, 8080]


def clean_banner(raw):
    """Keep only readable characters from a banner."""
    return "".join(ch for ch in raw if ch.isprintable()).strip()


def guess_service(port, banner):
    """Guess the service from the port number, then from the banner."""
    service = SERVICES.get(port, "Unknown")
    upper = banner.upper()
    if "SSH" in upper:
        service = "SSH"
    elif "FTP" in upper:
        service = "FTP"
    elif "HTTP" in upper:
        service = "HTTP"
    elif "SMTP" in upper:
        service = "SMTP"
    return service


def scan_port(host, port):
    """Try one TCP port. Returns (is_open, banner)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((host, port))
    banner = ""
    if result == 0:
        try:
            s.settimeout(1)
            banner = clean_banner(s.recv(1024).decode(errors="ignore"))
        except (socket.timeout, OSError):
            banner = ""
    s.close()
    return result == 0, banner


def scan_ports(host, ports, workers):
    """Scan many ports at once with threads. Returns (results, checked)."""
    results = []
    checked = 0
    executor = ThreadPoolExecutor(max_workers=workers)
    try:
        futures = {executor.submit(scan_port, host, p): p for p in ports}
        for future in as_completed(futures):
            port = futures[future]
            checked += 1
            try:
                is_open, banner = future.result()
            except Exception:
                continue
            if is_open:
                results.append((port, banner))
    except KeyboardInterrupt:
        print("\nScan stopped by user. Showing results found so far...")
    finally:
        executor.shutdown(wait=False, cancel_futures=True)
    results.sort()
    return results, checked


def format_result(port, banner):
    """One result line: port, state, service, banner."""
    service = guess_service(port, banner)
    if banner:
        return str(port) + " open - " + service + " - " + banner
    return str(port) + " open - " + service + " - (no banner)"


def parse_ports(text):
    """'1-100' -> (1, 100); '80' -> (80, 80)."""
    if "-" in text:
        start, end = text.split("-", 1)
        return int(start), int(end)
    port = int(text)
    return port, port


def main():
    parser = argparse.ArgumentParser(description="PortScan - Your own TCP port scanner")
    parser.add_argument("target", help="Target IP address or hostname to scan")
    parser.add_argument("-p", "--ports", default="1-100",
                        help="Port range like 1-100 or a single port like 80 (default: 1-100)")
    parser.add_argument("--quick", action="store_true",
                        help="Scan only the most common ports")
    parser.add_argument("-o", "--output", default="portscan-report.txt",
                        help="Report file (default: portscan-report.txt)")
    parser.add_argument("-t", "--threads", type=int, default=50,
                        help="Number of threads (default: 50)")
    args = parser.parse_args()

    try:
        ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print("Could not resolve hostname:", args.target)
        return

    if ip == args.target:
        label = args.target
    else:
        label = args.target + " (" + ip + ")"

    if args.quick:
        ports = list(COMMON_PORTS)
        ports_label = "quick (" + str(len(ports)) + " common ports)"
    else:
        try:
            start, end = parse_ports(args.ports)
        except ValueError:
            print("Invalid port range. Use 1-100 or a single port like 80.")
            return
        if start < 1 or end > 65535 or start > end:
            print("Invalid port range. Use 1-65535, start <= end.")
            return
        ports = list(range(start, end + 1))
        ports_label = str(start) + "-" + str(end)

    workers = max(1, min(args.threads, 200))

    print("Target:", label)
    print("Scanning", label, "ports", ports_label)
    start_time = time.time()
    results, checked = scan_ports(ip, ports, workers)
    elapsed = round(time.time() - start_time, 2)

    lines = []
    lines.append("PortScan Report")
    lines.append("Target: " + label)
    lines.append("Ports: " + ports_label)
    lines.append("Date: " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    lines.append("Time taken: " + str(elapsed) + " seconds")
    lines.append("Threads: " + str(workers))
    lines.append("")
    for port, banner in results:
        line = format_result(port, banner)
        print(line)
        lines.append(line)
    lines.append("")
    summary = "Summary: " + str(len(results)) + " open ports out of " + str(checked) + " scanned."
    lines.append(summary)

    print("Done in", elapsed, "seconds")
    print(summary)
    with open(args.output, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("Report saved to", args.output)


if __name__ == "__main__":
    main()
