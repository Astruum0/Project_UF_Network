import socket
from _thread import start_new_thread
import logging
import pickle
import pygame
from pong_class import Pong_game
from snake_class import Snake_game, Snake
from tic_tac_toe__class import Tic_Tac_Toe_Game

pygame.font.init()

server = "192.168.0.44"
port = 5556

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s] %(message)s")
file_handler = logging.FileHandler("server_logs.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
logger.info(f"Server Started, adress is {server}:{port}")
pong_games = {}
snake_games = {}
tic_tac_toe_games = {}
idCount = 0

font_size = 30
font = pygame.font.Font("fonts/PixelOperator8.ttf", font_size)


def online_pong(conn, p, gameId, pseudo):
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
                    if data == "start":
                        game.start()
                        game.winner = None
                    if data != "get" and data != "start":
                        game.movePanel(p, data)
                        game.update()
                    pong_games[gameId] = game
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    logger.info(f"{pseudo} disconnected from Pong Game {gameId}")

    try:
        del pong_games[gameId]
        logger.info(f"Closing Game {gameId}")
    except:
        pass
    idCount -= 1
    conn.close()


def online_snake(conn, p, gameId, pseudo):
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

    logger.info(f"{pseudo} disconnected from Snake Game {gameId}")

    try:
        del snake_games[gameId]
        logger.info(f"Closing Snake Game {gameId}")
    except:
        pass
    conn.close()


def online_tic_tac_toe(conn, p, gameId, pseudo):
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
                    tic_tac_toe_games[gameId] = game
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    logger.info(f"{pseudo} disconnected from TicTacToe Game {gameId}")
    try:
        del tic_tac_toe_games[gameId]
        logger.info(f"Closing Game {gameId}")
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    try:
        conn, addr = s.accept()
    except:
        logger.info("Closed server")
        break
    game_choosen, pseudo, choosed_id = conn.recv(4096).decode().split(",")
    if pseudo == "_":
        if game_choosen == "Pong":
            conn.sendall(pickle.dumps(pong_games))
        elif game_choosen == "Snake":
            conn.sendall(pickle.dumps(snake_games))
        elif game_choosen == "Tic_Tac_Toe":
            conn.sendall(pickle.dumps(tic_tac_toe_games))
        continue

    if game_choosen == "Pong":
        game_entered = False
        ID = 0
        try:
            ID = int(choosed_id)
            pong_games[ID].connected = True
            p = 1
            logger.info(
                f"Connecting {pseudo} {str(addr).replace(', ', ':')} to Pong Game {ID} ..."
            )
        except ValueError:
            for gameId in pong_games:
                if not pong_games[gameId].connected and choosed_id != "create":
                    ID = gameId
                    game_entered = True
                    p = 1
                    pong_games[ID].connected = True
                    pong_games[ID].list_pseudo.append(pseudo)

                    logger.info(
                        f"Connecting {pseudo} {str(addr).replace(', ', ':')} to Pong Game {ID} ..."
                    )
                    break
            if not game_entered or choosed_id == "create":
                for id_ in range(100):
                    if not id_ in pong_games:
                        pong_games[id_] = Pong_game(id_)
                        ID = id_
                        p = 0
                        logger.info(
                            f"{pseudo} {str(addr).replace(', ', ':')} created Pong Game {ID}"
                        )
                        break
        start_new_thread(online_pong, (conn, p, ID, pseudo))

    elif game_choosen == "Snake":
        game_entered = False
        ID = 0
        try:
            ID = int(choosed_id)
            logger.info(
                f"Connecting {pseudo} {str(addr).replace(', ', ':')} to Snake Game {ID} ..."
            )
        except:
            for gameId in snake_games:
                if (
                    snake_games[gameId].players_nbr <= 3
                    and not snake_games[gameId].started
                    and choosed_id != "create"
                ):
                    ID = gameId
                    game_entered = True
                    logger.info(
                        f"Connecting {pseudo} {str(addr).replace(', ', ':')} to Snake Game {ID}"
                    )
                    break
            if not game_entered or choosed_id == "create":
                for id_ in range(100):
                    if not id_ in snake_games:
                        snake_games[id_] = Snake_game(id_)
                        ID = id_
                        logger.info(
                            f"{pseudo} {str(addr).replace(', ', ':')} created Snake Game {ID} ..."
                        )
                        break

        surfacePseudo1 = font.render(
            pseudo, 1, Snake.colors[snake_games[ID].players_nbr], True
        )
        surfacePseudo2 = font.render(pseudo, 1, Snake.colors[4], True)
        while surfacePseudo1.get_width() > 180:
            font_size -= 1
            font = pygame.font.Font("fonts/PixelOperator8.ttf", font_size)
            surfacePseudo1 = font.render(
                pseudo, 1, Snake.colors[snake_games[ID].players_nbr], True
            )
            surfacePseudo2 = font.render(pseudo, 1, Snake.colors[4], True)

        snake_games[ID].newPlayer(pseudo)
        start_new_thread(
            online_snake, (conn, snake_games[ID].players_nbr - 1, ID, pseudo)
        )

    elif game_choosen == "Tic_Tac_Toe":
        game_entered = False
        ID = 0
        if type(choosed_id) == int:
            ID = choosed_id
            tic_tac_toe_games[ID].connected = True
            p = 1
            logger.info(
                f"Connecting {pseudo} {str(addr).replace(', ', ':')} to Snake Game {ID}"
            )
        else:
            for gameId in tic_tac_toe_games:
                if not tic_tac_toe_games[gameId].connected and choosed_id != "create":

                    ID = gameId
                    tic_tac_toe_games[ID].connected = True
                    game_entered = True
                    logger.info(
                        f"Connecting {pseudo} {str(addr).replace(', ', ':')} to Snake Game {ID}"
                    )
                    p = 1
                    break
            if not game_entered or choosed_id == "create":
                for id_ in range(100):
                    if not id_ in tic_tac_toe_games:
                        tic_tac_toe_games[id_] = Tic_Tac_Toe_Game(id_)
                        ID = id_
                        p = 0
                        logger.info(
                            f"{pseudo} {str(addr).replace(', ', ':')} created TicTacToe Game {ID} ..."
                        )
                        break
        tic_tac_toe_games[ID].list_pseudo.append(pseudo)
        start_new_thread(online_tic_tac_toe, (conn, p, ID, pseudo))
