import socket
IP_SEND, PORT_SEND = "192.168.174.228", 4445

try:
    while True:
        while True:
            try:
                client = socket.socket(socket.AF_INET)
                print(f"[SEND] Connecting to {IP_SEND}:{PORT_SEND}")
                client.connect((IP_SEND, PORT_SEND))
                break
            except TimeoutError:
                print(f"[SEND] Connection Timed Out")
        
        print(f"[SEND] Connected to {IP_SEND}:{PORT_SEND}")
        try:
            while True:
                command = input("[SEND] Enter Command: ")
                client.send(command.encode())       
        except Exception:
            print(f"[SEND] Reconnecting to {IP_SEND}:{PORT_SEND}")
        finally:
            client.close()
except KeyboardInterrupt:
    print("\n[SEND] Keyboard Interrupt Detected.")
    exit(1)
        
