import socket
from _thread import start_new_thread
import pickle
import pygame
from pong_class import Pong_game
from snake_class import Snake_game, Snake
from tic_tac_toe__class import Tic_Tac_Toe_Game

pygame.font.init()

server = "192.168.43.63"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")
pong_games = {}
snake_games = {}
tic_tac_toe_games = {}
idCount = 0

font_size = 30
font = pygame.font.Font("PixelOperator8.ttf", font_size)


def online_pong(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in pong_games:
                game = pong_games[gameId]

                if not data:
                    break
                else:
                    if data != "get":
                        game.movePanel(p, data)
                        game.update()
                        pong_games[gameId] = game
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print(f"Player {p+1} disconnected from Pong Game", gameId)

    try:
        del pong_games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


def online_snake(conn, p, gameId):
    conn.send(str.encode(str(p)))
    conn.sendall(pickle.dumps(snake_games[gameId]))
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in snake_games:
                game = snake_games[gameId]

                if not data:
                    break
                else:
                    if data == "start":
                        game.started = True
                    if data != "get" and data != "start":
                        game.moveSnake(p, data)
                        game.update()
                    snake_games[gameId] = game
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print(f"Player {p+1} disconnected from Snake Game", gameId)

    try:
        del snake_games[gameId]
        print("Closing Snake Game", gameId)
    except:
        pass
    conn.close()

def online_tic_tac_toe(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))
    conn.sendall(pickle.dumps(tic_tac_toe_games[gameId]))
    while True:
        try:
            data = conn.recv(4096).decode()
            data = data.split(",")
            if gameId in tic_tac_toe_games:
                game = tic_tac_toe_games[gameId]
                if not data:
                    break
                else:
                    if data[0] == "pos":
                        game.Update(int(data[1]), int(data[2]), int(data[3]))
                        game = tic_tac_toe_games[gameId]
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


while True:
    conn, addr = s.accept()
    game_choosen, pseudo = conn.recv(4096).decode().split(",")
    print("Connected to : ", addr)
    print(f"Looking for available {game_choosen} lobbies...")

    if game_choosen == "Pong":
        idCount += 1
        p = 0
        gameId = (idCount - 1) // 2
        if idCount % 2 == 1:
            pong_games[gameId] = Pong_game(gameId)
            print("Creating a new game...")
        else:
            print(f"Connecting to Pong Game {gameId} ...")
            pong_games[gameId].connected = True
            p = 1

        start_new_thread(online_pong, (conn, p, gameId))
        
    elif game_choosen == "Snake":
        game_entered = False
        ID = 0
        for gameId in snake_games:
            if snake_games[gameId].players_nbr <= 3 and not snake_games[gameId].started:
                print(f"Connecting to Snake Game {gameId} ...")

                ID = gameId
                game_entered = True
                break
        if not game_entered:
            for id_ in range(100):
                if not id_ in snake_games:
                    snake_games[id_] = Snake_game(id_)
                    ID = id_
                    break

        surfacePseudo1 = font.render(
            pseudo, 1, Snake.colors[snake_games[ID].players_nbr], True
        )
        surfacePseudo2 = font.render(pseudo, 1, Snake.colors[4], True)
        while surfacePseudo1.get_width() > 180:
            font_size -= 1
            font = pygame.font.Font("PixelOperator8.ttf", font_size)
            surfacePseudo1 = font.render(
                pseudo, 1, Snake.colors[snake_games[ID].players_nbr], True
            )
            surfacePseudo2 = font.render(pseudo, 1, Snake.colors[4], True)

        snake_games[ID].newPlayer(pseudo)
        start_new_thread(online_snake, (conn, snake_games[ID].players_nbr - 1, ID))

    elif game_choosen == "Tic_Tac_Toe":
        idCount += 1
        p = 0
        gameId = (idCount - 1) // 2
        if idCount % 2 == 1:
            tic_tac_toe_games[gameId] = Tic_Tac_Toe_Game(gameId)
            print("Creating a new game...")
        else:
            print(f"Connecting to Tic Tac Toe Game {gameId} ...")
            tic_tac_toe_games[gameId].connected = True
            p = 1

        start_new_thread(online_tic_tac_toe, (conn, p, gameId))
