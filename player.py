import math
import pygame
pygame.init()

scale = 20
cols = 28

class Player():
    def __init__(self, x, y, xv, yv):
        self.x = x
        self.y = y
        self.realX = self.x * scale + scale // 2
        self.realY = self.y * scale + scale // 2
        self.xv = xv
        self.yv = yv
        self.nextX = 0
        self.nextY = 0
        self.score = 0
        self.lives = 3

    def show(self, surface):
        pygame.draw.circle(surface, (255, 255, 0), (self.realX, self.realY), int(scale / 1.3))

    def move(self):
        self.realX += self.xv * 4
        self.realY += self.yv * 4
        if self.realX % scale == 10:
            self.x = math.floor(self.realX // scale)
        if self.realY % scale == 10:
            self.y = math.floor(self.realY // scale)

        if self.realX < 0:
            self.realX = (cols - 1) * scale - 10
            self.x = cols - 1
        if self.realX > cols * scale:
            self.realX = 10
            self.x = 0
