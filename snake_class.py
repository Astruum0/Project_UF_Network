import pygame
from pygame.locals import QUIT, K_UP, K_LEFT, K_RIGHT, K_DOWN, K_SPACE, K_s
from random import randint
import time

pygame.font.init()


class Snake:
    colors = [
        (52, 152, 219),
        (231, 76, 60),
        (46, 204, 113),
        (155, 89, 182),
        (90, 90, 90),
    ]
    hearts = [pygame.image.load(f"sprites_snake/hearts{i}.png") for i in range(1, 4)]

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
        self.font = pygame.font.Font("PixelOperator8.ttf", self.font_size)
        self.pseudo = self.font.render(self.name, 1, (255, 255, 255), True)

        while self.pseudo.get_width() > 180:
            self.font_size -= 1
            self.font = pygame.font.Font("PixelOperator8.ttf", self.font_size)
            self.pseudo = self.font.render(self.name, 1, (255, 255, 255), True)

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

    def dead(self):
        if self.lives <= 0:
            self.state = "dead"
            self.pseudo = self.font.render(self.name, 1, (80, 80, 80,), True)
            return True
        else:
            return False

    def move(self, direction):
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

        if self.state == "invulnerable":
            self.blinkIndex += 1
            if self.blinkIndex >= 10:
                self.blink = not self.blink
                self.blinkIndex = 0

    def showStats(self, win):
        if self.lives > 0:
            win.blit(Snake.hearts[self.lives - 1], (900, 52 + self.snake_id * 120))
        win.blit(
            self.pseudo,
            (
                895 - self.pseudo.get_width(),
                50 + self.snake_id * 120 + (30 - self.font_size) // 2,
            ),
        )

    def reset(self):
        self.coords = [self.starting_coords for _ in range(self.startlength)]
        self.directions = ["none" for _ in range(self.startlength - 1)] + [
            self.startdir
        ]
        self.pseudo = self.font.render(self.name, 1, (255, 255, 255), True)
        self.lives = 3
        self.state = "normal"


class snake_game:
    starting_coords = [(100, 100), (595, 100), (100, 595), (595, 595)]
    starting_dirs = ["RIGHT", "LEFT"]
    font = pygame.font.Font("PixelOperator8.ttf", 40)

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
                snake_game.starting_coords[self.players_nbr],
                self.players_nbr,
                name,
                length=20,
                start_dir=snake_game.starting_dirs[self.players_nbr % 2],
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
                self.winnerSurface = snake_game.font.render(
                    self.winner.name, 1, (self.winner.color), True
                )
                self.winsSurface = snake_game.font.render(
                    "Wins !", 1, (self.winner.color), True
                )

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

        if self.showWinner:
            win.blit(
                self.winnerSurface,
                (
                    700 // 2 - self.winnerSurface.get_width() // 2,
                    700 // 2 - self.winnerSurface.get_height() // 2 - 21,
                ),
            )
            win.blit(
                self.winsSurface,
                (
                    700 // 2 - self.winsSurface.get_width() // 2,
                    700 // 2 - self.winsSurface.get_height() // 2 + 21,
                ),
            )

        pygame.draw.line(win, (255, 255, 255), (700, 0), (700, 700), 2)


if __name__ == "__main__":

    win = pygame.display.set_mode((1000, 700))
    clock = pygame.time.Clock()
    jeu = True

    game = snake_game(0)
    game.newPlayer("Astruum")
    game.newPlayer("o4")
    game.newPlayer("Malgache")
    while jeu:
        clock.tick(45)
        win.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                jeu = False

        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            game.moveSnake(0, "UP")
        if keys[K_DOWN]:
            game.moveSnake(0, "DOWN")
        if keys[K_LEFT]:
            game.moveSnake(0, "LEFT")
        if keys[K_RIGHT]:
            game.moveSnake(0, "RIGHT")
        if keys[K_SPACE]:
            for s in game.players:
                s.append_length(1)
        if keys[K_s]:
            game.started = True

        if game.started:
            game.update()
        game.show(win)

        pygame.display.update()
