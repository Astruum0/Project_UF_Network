import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION
from pseudo_type import enterPseudo
from pong_client import pong_client

win = pygame.display.set_mode((600, 600))
pygame.display.set_caption("PyNetGames")

bg = pygame.image.load("menu_sprites/menu.png")

hover = pygame.image.load("menu_sprites/hover.png")

clock = pygame.time.Clock()

btn_width = 487
btn_height = 71

pseudo = enterPseudo()

pygame.font.init()
font = pygame.font.Font("fonts/PixelOperatorMono8-Bold.ttf", 20)
welcome_text = font.render(f"Welcome, {pseudo} !", 1, (255, 255, 255))

x_hover, y_hover = (None, None)

menu = True
while menu:
    clock.tick(60)
    win.blit(bg, (0, 0))

    win.blit(welcome_text, (600 / 2 - welcome_text.get_width() // 2, 15))

    x_mouse, y_mouse = pygame.mouse.get_pos()
    for e in pygame.event.get():
        if e.type == QUIT:
            menu = False
            break

        if (
            x_mouse > 56
            and x_mouse < 56 + btn_width
            and y_mouse > 207
            and y_mouse < 207 + btn_height
        ):
            x_hover, y_hover = (56, 207)
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                pong_client(pseudo)
        elif (
            x_mouse > 56
            and x_mouse < 56 + btn_width
            and y_mouse > 292
            and y_mouse < 292 + btn_height
        ):
            x_hover, y_hover = (56, 292)
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                print("TicTacToe")
        elif (
            x_mouse > 56
            and x_mouse < 56 + btn_width
            and y_mouse > 377
            and y_mouse < 377 + btn_height
        ):
            x_hover, y_hover = (56, 377)
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                print("Snake")
        elif (
            x_mouse > 56
            and x_mouse < 56 + btn_width
            and y_mouse > 462
            and y_mouse < 462 + btn_height
        ):
            x_hover, y_hover = (56, 462)
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                print("Uno")
        else:
            x_hover, y_hover = (None, None)

    if x_hover and y_hover:
        win.blit(hover, (x_hover, y_hover))

    pygame.display.update()
