import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION

win = pygame.display.set_mode((600, 600))
pygame.display.set_caption("PyNetGames")

bg = pygame.image.load("menu_sprites/menu.png")

hover = pygame.image.load("menu_sprites/hover.png")

clock = pygame.time.Clock()

btn_width = 487
btn_height = 71


menu = True
while menu:
    clock.tick(60)
    win.blit(bg, (0, 0))

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
                print("PONG")
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
