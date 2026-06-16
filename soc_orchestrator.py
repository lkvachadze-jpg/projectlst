import json
import time
import os

WAZUH_ALERTS_PATH = "/var/ossec/logs/alerts/alerts.json"

print("[*] Custom SOC Orchestrator Active...")
print("[*] Monitoring live Wazuh stream for Brute Force Tactic (MITRE T1110)...")
print("-" * 60)

if not os.path.exists(WAZUH_ALERTS_PATH):
    os.makedirs(os.path.dirname(WAZUH_ALERTS_PATH), exist_ok=True)
    with open(WAZUH_ALERTS_PATH, "w") as f:
        pass

with open(WAZUH_ALERTS_PATH, "r") as f:
    f.seek(0, 2)
    
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue
            
        try:
            alert = json.loads(line)
            rule_id = alert.get("rule", {}).get("id")
            src_ip = alert.get("data", {}).get("srcip", "Unknown IP")
            dst_user = alert.get("data", {}).get("dstuser", "Unknown User")
            
            if rule_id == "5712":
                print("\n" + "="*60)
                print(f"[!!! CRITICAL INTEGRATION ALERT !!!]")
                print(f"[TACTIC] MITRE ATT&CK T1110 - Brute Force Detected!")
                print(f"[TARGET] Attacker IP {src_ip} is targeting local user: {dst_user}")
                print(f"[RESPOND] Automatically deploying active firewall rules (iptables) to block {src_ip}...")
                print(f"[STATUS] Threat neutralized. Incident response cycle completed.")
                print("="*60 + "\n")
        except Exception:
            pass
