import pygame
from database import Database
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION
from hided import *

try:
    database = Database(mysql_config)
    database.connect()
except:
    pass


def get_personal_stat(pseudo):
    return (database.get(f"SELECT user_name, win_pong, win_ttt, win_snake FROM users WHERE user_name = '{pseudo}'"))[0]

def get_global_stat(jeu):
    return (database.get(f"SELECT user_name, win_{jeu} FROM users ORDER BY win_{jeu} DESC"))

def stats(pseudo):
    pygame.init()
    pygame.font.init()
    font = pygame.font.Font(
        "fonts/PixelOperator8.ttf", 30
    )
    win = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("PyNetGames")

    run = True
    bg = pygame.image.load("menu_sprites/stat.png")
    hover = pygame.image.load("menu_sprites/hover.png")
    
    stat = get_personal_stat(pseudo)
    info = []
    for inf in stat:
        if inf == stat[0]:
            info.append(font.render(f"{pseudo}", 1, (254, 58, 53)))
        else:
            info.append(font.render(f"{str(inf)} win", 1, (254, 58, 53)))
    coord = [(600/2 - info[0].get_width() // 2, 145), (290, 200), (310, 310), (320, 425)]
            
    while run:
        win.blit(bg, (0, 0))
        for i, inf in enumerate(info):
            win.blit(inf, coord[i])
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if 60 < mouse_x < 540 and 500 < mouse_y < 570:
            win.blit(hover, (57, 503))
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
                break
            if event.type == MOUSEBUTTONDOWN and 60 < mouse_x < 540 and 500 < mouse_y < 570:
                leaderboard(pseudo)

            pygame.display.update()

def leaderboard(pseudo):
    pygame.init()
    pygame.font.init()
    font = pygame.font.Font(
        "fonts/PixelOperator8.ttf", 30
    )
    win = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("PyNetGames")

    run = True
    bg = pygame.image.load("menu_sprites/leaderboard.png")
    hover = pygame.image.load("menu_sprites/hover2.png")
    
    stat = []
    page = 0
    choosed_category = None
    
    while run:
        win.blit(bg, (0, 0))
        for i, people in enumerate(stat[page*5:page*5+5]):
            last = None
            for j, info in enumerate(people):
                if (page==0 and i==0):
                    couleur = (255,215,0)
                elif (page==0 and i==1):
                    couleur = (192,192,192)
                elif (page==0 and i==2):
                    couleur = (205, 127, 50)
                elif str(info)== pseudo or last == pseudo:
                    couleur = (255, 255, 255)
                    last = pseudo
                else:
                    couleur = (254, 58, 53)
                win.blit(font.render(str(info), 1, couleur), (100+j*350, 250+i*50))
        if choosed_category == "pong":
            win.blit(hover, (117, 149))
        if choosed_category == "ttt":
            win.blit(hover, (272, 149))
        if choosed_category == "snake":
            win.blit(hover, (427, 149))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if 150 < mouse_y < 200:
            if 120 < mouse_x < 170:
                win.blit(hover, (117, 149))
            if 275 < mouse_x < 325:
                win.blit(hover, (272, 149))
            if 430 < mouse_x < 480:
                win.blit(hover, (427, 149))
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
                break
            if event.type == MOUSEBUTTONDOWN:
                if 150 < mouse_y < 200:
                    if 120 < mouse_x < 170:
                        stat = get_global_stat("pong")
                        choosed_category = "pong"
                        page = 0
                    if 275 < mouse_x < 325:
                        stat = get_global_stat("ttt")
                        choosed_category = "ttt"
                        page = 0
                    if 430 < mouse_x < 480:
                        stat = get_global_stat("snake")
                        choosed_category = "snake"
                        page = 0
                if 510 < mouse_y < 560:
                    if 480 < mouse_x < 530:
                        if stat[(page+1)*5:(page+1)*5+5] != []:
                            page += 1
                    if 65 < mouse_x < 120:
                        if page > 0:
                            page -= 1

            pygame.display.update()
leaderboard("Matteo")
