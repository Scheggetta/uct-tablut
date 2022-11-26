import socket


class ServerConnector:
    def __init__(self, ip_address: str, port: int):
        self.ip_address = ip_address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip_address, port))

    def close_connection(self):
        self.socket.close()

    def send_msg(self, msg):
        self.socket.sendall(msg)

    def read(self) -> bytes:
        # Read 4 bytes (i.e., length of message)
        payload = bytes()
        while len(payload) < 4:
            payload += self.socket.recv(1)

        # Read the rest
        size = int.from_bytes(payload[:4], byteorder='big')
        while len(payload) - 4 < size:
            payload += self.socket.recv(1)
        return payload


