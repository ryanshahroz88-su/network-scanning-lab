# network-scanning-lab

5 lab projects on my own VMs, by Steve.

Tools: Nmap, Wireshark, enum4linux, dig, snmpwalk. Lab only.

## Projects

1. **01-network-mapper** — Network Mapper: ping sweep, port scan, service/version detection, network map + inventory.
2. **02-loud-vs-quiet** — Loud vs Quiet: connect / SYN / UDP scans compared in Wireshark.
3. **03-enumeration-deep-dive** — Enumeration Deep-Dive: SMB, DNS zone transfer, SNMP, plus hardening fixes.
4. **04-firewall-evasion** — Firewall Evasion Test: against my own lab firewall.
5. **05-full-network-assessment** — Full Network Assessment: report plus live demo.

Each folder holds that project's final report (PDF).

## Tools I built

The tools now live in their own repositories:

- **[firewall-evasion-tool](https://github.com/ryanshahroz88-su/firewall-evasion-tool)** — runs the 4 Project 4 tests and compares them.
- **[brute-force-detector](https://github.com/ryanshahroz88-su/brute-force-detector)** — reads SSH logs, counts failed logins per IP, and flags suspicious IPs.
- **[port-scanner](https://github.com/ryanshahroz88-su/port-scanner)** — a TCP port scanner built from scratch in Python.
