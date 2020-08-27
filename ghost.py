import math
import random
import pygame
from node import Node
pygame.init()

scale = 20
grid = []



# ~ turns = [Node(1, 1), Node(6, 1), Node(12, 1), Node(15, 1), Node(21, 1), Node(26, 1),
# ~ Node(1, 5), Node(6, 5), Node(9, 5), Node(12, 5), Node(15, 5), Node(18, 5), Node(21, 5), Node(26, 5),
# ~ Node(1, 8), Node(6, 8), Node(9, 8), Node(12, 8), Node(15, 8), Node(18, 8), Node(21, 8), Node(26, 8),
# ~ Node(9, 11), Node(12, 11), Node(15, 11), Node(18, 11),
# ~ Node(6, 14), Node(9, 14), Node(18, 14), Node(21, 14),
# ~ Node(9, 17), Node(18, 17),
# ~ Node(1, 20), Node(6, 20), Node(9, 29), Node(12, 20), Node(15, 20), Node(18, 20), Node(21, 20), Node(26, 20),
# ~ Node(1, 23), Node(3, 23), Node(6, 23), Node(9, 23), Node(12, 23), Node(15, 23), Node(18, 23), Node(21, 23), Node(24, 23), Node(26, 23),
# ~ Node(1, 26), Node(3, 26), Node(6, 26), Node(9, 26), Node(12, 26), Node(15, 26), Node(18, 26), Node(21, 26), Node(24, 26), Node(26, 26),
# ~ Node(1, 29), Node(12, 29), Node(15, 29), Node(26, 29)]

# ~ neighbors = [[1,6],[0,7,2],[1,9,3],[2,10,4],[3,12,5],[4,13],
# ~ [0,7,14],[6,15,8,1],[7,16,9],[8,17,10,3],[10,19,12],[11,20,13,4],[12,21,5],
# ~ [6,15],[14,26,16,7],[8,17],[16,23],[24,19],[12,21,29],[20,13],

def init(g):
    global grid
    grid = []

    for i in g:
        col = []
        for j in i:
            col.append(Node(j.x, j.y, j.wall))
        grid.append(col)


def distance(x1, y1, x2, y2):
    a = abs(x1 - x2)
    b = abs(y1 - y2)
    c = math.sqrt(pow(a, 2) + pow(b, 2))
    return c


def build_path(spots, start, end):
    path = []
    current = end
    while current.came_from:
        path.append(current)
        current = current.came_from
    path.append(start)
    return path[::-1]




class Ghost():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.realX = self.x * scale + scale // 2
        self.realY = self.y * scale + scale // 2
        self.xv = 0
        self.yv = 0
        self.path = []
        self.color = color
        self.speed = 4

    def show(self, surface):
        pygame.draw.circle(surface, self.color, (self.realX, self.realY), int(scale / 1.3))

        if self.path:
            for i in self.path[::-1]:
                if i.came_from:
                    pygame.draw.line(surface, self.color, (i.x * scale + scale // 2, i.y * scale + scale // 2), (i.came_from.x * scale + scale // 2, i.came_from.y * scale + scale // 2), 5)

    def get_path(self, target):
        global grid
        """
        Target = (x,y) touple
        x = int
        y = int
        """
        open_set = []
        start = grid[math.floor(self.realX // scale)][math.floor(self.realY // scale)]
        end = grid[target[0]][target[1]]

        open_set.append(start)
        start.g_score = 0
        start.f_score = distance(start.x, start.y, end.x, end.y)

        while len(open_set) > 0:

            current = sorted(open_set, key=lambda x: x.f_score)[0]
            if current == end:
                self.path = build_path(grid, start, end)

            open_set.remove(current)

            for neighbor in current.find_neighbors(grid, len(grid), len(grid[0])):
                if current == start:
                    if (neighbor.x == self.x - self.xv) and (neighbor.y == self.y - self.yv):
                        continue
                if not neighbor.wall:
                    tempG = current.g_score + distance(current.x, current.y, neighbor.x, neighbor.y)
                    if tempG < neighbor.g_score:
                        neighbor.came_from = current
                        neighbor.g_score = tempG
                        neighbor.f_score = tempG + distance(neighbor.x, neighbor.y, end.x, end.y)
                        if not neighbor in open_set:
                            open_set.append(neighbor)


    def move(self):
        try:
            next_move = self.path[1]
        except IndexError:
            next_move = self.path[0]

        if self.x > next_move.x and self.realY % scale == 10:
            self.xv = -1
            self.yv = 0
        elif self.x < next_move.x and self.realY % scale == 10:
            self.xv = 1
            self.yv = 0
        elif self.y > next_move.y and self.realX % scale == 10:
            self.xv = 0
            self.yv = -1
        elif self.y < next_move.y and self.realX % scale == 10:
            self.xv = 0
            self.yv = 1

        self.realX += self.xv * self.speed
        self.realY += self.yv * self.speed
        self.x = math.floor(self.realX // scale)
        self.y = math.floor(self.realY // scale)

