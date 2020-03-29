import socket
from _thread import start_new_thread
import pickle
from pong_class import Pong_game

server = "192.168.1.38"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")
games = {}
idCount = 0


def online_pong(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data != "get":
                        game.movePanel(p, data)
                        game.update()
                        games[gameId] = game
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print(f"Player {p+1} disconnected")

    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    game_choosen = conn.recv(4096).decode()
    print("Connected to : ", addr)
    print(f"Looking for available {game_choosen} lobbies...")

    if game_choosen == "Pong":
        idCount += 1
        p = 0
        gameId = (idCount - 1) // 2
        if idCount % 2 == 1:
            games[gameId] = Pong_game(gameId)
            print("Creating a new game...")
        else:
            print(f"Connecting to Game {gameId} ...")
            games[gameId].connected = True
            p = 1

        start_new_thread(online_pong, (conn, p, gameId))
