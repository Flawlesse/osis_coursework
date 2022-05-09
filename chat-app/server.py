import socket
from datetime import datetime
import threading
import re


HOST = "localhost"
TCP_PORT = 9090
UDP_PORT = 9091
BUFSIZE = 65536

class Server():
    def __init__(self):
        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server.bind((HOST, TCP_PORT))
        self.tcp_server.listen(2)
        print("TCP server started.")

        self.udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_server.bind((HOST, UDP_PORT))
        print("UDP server started.")

        self.users = dict()  # keeps users like "name": address

    def _tcp_accept(self):
        needs_new_connection = True
        client_connection, address = None, None
        while True:
            if needs_new_connection:
                client_connection, address = self.tcp_server.accept()
                needs_new_connection = False
            print(f"TCP server connected to {address[0]}:{address[1]}.")
            if len(self.users.items()) == 2:
                print("No more users allowed!")
                client_connection.recv(BUFSIZE)
                client_connection.send("TOO_MANY".encode('utf-8'))
            else:
                name = client_connection.recv(BUFSIZE).decode('utf-8')
                if name in self.users.keys():
                    print(f"User {name} already exists.")
                    client_connection.send("EXISTS".encode('utf-8'))
                else:
                    self.users[name] = None
                    client_connection.send("SUCCESS".encode("utf-8"))
                    print(f"Took place for {name}.")
                    client_connection.close()
                    needs_new_connection = True
            

    def _udp_accept(self):
        while True:
            message, address = self.udp_server.recvfrom(BUFSIZE)
            message = message.decode('utf-8').strip()
            try:
                if re.match(r"/REG/.+", message) is not None:
                    name = message[5:]
                    if name not in self.users.keys() or self.users[name] is not None:
                        raise KeyError("Tried to hack the system.")
                    self.users[name] = address
                    self.udp_server.sendto(f"User {name} sucessfully connected.".encode('utf-8'), address)
                    print(f"Successfully registered user {name}.")
                elif message == "\q":
                    name = None
                    for user in self.users.items():
                        if user[1] == address:
                            name = user[0]
                            self.udp_server.sendto(f"User {user[0]} sucessfully disconnected.".encode('utf-8'), address)
                            print(f"User {name} removed.")
                    self.users.pop(name)
                else:
                    name = "<anonymous>"
                    for user in self.users.items():
                        if user[1] == address:
                            name = user[0]
                    for user in self.users.items():
                        self.udp_server.sendto((f"{name}:{datetime.now()}:\n" + message).encode('utf-8'), user[1])
            except KeyError as e:
                print(e.args[0])



    def start(self):
        init_connection_thread = threading.Thread(target=self._tcp_accept, daemon=True)
        messaging_thread = threading.Thread(target=self._udp_accept, daemon=True)
        init_connection_thread.start()
        messaging_thread.start()

    def stop(self):
        self.tcp_server.close()
        self.udp_server.close()


if __name__ == "__main__":
    server = Server()
    try:
        server.start()
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()