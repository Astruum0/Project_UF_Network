import socket
import pickle


class Network:
    def __init__(self, game_type, pseudo):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.14"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect(game_type, pseudo)

    def getP(self):
        return self.p

    def connect(self, game, pseudo):
        try:
            self.client.connect(self.addr)
            self.client.send(str.encode(game + "," + pseudo))
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048 * 4))
        except socket.error as e:
            print(e)
