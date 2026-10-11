#!/usr/bin/env python3
import sys
import subprocess

print(r"""
                           
                           
 .-.   .--.   .    .  .--. 
(   )  |   )  |\  /|  |   )
 `-.   |--'   | \/ |  |--' 
(   )  |  \   |    |  |  \ 
 `-'   '   `  '    '  '   `
                           
                           

    Speed Run My Recon
        by nmesoma0x
""")

addr = sys.argv[1] if len(sys.argv) > 1 else input("input ip: ")

if not addr:
    print("Error: No target provided.")
    raise SystemExit(1)

print(f"\n[*] Pinging {addr}...\n")
subprocess.run(["ping", "-c", "4", addr])

print(f"\n[*] Scanning {addr} with Nmap...\n")
subprocess.run(["nmap", "-sV", addr])

