from network_for_client import Network
from pong_client import pong_client
from snake_client import snake_client
from tic_tac_toe_client import tic_tac_toe_client
import pygame


def returnID(x_pos, y_pos):
    if x_pos >= 174 and x_pos <= 174 + 245 and y_pos >= 480 and y_pos <= 521 + 35:
        if y_pos < 480 + 35:
            return "create"
        elif y_pos > 521:
            return "auto"
    id_ = (y_pos - 150) // 50
    if id_ >= 0:
        return id_
    else:
        return 100


def createText(game, list_games):
    font = pygame.font.Font(
        "fonts/PixelOperator8.ttf", (30 if game != "Tic_Tac_Toe" else 20)
    )

    saloonText = []

    if game != "Snake":
        for id in list_games:
            if list_games[id].connected == False:
                saloonText.append(
                    font.render(f"Game {id + 1} - 1/2", 1, (255, 255, 255))
                )
    elif game == "Snake":
        for id in list_games:
            if list_games[id].players_nbr < 4:
                saloonText.append(
                    font.render(
                        f"Game {id + 1} - {list_games[id].players_nbr}/4",
                        1,
                        (255, 255, 255),
                    )
                )

    return saloonText


def show_saloon(game, pseudo):
    net = Network(game, "_", "")
    games = net.getP()

    pygame.init()
    pygame.font.init()
    win = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("PyNetGames")
    bg = pygame.image.load("menu_sprites/saloon.png")

    font = pygame.font.Font(
        "fonts/PixelOperator8.ttf", (30 if game != "Tic_Tac_Toe" else 20)
    )

    title = font.render(f"Choose a {game.replace('_',' ')} Saloon", 1, (255, 255, 255))

    saloonText = createText(game, games)

    while True:
        win.blit(bg, (0, 0))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                choice = returnID(mouse_x, mouse_y)
                if choice in ["auto", "create"] or int(choice) <= len(games):
                    if game == "Pong":
                        pong_client(pseudo, str(choice))
                        return
                    elif game == "Snake":
                        snake_client(pseudo, str(choice))
                        return
                    elif game == "Tic_Tac_Toe":
                        tic_tac_toe_client(pseudo, str(choice))
                        return

        win.blit(title, (300 - title.get_width() / 2, 50))

        i = 0
        for fnt in saloonText:
            win.blit(fnt, (600 / 2 - fnt.get_width() / 2, 210 + i * 50))
            i += 1

        pygame.display.update()


if __name__ == "__main__":
    show_saloon("Snake", "Astruum")
