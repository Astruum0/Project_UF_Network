from random import randint
import pygame

X = pygame.image.load("sprites_tic_tac_toe/x.png")
O = pygame.image.load("sprites_tic_tac_toe/o.png")


class Board:
    def __init__(self):
        self.board = [[0] * 3 for i in range(3)]
        self.end = False
        self.winner = 0

    def Show(self, win):
        global X, O
        dico = {
            0: [80, 200],
            1: [250, 200],
            2: [420, 200],
            3: [80, 380],
            4: [250, 380],
            5: [420, 380],
            6: [80, 550],
            7: [250, 550],
            8: [420, 550],
        }
        for i, row in enumerate(self.board):
            for j, case in enumerate(row):
                if case == -1:
                    win.blit(O, dico[3 * i + j])
                elif case == 1:
                    win.blit(X, dico[3 * i + j])

    def Place(self, x, y, player):
        self.board[x][y] = player
        self.Win()
        if self.Number_Empty_Cells() == 0:
            self.end, self.winner = True, 0

    def Check(self, x, y):
        if 0 <= x <= 2 and 0 <= y <= 2 and self.board[x][y] == 0:
            return True
        else:
            return False

    def Number_Empty_Cells(self):
        cells = []
        for x, row in enumerate(self.board):
            for y, cell in enumerate(row):
                if cell == 0:
                    cells.append([x, y])
        return len(cells)

    def Win(self):
        board = self.board
        win_state = [
            [board[0][0], board[0][1], board[0][2]],
            [board[1][0], board[1][1], board[1][2]],
            [board[2][0], board[2][1], board[2][2]],
            [board[0][0], board[1][0], board[2][0]],
            [board[0][1], board[1][1], board[2][1]],
            [board[0][2], board[1][2], board[2][2]],
            [board[0][0], board[1][1], board[2][2]],
            [board[2][0], board[1][1], board[0][2]],
        ]
        if [-1, -1, -1] in win_state:
            self.end, self.winner = True, -1
        if [1, 1, 1] in win_state:
            self.end, self.winner = True, 1


class Tic_Tac_Toe_Game:
    def __init__(self, id):
        self.id = id
        self.board = Board()
        self.can_play = [True, False]
        self.connected = False

    def Update(self, x, y, number_player):
        if self.board.Check(x, y):
            self.board.Place(x, y, number_player)
            self.can_play = [not (i) for i in self.can_play]
        # self.board.Win()

    def Show(self, win):
        self.board.Show(win)

    def Reset(self, id):
        self.id = id
        self.board = Board()
