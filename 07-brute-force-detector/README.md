# Brute-Force Detector

A small defence-side, lab-only Python tool. It reads an SSH log file, counts failed logins per IP, and flags any IP with 5 or more failed attempts.

It only reads the log. It does not attack anything.

## How to run

```bash
python3 brute-force-detector.py sample-auth.log
python3 brute-force-detector.py /path/to/your-auth.log
```

It prints a small table and saves a short report (`brute-force-report.txt`).

## Real result (my own lab, 4 Nov 2026)

Run on the real `auth.log` from my own Metasploitable 3 VM. I made the failed logins myself, from my own Kali machine, to test the detector:

- `192.168.10.214` (my Kali machine): 6 failed logins — flagged as SUSPICIOUS

The detector caught my own attack — that was the whole point of the test.

Note: this log also taught the tool something. Syslog compresses repeated lines into `message repeated 2 times`, and the first version of the tool undercounted those (4 instead of 6). The tool now counts repeated lines properly.

A sample log (`sample-auth.log`) is included if you want to try the tool without your own log file.

## Rules

- Lab VMs only, on your own machines.
- Never run it on real networks or machines you do not own.
