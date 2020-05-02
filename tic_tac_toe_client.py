from random import randint
from network_for_client import Network
import pygame


def tic_tac_toe_client(pseudo, id_):
    pygame.init()
    width = 616
    height = 700
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Tic-Tac-Toe")
    grille = pygame.image.load("sprites_tic_tac_toe/board.png")

    font20 = pygame.font.Font("fonts/PixelOperator8.ttf", 20)
    waiting_text = font20.render("Waiting for Player...", 1, (0, 0, 0), True)
    your_turn = font20.render("Your turn", 1, (0, 0, 0), True)
    other_turn = font20.render("Opponent turn", 1, (0, 0, 0), True)

    run = True
    can_Play = True
    # end = False
    # winner = 0

    net = Network("Tic_Tac_Toe", pseudo, id_)
    player = int(net.getP())
    if player + 1 == 1:
        number_player = 1
    else:
        number_player = -1
    print("You are Player", player + 1)

    while run:
        win.blit(grille, (0, 0))
        try:
            game = net.send("get,")
        except:
            win = pygame.display.set_mode((600, 600))
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                win = pygame.display.set_mode((600, 600))
                return
        if game.connected:
            can_Play = game.can_play[player]
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and can_Play == True:

                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    x, y = -1, -1

                    for i in range(0, 3):
                        if (i * 190) + 60 < mouse_x < (i * 190) + 200:
                            y = i

                    for i in range(0, 3):
                        if (i * 170) + 200 < mouse_y < (i * 170) + 330:
                            x = i
                    game = net.send(f"pos,{x},{y},{number_player}")
            game.Show(win)
            win.blit(
                your_turn if can_Play else other_turn,
                (
                    700 / 2 - your_turn.get_width() / 2
                    if can_Play
                    else 700 / 2 - other_turn.get_width() / 2,
                    700 / 2 - other_turn.get_height() / 2 - 300
                    if can_Play
                    else 700 / 2 - other_turn.get_height() / 2 - 300,
                ),
            )

        else:
            win.blit(
                waiting_text,
                (
                    700 / 2 - waiting_text.get_width() / 2,
                    700 / 2 - waiting_text.get_height() / 2 - 300,
                ),
            )

        pygame.display.update()
