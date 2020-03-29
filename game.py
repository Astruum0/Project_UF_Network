import pygame
import random


class Panel:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.longueur = 120
        self.largeur = 20

        self.vel = 15

    def moveUp(self):
        self.y -= self.vel

    def moveDown(self):
        self.y += self.vel

    def wallCollideUp(self):
        if self.y <= 0:
            return True
        else:
            return False

    def wallCollideDown(self):
        if self.y >= 380:
            return True
        else:
            return False

    def draw(self, win):
        pygame.draw.rect(
            win, (255, 255, 255), (self.x, self.y, self.largeur, self.longueur)
        )


class Ball:
    def __init__(self):
        self.x = 390
        self.y = 240
        self.taille = 20
        direction = random.randint(0, 3)
        if direction == 0:
            self.vx = 5
            self.vy = 5
        if direction == 1:
            self.vx = 5
            self.vy = -5
        if direction == 2:
            self.vx = -5
            self.vy = 5
        if direction == 3:
            self.vx = -5
            self.vy = -5

    def checkCollision(self, Lpanel, Rpanel):
        if self.y <= 0 or self.y >= 480:
            self.vy *= -1

        if (
            self.x <= 40
            and self.x >= 20
            and self.y >= Lpanel.y
            and self.y <= Lpanel.y + 120
        ) or (
            self.x >= 740
            and self.x <= 760
            and self.y >= Rpanel.y
            and self.y <= Rpanel.y + 120
        ):
            self.vx *= -1
            if self.vx > 0:
                self.vx += 1
            if self.vx < 0:
                self.vx -= 1
            if self.vy > 0:
                self.vy += 1
            if self.vy < 0:
                self.vy -= 1

    def reset(self):
        self.x = 390
        self.y = 240
        direction = random.randint(0, 3)
        if direction == 0:
            self.vx = 5
            self.vy = 5
        if direction == 1:
            self.vx = 5
            self.vy = -5
        if direction == 2:
            self.vx = -5
            self.vy = 5
        if direction == 3:
            self.vx = -5
            self.vy = -5

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, win):
        pygame.draw.ellipse(
            win, (255, 255, 255), (self.x, self.y, self.taille, self.taille)
        )


class Game:
    numbers = [pygame.image.load(f"score/{i}.png") for i in range(8)]

    def __init__(self, id):
        self.id = id
        self.p1 = Panel(20, 200)
        self.p2 = Panel(760, 200)
        self.ball = Ball()
        self.score = [0, 0]

        self.connected = False

    def movePanel(self, p, move):
        if p == 0 and move == "UP" and not self.p1.wallCollideUp():
            self.p1.moveUp()
        if p == 1 and move == "UP" and not self.p2.wallCollideUp():
            self.p2.moveUp()
        if p == 0 and move == "DOWN" and not self.p1.wallCollideDown():
            self.p1.moveDown()
        if p == 1 and move == "DOWN" and not self.p2.wallCollideDown():
            self.p2.moveDown()

    def updateScore(self):
        if self.ball.x >= 800:
            self.ball.reset()
            self.score[0] += 1
        if self.ball.x <= -20:
            self.score[1] += 1
            self.ball.reset()

    def update(self):
        self.updateScore()
        self.ball.checkCollision(self.p1, self.p2)
        self.ball.update()

        if 7 in self.score:
            self.reset()

    def show(self, win):
        self.p1.draw(win)
        self.p2.draw(win)
        self.ball.draw(win)

        win.blit(Game.numbers[self.score[0]], (351, 20))
        win.blit(Game.numbers[self.score[1]], (410, 20))

    def reset(self):
        self.ball.reset
        self.p1.y = 200
        self.p2.y = 200
        self.score = [0, 0]
