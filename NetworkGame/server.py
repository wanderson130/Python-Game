import socket
from _thread import *
import pickle
from game import Game

server = "192.168.0.11"
port = 5555
#criaçao do socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#local onde atrelamos o endereço/porta do servidor
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

#Instrui o modo passivo para conexao dos players
s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0

#Verifica estado do jogo atual a partir do client
def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()
            #atrela um id para cada jogo
            if gameId in games:
                game = games[gameId]
                #dependendo da informação atual faz uma determinada modificação
                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()

#garante a inicialização do jogo somente se existir um outro jogador e atribui um id para ambos.
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId))