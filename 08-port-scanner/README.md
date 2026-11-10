# PortScan — Your Own TCP Port Scanner

PortScan is a TCP port scanner written from scratch in Python. Give it a target
and a port range, and it connects to each port, reads the service banner, names
the service, and saves a clean report.

Built as a PNY Trainings final project (Network Scanning & Enumeration track).
Lab use only — scan only machines you own or have permission to test.

## Features

- Scan a single port, a range (`1-1000`), or `--quick` (14 most common ports)
- Banner grabbing — reads the greeting a service sends when you connect
- Service naming — from a built-in list of well-known ports, confirmed from the banner
- Multi-threaded scanning with `ThreadPoolExecutor` (default 50 workers)
- Clean Ctrl+C — stops the scan and prints/saves what was found so far
- Report file — target, date, timing, results table, and summary
- Hostname support — give a name, it resolves the IP and shows it

## How to run

```bash
python3 portscan.py 192.168.10.162
python3 portscan.py 192.168.10.162 -p 1-1000
python3 portscan.py 192.168.10.162 -p 80
python3 portscan.py 192.168.10.162 --quick
python3 portscan.py 192.168.10.162 -p 1-100 -o my-report.txt
python3 portscan.py 192.168.10.162 -t 100
```

Run `python3 portscan.py --help` to see every option.

## How it works

1. `socket.connect_ex` tries a TCP connection to each port (returns 0 when open).
2. On open ports, `recv` reads up to 1024 bytes — the banner, the service's greeting.
3. The service is guessed from the port number, then confirmed from the banner text.
4. `ThreadPoolExecutor` checks many ports at once instead of one by one.
5. Results print as a table and save to a text report.

## Real lab results (Metasploitable 3, 192.168.10.162)

`--quick` scan (14 common ports, 1.02 seconds):

| Port | State | Service | Banner |
|------|-------|---------|--------|
| 21 | open | FTP | 220 ProFTPD 1.3.5 Server (ProFTPD Default Installation) [192.168.10.162] |
| 22 | open | SSH | SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13 |
| 80 | open | HTTP | (no banner — HTTP waits for a request) |
| 445 | open | SMB | (no banner) |
| 631 | open | IPP | (no banner) |
| 3306 | open | MySQL | Host 'Steve' is not allowed to connect to this MySQL server |
| 8080 | open | HTTP-Proxy | (no banner) |

The MySQL banner is an access-denied error — the service is running, but it
refuses connections from this host. That is still a finding: the port is open
and the service is identified.

A full `1-1000` scan found the same 5 ports in that range (21, 22, 80, 445, 631)
in 20.14 seconds.

## Speed: before and after threads

Same target, same range (ports 1–100):

| Scan | Time |
|------|------|
| One by one | 98.75 seconds |
| With threads (50 workers) | 2.11 seconds |

About 47x faster, with identical results.

## Checked against Nmap

```
nmap -p 21,22,80,445,631,3306,8080 192.168.10.162
```

Nmap reported all 7 ports open (ftp, ssh, http, microsoft-ds, ipp, mysql,
http-proxy) — an exact match with PortScan's `--quick` results.

## Files

- `portscan.py` — the tool (Python 3, standard library only, no extra packages)
- `README.md` — this file
- `sample-report.txt` — a real report from a `--quick` scan of the lab target

## Lab rules

Build and test PortScan only on systems you own or have written permission to
test, inside an isolated lab environment. Never scan a network you do not own.
Scanning without permission is unauthorized access.
