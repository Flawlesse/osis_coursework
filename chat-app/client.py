# TCP CLIENT
# import socket

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(("localhost", 9999))

# client.send("Hello server!".encode('utf-8'))
# print(client.recv(1024).decode('utf-8'))
# client.send("Bye server!".encode('utf-8'))
# print(client.recv(1024).decode('utf-8'))


# UDP CLIENT
# import socket

# client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# client.sendto("Hello server!".encode('utf-8'), ("localhost", 9999))
# print(client.recvfrom(1024)[0].decode('utf-8'))

import socket
from os import system
import threading
import time


HOST = "localhost"
TCP_PORT = 9090
UDP_PORT = 9091
BUFSIZE = 65536


class Client():
    def __init__(self):
        self.client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_tcp.connect((HOST, TCP_PORT))
        self.client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        print('Welcome! You are new here, so go ahead and register.')
        self._register()

        # this runs only after the registration 
        listen_udp_thread = threading.Thread(target=self.listen_udp, daemon=True)
        listen_udp_thread.start()

        while True:
            try:
                message = input()
                self.client_udp.sendto(message.encode('utf-8'), (HOST, UDP_PORT))
                if message.strip() == "\q":
                    time.sleep(0.5)
                    print("Shutting down client...")
                    exit(0)
            except ConnectionResetError:
                print("Looks like a server problem.")
                exit(0)
            except KeyboardInterrupt:
                self.client_udp.sendto("\q".encode('utf-8'), (HOST, UDP_PORT))
                print("Gracefully exiting...")
                exit(0)

    def _register(self):
        fail = True
        while fail:
            name = input("\nTell me your name please: ")
            name = name.strip()
            if name == "":
                continue
            self.client_tcp.send(name.encode('utf-8'))
            response = self.client_tcp.recv(BUFSIZE).decode('utf-8')
            print(f"Response: {response}")
            if response == "TOO_MANY":
                print("Looks like you're out of place for now, wait your turn...")
            elif response == "EXISTS":
                print("Homie has the same name, what a coincidence! Pick other name.")
            elif response == "SUCCESS":
                print("Good job!")
                self.client_udp.sendto(f"/REG/{name}".encode('utf-8'), (HOST, UDP_PORT))
                print(self.client_udp.recvfrom(BUFSIZE)[0].decode('utf-8'))
                fail = False

    def listen_udp(self):
        while True:
            try:
                message = self.client_udp.recvfrom(BUFSIZE)[0].decode('utf-8')
                print(f"\n{message}\n")
            except ConnectionResetError:
                print("Looks like a server problem.")
                exit(0)



if __name__ == "__main__":
    system('clear')
    client = Client()
    client.start()