# main.py — C9 Faizan™ Advanced Network Toolkit v3.0
import os
import time
import asyncio  # Asyncio run karne ke liye zaroori hai
from utils.colors import Colors
from modules.tcp_syn import start_syn_flood
from modules.udp_raw import start_udp_raw
from modules.http_adv import start_http_test
from modules.layer7_async import start_async_l7_test  # Sahi tareeqe se import kiya gaya hai

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print(f"""{Colors.RED}
 ██████╗ ██████╗     ███████╗ █████╗ ██╗███████╗ █████╗ ███╗   ██╗
██╔════╝██╔═████╗    ██╔════╝██╔══██╗██║╚══███╔╝██╔══██╗████╗  ██║
██║     ██║██╔██║    █████╗  ███████║██║  ███╔╝ ███████║██╔██╗ ██║
██║     ██╚████║║    ██╔══╝  ██╔══██║██║ ███╔╝  ██╔══██║██║╚██╗██║
╚██████╗╚██████╔╝    ██║     ██║  ██║██║███████╗██║  ██║██║ ╚████║
 ╚═════╝ ╚═════╝     ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝
                {Colors.YELLOW}🔥 C9 Faizan™ Advanced Network Toolkit v3.0 🔥{Colors.END}
    """)

def main():
    while True:
        clear()
        banner()
        print(Colors.info("Educational & Stress Testing Environment Only\n"))
        
        print(f"{Colors.BOLD}Select Real-World Test Method:{Colors.END}")
        print("1. TCP SYN Flood (Advanced Layer-4 Raw Spoofing)")
        print("2. UDP Raw Flood (High-Speed Buffer Stress)")
        print("3. HTTP Application Flood (Layer-7 Threaded Simulation)")
        print("4. Advanced Layer-7 Asynchronous Stress Test (Low & Slow)")
        print("5. Exit\n")
        
        choice = input(">> ")
        
        if choice in ['1', '2', '3', '4']:
            try:
                target = input("Target IP/Host: ")
                port = int(input("Target Port: "))
                duration = int(input("Duration (seconds): "))
                
                if choice == '1':
                    start_syn_flood(target, port, duration)
                elif choice == '2':
                    start_udp_raw(target, port, duration)
                elif choice == '3':
                    threads = int(input("Thread Count (e.g. 50-100): "))
                    start_http_test(target, port, duration, threads)
                elif choice == '4':
                    connections = int(input("Max Async Connections (Recommended: 1000-5000): "))
                    # Python ke async loop ko chalane ka sahi tareeqa
                    asyncio.run(start_async_l7_test(target, port, duration, connections))
                    
            except ValueError:
                print(Colors.error("Invalid input! Ports, Duration, and Threads must be numbers."))
                time.sleep(2)
                
        elif choice == '5':
            print(Colors.success("Exiting Safely. System Secured."))
            break
        else:
            print(Colors.error("Invalid choice, try again."))
            time.sleep(1)

if __name__ == "__main__":
    main()
    
