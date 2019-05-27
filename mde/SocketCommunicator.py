import socket

class SocketCommunicator:

    def __init__(self, TCP_IP, TCP_PORT, BUFFER_SIZE):
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = BUFFER_SIZE
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.TCP_IP, self.TCP_PORT))

    def close(self):
        self.socket.close()

    def send(self, message):
        self.socket.send(message.encode('utf-8'))
        data = self.socket.recv(self.BUFFER_SIZE)
        return data

    def no_reply(self, message):
        self.socket.send(message.encode('utf-8'))

