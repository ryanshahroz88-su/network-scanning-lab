# Firewall Evasion Tester

A small lab-only Python tool, built after PNY Project 4 (Firewall Evasion Test).

## What it does

It runs 4 Nmap scans on a lab target and compares them in a small table:

1. **baseline** — a normal scan
2. **fragment** — the scan broken into small pieces (`-f`)
3. **decoy** — the scan hidden among fake sources (`-D RND:5`)
4. **timing** — a slow, quiet scan (`-T2`, top 100 ports)

It saves every scan plus one summary report (`evasion-report.txt`).

## How to run

```bash
python3 firewall-evasion-tool.py 192.168.10.91
```

Run just one test:

```bash
python3 firewall-evasion-tool.py 192.168.10.91 --only fragment
```

## Result (3 Nov 2026, Metasploitable 3 at 192.168.10.91)

All 4 tests found the same 7 open ports: **21, 22, 80, 445, 631, 3306, 8080**.

Lesson: the evasion tricks changed nothing — the firewall sees through all of them.

## Rules

- Lab VMs only. The tool refuses public internet IPs on purpose.
- Never run it on real networks or machines you do not own.
