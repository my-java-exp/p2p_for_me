from config import P2PServer, P2PClient
from threading import Thread

manual = "\nBy The Way 'host' and 'port' mean the host and port to connect to\n------------------------------------------------------\n  1. Write '<host> <port> C' for client only mod\n  2. Write <host> <port> for server-client mode\n  3. Press enter(type nothing) for server only mode\n------------------------------------------------------\n"

def main():
    print(manual)

    uInput = input("> ")

    if uInput == "e":
        print("Exiting")
        return
    
    if uInput == "":
        try:
            server = P2PServer()
            server_thread = Thread(target=server.run)
            server_thread.start()
            server_thread.join()
            return
        except KeyboardInterrupt:
            return

    elif uInput.endswith("C"):
        try:
            host, port, _ = uInput.split()
            client = P2PClient(host, port)

            client_thread = Thread(target=client.connect)
            client_thread.start()
            client_thread.join()
            return
        except KeyboardInterrupt:
            return
    
    elif uInput.count(" ") == 1:
        try:
            host, port = uInput.split()

            if port.isdigit():
                port = int(port)
            
            else:
                print("Invalid port number. Please enter a valid integer for the port.")
                return
        
            client = P2PClient(host, port)
            server = P2PServer()
            
            client_thread = Thread(target=client.connect)
            client_thread.start()

            server_thread = Thread(target=server.run)
            server_thread.start()

            client_thread.join()
            server_thread.join()

            return
        except KeyboardInterrupt:
            return

main()