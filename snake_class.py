import pygame
from pygame.locals import QUIT, K_UP, K_LEFT, K_RIGHT, K_DOWN, K_SPACE, K_s
from random import randint


class Snake:
    colors = [(52, 152, 219), (231, 76, 60), (46, 204, 113), (155, 89, 182)]

    def __init__(self, coords, i, length=3, start_dir="UP"):
        self.snake_id = i
        self.coords = [coords for _ in range(length)]
        self.directions = ["none" for _ in range(length - 1)] + [start_dir]
        self.size = 5
        self.lives = 3
        self.state = "normal"

    def updateSnakePos(self):

        for i, direction in enumerate(self.directions):
            x, y = self.coords[i]
            if direction == "UP":
                y -= self.size
            elif direction == "DOWN":
                y += self.size
            elif direction == "LEFT":
                # print(self.coords)
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

    def move(self, direction):
        self.directions[-1] = direction

    def append_length(self, iterate):
        for _ in range(iterate):
            self.coords.insert(0, self.coords[0])
            self.directions.insert(0, "none")

    def show(self, win):
        for x, y in self.coords:
            pygame.draw.rect(
                win, Snake.colors[self.snake_id], (x, y, self.size, self.size)
            )


class snake_game:
    starting_coords = [(100, 100), (595, 100), (100, 595), (595, 595)]
    starting_dirs = ["RIGHT", "LEFT"]

    def __init__(self, id):
        self.id = id
        self.players = []
        self.players_nbr = 0
        self.new_apple()
        self.started = False

    def newPlayer(self):
        self.players.append(
            Snake(
                snake_game.starting_coords[self.players_nbr],
                self.players_nbr,
                length=30,
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

    def show(self, win):
        for s in self.players:
            s.show(win)
        pygame.draw.ellipse(
            win, (243, 156, 18), self.apple,
        )


if __name__ == "__main__":

    win = pygame.display.set_mode((700, 700))
    clock = pygame.time.Clock()
    jeu = True

    game = snake_game(0)
    game.newPlayer()
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
