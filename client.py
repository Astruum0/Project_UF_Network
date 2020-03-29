import pygame
from network_for_client import Network
import pickle

pygame.init()

clock = pygame.time.Clock()
pygame.font.init()
bg = pygame.image.load("bg.png")
width = 800
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("PONG")

font = pygame.font.Font("PixelOperator8.ttf", 20)
waiting_text = font.render("Waiting for Player...", 1, (255, 255, 255), True)

jeu = True
net = Network("Pong")
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
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jeu = False
            pygame.quit()

    if game.connected:
        move = "none"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            move = "UP"
        if keys[pygame.K_DOWN]:
            move = "DOWN"
        game = net.send(move)
        game.show(win)

    else:
        win.blit(
            waiting_text,
            (
                width / 2 - waiting_text.get_width() / 2,
                height / 2 - waiting_text.get_height() / 2 - 200,
            ),
        )

    pygame.display.update()
