# network-scanning-lab

7 lab projects on my own VMs, by Steve.

Tools: Nmap, Wireshark, enum4linux, dig, snmpwalk. Lab only.

## Projects

1. **01-network-mapper** — Network Mapper: ping sweep, port scan, service/version detection, network map + inventory.
2. **02-loud-vs-quiet** — Loud vs Quiet: connect / SYN / UDP scans compared in Wireshark.
3. **03-enumeration-deep-dive** — Enumeration Deep-Dive: SMB, DNS zone transfer, SNMP, plus hardening fixes.
4. **04-firewall-evasion** — Firewall Evasion Test: against my own lab firewall.
5. **05-full-network-assessment** — Full Network Assessment: report plus live demo.
6. **06-firewall-evasion-tool** — Firewall Evasion Tester: a small Python tool that runs the 4 Project 4 tests and compares them. Result on 3 Nov 2026: all 4 tests found the same 7 open ports (21, 22, 80, 445, 631, 3306, 8080).
7. **07-brute-force-detector** — Brute-Force Detector: a small Python tool that reads SSH logs, counts failed logins per IP, and flags suspicious IPs. Real result on 4 Nov 2026: my own Kali IP (192.168.10.214) flagged with 6 failed logins.

Folders 01–05 hold that project's final report (PDF); 06 and 07 hold each tool's code, README, and report.
