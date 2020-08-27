
class Tile():
    def __init__(self, x, y, wall, small, big, gate):
        self.x = x
        self.y = y
        self.wall = wall
        self.small = small
        self.big = big
        self.gate = gate
        self.blocked = wall or gate
