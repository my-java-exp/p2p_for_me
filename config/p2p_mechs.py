import socket as s
import threading
import shlex

from config.p2p_dataclass import server_dataclass
from config.p2p_funcs import log, returnFileType, lambda_log
from config.p2p_commands import server_commands, client_commands

# Client code
class P2PClient:
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)

        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    
    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            log(f"Connected to server at {self.host}:{self.port}")

            while True:
                command = input("> ")

                if command.upper() == "EXIT":
                    self.socket.sendall(command.encode())
                    self.socket.close()
                    break
                
                # For uLS command, we want to list files on server side
                if command.startswith("uLS"):
                    self.socket.sendall(command.encode())
                    data = self.socket.recv(4096).decode()
                    print("Files on server:")
                    print(data)
                    continue

                # For mLS command, we want to list files on client side
                elif command.startswith("mLS"):
                    print("Files to upload: ")
                    print(data)
                    continue

                if command.startswith("UPLOAD") or command.startswith("DOWNLOAD"):
                    self.socket.sendall(command.encode())
                    parts = shlex.split(command)

                    if len(parts) < 2:
                        print("Invalid command. Please enter UPLOAD <filename> or DOWNLOAD <filename>.")
                        continue

                    cmd = parts[0].upper()
                    filename = parts[1]

                    client_commands.get(cmd, lambda *args: lambda_log(self.socket, f"Invalid command: {cmd}"))(self.socket, filename, returnFileType(filename))
                else:
                    print("Invalid command. Please enter UPLOAD <filename> or DOWNLOAD <filename>.")
            
        except Exception as e:
            log(f"Error connecting to server: {e}")
            return
    
# Server code
class P2PServer:
    def __init__(self):
        self.host = server_dataclass.host
        self.port = server_dataclass.port

        self.connections = []

        self.socket = s.create_server((self.host, self.port), family=s.AF_INET)
        self.socket.settimeout(1)

    def handle_client(self, conn: s.socket, addr):
        try:
            while True:

                try:
                    command = conn.recv(1024).decode()

                    if command == "":
                        log(f"Connection lost with {addr[0]}:{addr[1]}")
                        break

                except s.timeout:
                    continue

                if command.upper() == "EXIT":
                    conn.close()
                    break
            
                parts = shlex.split(command)

                if len(parts) < 2:
                    lambda_log(conn, f"Invalid command from {addr[0]}:{addr[1]}: {command}", "Invalid command: \nAvailable commands are: UPLOAD <filename>, DOWNLOAD <filename>")
                    continue

                cmd = parts[0].upper()
                filename = parts[1]

                server_commands.get(cmd, lambda *args: lambda_log(conn, f"Invalid command from {addr[0]}:{addr[1]}: {command}", "Invalid command: \nAvailable commands are: UPLOAD <filename>, DOWNLOAD <filename>"))(conn, filename, returnFileType(filename))
        except Exception as e:
            log(f"Error handling client {addr[0]}:{addr[1]}: {e}")
        finally:
            conn.close()
            log(f"Connection closed with {addr[0]}:{addr[1]}")
    
    def run(self):
        log(f"Server started on {self.host}:{self.port}")
        try:
            while True:
                try:
                    conn, addr = self.socket.accept()
                except s.timeout:
                    continue

                conn.settimeout(10.0)
                self.connections.append({conn: addr})
                try:
                    log(f"Connection established with {addr[0]}:{addr[1]}")
                    threading.Thread(target=self.handle_client, args=(conn, addr)).start()
                except Exception as e:
                    log(f"Error handling connection with {addr[0]}:{addr[1]}: {e}")
                    continue

                finally:
                    log(f"Finished handling connection with {addr[0]}:{addr[1]}")

        except KeyboardInterrupt:
            log("Server shutting down...")
        
        self.socket.close()
    
if __name__ == "__main__":
    print(f"HOST: {server_dataclass.host}\nPORT: {server_dataclass.port}")