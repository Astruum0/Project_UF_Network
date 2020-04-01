import pygame
from pygame.locals import *


def enterPseudo():
    """
    Function that open a window where the user can type his pseudo
    """

    pygame.font.init()
    win = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Save your Level")
    clock = pygame.time.Clock()
    font = pygame.font.Font("fonts/PixelOperatorMono8-Bold.ttf", 30)
    bg = pygame.image.load("menu_sprites/inputpseudo.png")
    index = 0

    name = []

    loop = True
    while loop:
        win.blit(bg, (0, 0))
        clock.tick(60)
        text = ""
        for letter in name:
            text += letter
        for event in pygame.event.get():
            if event.type == QUIT:
                loop = False
                return

            if event.type == MOUSEBUTTONDOWN:
                if (
                    event.pos[0] >= 521
                    and event.pos[0] <= 560
                    and event.pos[1] >= 315
                    and event.pos[1] <= 355
                    and len(text) > 1
                ):
                    loop = False
                    return text
                # if (
                #     event.pos[0] >= 531
                #     and event.pos[0] <= 576
                #     and event.pos[1] >= 531
                #     and event.pos[1] <= 576
                # ):
                #     saving = False
                #     return

            if event.type == KEYDOWN and event.unicode != "" and event.unicode != '"':
                if event.key == K_LEFT:
                    if index > 1:
                        index -= 1
                elif event.key == K_RIGHT:
                    if index < len(name):
                        index += 1
                elif event.key == K_BACKSPACE and len(name) > 0:
                    name.pop(index - 1)
                    if index > 1:
                        index -= 1
                elif event.key == K_RETURN:
                    loop = False
                    return text
                elif (
                    len(name) <= 14
                    and event.unicode != "\x7f"
                    and event.key != K_UP
                    and event.key != K_DOWN
                ):
                    name.insert(index, event.unicode)
                    index += 1

        if name == []:
            index = 0

        pygame.draw.ellipse(win, (80, 80, 80), (55 + (index * 30), 321, 5, 30))

        textname = font.render(text, True, (20, 20, 20))
        win.blit(textname, (55, 321))

        pygame.display.update()


if __name__ == "__main__":
    print(enterPseudo())
