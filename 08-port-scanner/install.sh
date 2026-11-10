#!/bin/bash
# PortScan installer — makes 'portscan' a real command on Kali Linux.
# Run it from the folder where portscan.py is:
#   bash install.sh

set -e

if [ ! -f portscan.py ]; then
  echo "portscan.py not found in this folder."
  echo "Please run this script from the folder that has portscan.py."
  exit 1
fi

cp portscan.py /usr/local/bin/portscan
chmod +x /usr/local/bin/portscan

echo "Installed! 'portscan' is now a command, like nmap."
echo "Try it:"
echo "  portscan 192.168.10.162 --quick"
echo ""
portscan --help
