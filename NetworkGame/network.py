import socket
import pickle

class Network:
    #inicialização
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.11"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    #Informa quem foi conectado
    def getP(self):
        return self.p

    #Checa se foi devidamente conectado
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    #Checa se houve a troca de informações [envia srt e decodifica um objeto]
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)
