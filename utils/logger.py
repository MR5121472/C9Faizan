# utils/logger.py — Advanced Logging
import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "attack_log.txt")

def log_attack(method, target, port, duration):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{now}] Method: {method} | Target: {target}:{port} | Duration: {duration}s\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)
        f.flush()
      
