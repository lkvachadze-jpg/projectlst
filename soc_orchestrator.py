import os
import sys
import time
import json
import subprocess

log_path = "/var/ossec/logs/alerts/alerts.json"

print("--- starting soc script ---")
print("monitoring for ssh brute force...")

while not os.path.exists(log_path):
    print("waiting for alerts.json file...")
    time.sleep(5)

print("found file, starting loop.")

with open(log_path, "r") as f:
    f.seek(0, 2)
    
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue
            
        try:
            data = json.loads(line)
            rule = data["rule"]["id"]
            
            if rule == "5712":
                ip = data["data"]["srcip"]
                user = data["data"].get("dstuser", "unknown")
                
                print(f"\n!!! ALERT !!!")
                print(f"Brute force detected from IP: {ip} (Target user: {user})")
                print(f"Blocking {ip} using iptables...")
                
                cmd = f"sudo iptables -A INPUT -s {ip} -j DROP"
                subprocess.run(cmd, shell=True, check=True)
                
                print(f"IP {ip} successfully blocked.\n")
                
        except:
            pass
