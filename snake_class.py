import pygame
from pygame.locals import QUIT, K_UP, K_LEFT, K_RIGHT, K_DOWN, K_SPACE, K_s
from random import randint
import time


class Snake:
    colors = [
        (52, 152, 219),
        (231, 76, 60),
        (46, 204, 113),
        (155, 89, 182),
        (90, 90, 90),
    ]
    hearts = [pygame.image.load(f"sprites_snake/hearts{i}.png") for i in range(1, 4)]

    forbidden_move = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}

    def __init__(self, coords, i, name, length=20, start_dir="UP"):
        self.snake_id = i
        self.name = name
        self.coords = [coords for _ in range(length)]
        self.directions = ["none" for _ in range(length - 1)] + [start_dir]
        self.starting_coords = coords
        self.startdir = start_dir
        self.startlength = length
        self.size = 5
        self.lives = 3
        self.state = "normal"
        self.color = Snake.colors[self.snake_id]
        self.blink = True
        self.blinkIndex = 0
        self.font_size = 30

    def updateSnakePos(self):

        for i, direction in enumerate(self.directions):
            x, y = self.coords[i]
            if direction == "UP":
                y -= self.size
            elif direction == "DOWN":
                y += self.size
            elif direction == "LEFT":
                x -= self.size
            elif direction == "RIGHT":
                x += self.size

            if x >= 700:
                x = 0
            elif x < 0:
                x = 695
            if y >= 700:
                y = 0
            elif y < 0:
                y = 695

            self.coords[i] = (x, y)

        for i in range(len(self.directions) - 1):
            self.directions[i] = self.directions[i + 1]

    def checkCollision(self, snakes):

        if self.state == "normal":
            head_x, head_y = self.coords[-1]

            for s in snakes:
                for x, y in s.coords[:-1]:
                    if s.state == "normal":
                        if x == head_x and y == head_y:
                            self.lives -= 1
                            self.startInvicibleTime = time.time()
                            self.state = "invulnerable"

        elif (
            self.state == "invulnerable" and time.time() - self.startInvicibleTime > 2.5
        ):
            self.state = "normal"

        if self.state == "invulnerable":
            self.blinkIndex += 1
            if self.blinkIndex >= 15:
                self.blink = not self.blink
                self.blinkIndex = 0

    def dead(self):
        if self.lives <= 0:
            self.state = "dead"
            return True
        else:
            return False

    def move(self, direction):
        if (
            direction != "none"
            and not Snake.forbidden_move[self.directions[-1]] == direction
        ):
            self.directions[-1] = direction

    def append_length(self, iterate):
        for _ in range(iterate):
            self.coords.insert(0, self.coords[0])
            self.directions.insert(0, "none")

    def show(self, win):
        for x, y in self.coords:
            if self.state == "normal":
                pygame.draw.rect(
                    win, Snake.colors[self.snake_id], (x, y, self.size, self.size)
                )
            elif self.state == "invulnerable" and self.blink:
                pygame.draw.rect(win, Snake.colors[4], (x, y, self.size, self.size))

    def showStats(self, win):
        if self.lives > 0:
            win.blit(Snake.hearts[self.lives - 1], (900, 52 + self.snake_id * 120))

    def reset(self):
        self.coords = [self.starting_coords for _ in range(self.startlength)]
        self.directions = ["none" for _ in range(self.startlength - 1)] + [
            self.startdir
        ]
        # self.pseudo = self.font.render(self.name, 1, (255, 255, 255), True)
        self.lives = 3
        self.state = "normal"


class Snake_game:
    # pygame.font.init()
    starting_coords = [(100, 100), (595, 100), (100, 595), (595, 595)]
    starting_dirs = ["RIGHT", "LEFT"]

    def __init__(self, id):
        self.id = id
        self.players = []
        self.players_nbr = 0
        self.dead_players = []
        self.new_apple()

        self.showWinner = False

        self.started = False

    def newPlayer(self, name):
        self.players.append(
            Snake(
                Snake_game.starting_coords[self.players_nbr],
                self.players_nbr,
                name,
                length=20,
                start_dir=Snake_game.starting_dirs[self.players_nbr % 2],
            )
        )
        self.players_nbr = len(self.players)

    def moveSnake(self, snake_id, direction):
        for s in self.players:
            if s.snake_id == snake_id:
                s.move(direction)

    def new_apple(self):
        self.apple = (randint(0, 137) * 5, randint(0, 137) * 5, 15, 15)

    def update(self):
        if not self.showWinner:
            for s in self.players:
                s.updateSnakePos()
                head_x, head_y = s.coords[-1]
                if (
                    head_x >= self.apple[0]
                    and head_x < self.apple[0] + self.apple[2]
                    and head_y >= self.apple[1]
                    and head_y < self.apple[1] + self.apple[3]
                ):
                    s.append_length(10)
                    self.new_apple()

                s.checkCollision(self.players)
                if s.dead():
                    self.players.remove(s)
                    self.dead_players.append(s)

            if len(self.players) == 1:
                self.startTimeShowWinner = time.time()
                self.showWinner = True
                self.winner = self.players[0]

        else:
            if time.time() - self.startTimeShowWinner > 3:
                self.showWinner = False
                self.reset()

    def reset(self):
        self.players = self.players + self.dead_players
        for s in self.players:
            s.reset()
        self.dead_players = []
        self.new_apple()
        self.showWinner = False
        self.started = False

    def show(self, win):
        if not self.showWinner:
            for s in self.players:
                s.show(win)
            pygame.draw.ellipse(
                win, (243, 156, 18), self.apple,
            )
        for all_s in self.players + self.dead_players:
            all_s.showStats(win)

        pygame.draw.line(win, (255, 255, 255), (700, 0), (700, 700), 2)


def show_font(game, win, font, surfaces):
    if game.started and len(game.players) == 1:
        winnerSurface = font.render(game.winner.name, 1, (game.winner.color), True)
        winsSurface = font.render("Wins !", 1, (game.winner.color), True)

    if game.showWinner:
        win.blit(
            winnerSurface,
            (
                700 // 2 - winnerSurface.get_width() // 2,
                700 // 2 - winnerSurface.get_height() // 2 - 21,
            ),
        )
        win.blit(
            winsSurface,
            (
                700 // 2 - winsSurface.get_width() // 2,
                700 // 2 - winsSurface.get_height() // 2 + 21,
            ),
        )
    for p, surface in zip(game.players, surfaces):
        win.blit(
            surface[1] if p.state == "dead" else surface[0],
            (
                895 - surface[1].get_width(),
                50 + p.snake_id * 120 + (30 - surface[1].get_height()) // 2,
            ),
        )
