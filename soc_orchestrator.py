import json
import os
import subprocess
import time

WAZUH_ALERTS = "/var/ossec/logs/alerts/alerts.json"

print("[*] Starting Integrated SOC Orchestrator...")
print("[*] Monitoring Wazuh alerts for SSH Brute Force (MITRE T1110)...")
print("-" * 60)

if not os.path.exists(WAZUH_ALERTS):
    os.makedirs(os.path.dirname(WAZUH_ALERTS), exist_ok=True)
    open(WAZUH_ALERTS, "w").close()

with open(WAZUH_ALERTS, "r") as f:
    f.seek(0, 2)

    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue

        try:
            alert = json.loads(line)
            rule_id = alert.get("rule", {}).get("id")

            if rule_id == "5712":
                src_ip = alert.get("data", {}).get("srcip", "Unknown IP")
                dst_user = alert.get("data", {}).get("dstuser", "Unknown User")

                print("\n" + "=" * 50)
                print(f"[ALERT] SECURITY EVENT DETECTED")
                print(f"[TACTIC] MITRE ATT&CK T1110 - Brute Force Attempt")
                print(f"[TARGET] Attacker IP {src_ip} targeted account: {dst_user}")
                print(f"[ACTION] Executing Linux firewall block on IP: {src_ip}...")

                subprocess.run(
                    ["sudo", "iptables", "-A", "INPUT", "-s", src_ip, "-j", "DROP"]
                )

                print("[STATUS] Firewall rules updated successfully. Threat neutralized.")
                print("=" * 50 + "\n")

        except Exception:
            pass

import json
import os
import subprocess
import time

WAZUH_ALERTS = "/var/ossec/logs/alerts/alerts.json"

print("[*] Starting Integrated SOC Orchestrator...")
print("[*] Monitoring Wazuh alerts for SSH Brute Force (MITRE T1110)...")
print("-" * 60)

while not os.path.exists(WAZUH_ALERTS):
    print("[*] Waiting for Wazuh to create alerts.json... Checking again in 5 seconds.")
    time.sleep(5)

print("[+] Found alerts.json. Starting log tailing...")

with open(WAZUH_ALERTS, "r") as f:
    f.seek(0, 2)

    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue

        try:
            alert = json.loads(line)
            rule_id = alert.get("rule", {}).get("id")

            if rule_id == "5712":
                src_ip = alert.get("data", {}).get("srcip", "Unknown IP")
                dst_user = alert.get("data", {}).get("dstuser", "Unknown User")

                print("\n" + "=" * 50)
                print(f"[ALERT] SECURITY EVENT DETECTED")
                print(f"[TACTIC] MITRE ATT&CK T1110 - Brute Force Attempt")
                print(f"[TARGET] Attacker IP {src_ip} targeted account: {dst_user}")
                print(f"[ACTION] Executing Linux firewall block on IP: {src_ip}...")

                subprocess.run(
                    ["sudo", "iptables", "-A", "INPUT", "-s", src_ip, "-j", "DROP"],
                    check=True
                )

                print("[STATUS] Firewall rules updated successfully. Threat neutralized.")
                print("=" * 50 + "\n")

        except Exception:
            pass
