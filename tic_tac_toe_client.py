from random import randint
from network_for_client import Network
import pygame

pygame.init()
width = 616
height = 700
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Tic-Tac-Toe")
grille = pygame.image.load('sprites_tic_tac_toe/board.png')
font = pygame.font.SysFont("", 80)

run = True
can_Play = True
end = False
winner = 0
    
net = Network("Tic_Tac_Toe", "Test")
player = int(net.getP())
if player + 1 == 1:
    number_player = 1
else:
    number_player = -1
print("You are Player", player + 1)

while run:
    win.blit(grille, (0,0))
    game = net.send("get,")
    if game.connected:
        can_Play = game.can_play[player]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP and can_Play == True:
                
                mouse_x, mouse_y = pygame.mouse.get_pos()
                x, y = -1, -1
                    
                for i in range(0,3):
                    if (i*190)+60 < mouse_x < (i*190)+200:
                        y = i

                for i in range(0,3):
                    if (i*170)+200 < mouse_y < (i*170)+330:
                        x = i
                game = net.send(f"pos,{x},{y},{number_player}")
    game.Show(win)

    pygame.display.update()
pygame.QUIT
