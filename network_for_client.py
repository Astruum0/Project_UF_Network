import socket
import pickle


class Network:
    def __init__(self, game_type, pseudo, gameId):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.14"
        self.port = 5556
        self.addr = (self.server, self.port)
        self.p = self.connect(game_type, pseudo, gameId)

    def getP(self):
        return self.p

    def connect(self, game, pseudo, gameId):
        self.client.connect(self.addr)
        self.client.send(str.encode(game + "," + pseudo + "," + gameId))
        if pseudo == "_":
            return pickle.loads(self.client.recv(2048 * 4))
        else:
            return self.client.recv(2048).decode()

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048 * 4))
        except socket.error as e:
            print(e)

    def disconnect(self):
        self.client.shutdown(socket.SHUT_RDWR)
        self.client.close()
