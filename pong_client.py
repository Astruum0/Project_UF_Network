import pygame
from network_for_client import Network
import pickle
import mysql.connector


def win_increase(gagnant):
    connection = mysql.connector.connect(host="mysql-sql-crackito.alwaysdata.net",
                                     database="sql-crackito_projetreseau",
                                     user="204318",
                                     password="20102001Aa")
    cursor = connection.cursor()
    sql_update_query = f"update users set win_pong = win_pong + 1 where user_name = '{gagnant}'"
    cursor.execute(sql_update_query)
    connection.commit()
    
def pong_client(pseudo, id_):
    pygame.init()

    clock = pygame.time.Clock()
    pygame.font.init()
    bg = pygame.image.load("sprites_pong/bg.png")
    width = 800
    height = 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("PONG")

    font = pygame.font.Font("fonts/PixelOperator8.ttf", 20)
    waiting_text = font.render("Waiting for Player...", 1, (255, 255, 255), True)
    jeu = True
    increased = False
    net = Network(
        "Pong", pseudo, id_ if id_ in ["create", "auto"] else str(int(id_) - 1)
    )
    player = int(net.getP())
    print("You are Player", player + 1)

    while jeu:
        clock.tick(60)
        win.blit(bg, (0, 0))
        try:
            game = net.send("get")
        except:
            jeu = False
            print("Couldn't get game")
            win = pygame.display.set_mode((600, 600))
            return
                

                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jeu = False
                win = pygame.display.set_mode((600, 600))
                return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and game.connected and not game.started:
            game = net.send("start")
        if game.started:
            increased = False
            move = "none"

            if keys[pygame.K_UP]:
                move = "UP"
            if keys[pygame.K_DOWN]:
                move = "DOWN"
             
            game = net.send(move)
            game.show(win)
            
            
        else:
            if game.winner == player and increased == False:
                win_increase(pseudo)
                increased = True
            win.blit(
                waiting_text,
                (
                    width / 2 - waiting_text.get_width() / 2,
                    height / 2 - waiting_text.get_height() / 2 - 200,
                ),
            )

        pygame.display.update()
