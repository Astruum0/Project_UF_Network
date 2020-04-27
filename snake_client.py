import pygame
from network_for_client import Network
import pickle
from snake_class import show_font, Snake
from pseudo_type import enterPseudo


def snake_client(pseudo, id_):
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    pygame.font.init()
    width = 1000
    height = 700
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("SNAKE")

    font20 = pygame.font.Font("fonts/PixelOperator8.ttf", 20)
    font40 = pygame.font.Font("fonts/PixelOperator8.ttf", 40)
    waiting_text = font20.render("Waiting for Player...", 1, (255, 255, 255), True)
    all_surfaces = []

    jeu = True
    net = Network("Snake", pseudo, id_)
    player = int(net.getP())
    print("You are Player", player + 1)

    def return_surfaces(pseudo, i):
        font_size = 30
        font = pygame.font.Font("fonts/PixelOperator8.ttf", font_size)
        surfacePseudo1 = font.render(pseudo, 1, Snake.colors[i], True)
        surfacePseudo2 = font.render(pseudo, 1, Snake.colors[4], True)
        while surfacePseudo1.get_width() > 180:
            font_size -= 1
            font = pygame.font.Font("fonts/PixelOperator8.ttf", font_size)
            surfacePseudo1 = font.render(pseudo, 1, Snake.colors[i], True)
            surfacePseudo2 = font.render(pseudo, 1, Snake.colors[4], True)
        return (surfacePseudo1, surfacePseudo2)

    try:
        game = net.send("get")
    except:
        jeu = False
        print("Couldn't get game")

    while jeu:
        clock.tick(45)
        win.fill((0, 0, 0))

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jeu = False
                win = pygame.display.set_mode((600, 600))
                return

        if game.started:

            move = "none"
            if keys[pygame.K_UP]:
                move = "UP"
            if keys[pygame.K_DOWN]:
                move = "DOWN"
            if keys[pygame.K_LEFT]:
                move = "LEFT"
            if keys[pygame.K_RIGHT]:
                move = "RIGHT"

            try:
                game = net.send(move)
            except:
                jeu = False
                print("Couldn't get game")
                win = pygame.display.set_mode((600, 600))
                return
            game.show(win)
            show_font(game, win, font40, all_surfaces)

        else:
            win.blit(
                waiting_text,
                (
                    700 / 2 - waiting_text.get_width() / 2,
                    700 / 2 - waiting_text.get_height() / 2 - 200,
                ),
            )
            list_pseudos = {}
            all_surfaces = []
            for p in game.players:
                list_pseudos[p.snake_id] = p.name
            for i in list_pseudos:
                all_surfaces.append(return_surfaces(list_pseudos[i], i))
            if keys[pygame.K_SPACE] and game.players_nbr > 1:
                game = net.send("start")
            else:
                try:
                    game = net.send("get")
                except:
                    jeu = False
                    print("Couldn't get game")
                    win = pygame.display.set_mode((600, 600))
                    return
            for s in game.players:
                s.showStats(win)
            show_font(game, win, font40, all_surfaces)

        pygame.display.update()
