from network_for_client import Network
import pygame


def returnID(y_pos):
    id_ = (y_pos - 200) // 50
    if id_ >= 0:
        return id_
    else:
        return 100


def show_saloon(game, pseudo):
    net = Network(game, "_", "")
    games = net.getP()

    listgames = []
    for g in games:
        listgames.append(games[g])

    pygame.init()
    pygame.font.init()
    win = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("PyNetGames")

    font = pygame.font.Font("fonts/PixelOperator8.ttf", 30)

    title = font.render(f"Choose a {game} Saloon", 1, (255, 255, 255))

    saloonText = []

    if game != "Snake":
        for id in games:
            if games[id].connected == False:
                saloonText.append(
                    font.render(f"Game {id + 1} - 1/2", 1, (255, 255, 255))
                )
    elif game == "Snake":
        for id in games:
            if games[id].players_nbr < 4:
                saloonText.append(
                    font.render(
                        f"Game {id + 1} - {games[id].players_nbr}/4", 1, (255, 255, 255)
                    )
                )

    while True:
        win.fill((0, 0, 0))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                _, mouse_y = pygame.mouse.get_pos()
                id_ = returnID(mouse_y)
                if id_ < len(listgames):
                    print(id_)

        win.blit(title, (300 - title.get_width() / 2, 100))

        i = 0
        for fnt in saloonText:
            win.blit(fnt, (600 / 2 - fnt.get_width() / 2, 210 + i * 50))
            i += 1

        pygame.display.update()


if __name__ == "__main__":
    show_saloon("Snake", "Astruum")
