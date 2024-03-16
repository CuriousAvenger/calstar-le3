import socket
IP_RECV, PORT_RECV = "0.0.0.0", 4444
FILE_PATH = "data.txt"

try:
    while True:
        server = socket.socket(socket.AF_INET)
        server.bind((IP_RECV, PORT_RECV))
        print(f"[RECV] Listening on {IP_RECV}:{PORT_RECV}")

        server.listen(1)
        conn, addr = server.accept()
        print(f"[RECV] COM-DAQ Connection: {addr[0]}:{addr[1]}")
        conn.settimeout(3)
        try:
            print(f"[RECV] Writing Data to {FILE_PATH}\n")
            while True:
                f = open(FILE_PATH, "a")
                f.write(f"{conn.recv(256).decode()}\n")
                f.close()
        except TimeoutError:
            print("[RECV] DAQ Connection Timed Out.")
            print(f"[RECV] Rebinding to {IP_RECV}:{PORT_RECV}")
        finally:
            conn.close()
except KeyboardInterrupt:
    print("[RECV] Keyboard Interrupt Detected.")
    exit(1)
        
