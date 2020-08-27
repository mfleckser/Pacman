class Node():
    def __init__(self, x, y, wall):
        self.x = x
        self.y = y
        self.wall = wall
        self.came_from = None
        self.g_score = float("inf")
        self.f_score = float("inf")



    def find_neighbors(self, spots, cols, rows):
        neighbors = []
        if self.x > 0:
            neighbors.append(spots[self.x - 1][ self.y])
        if self.x < cols - 1:
            neighbors.append(spots[self.x + 1][ self.y])
        if self.y > 0:
            neighbors.append(spots[self.x][ self.y - 1])
        if self.y < rows - 1:
            neighbors.append(spots[self.x][ self.y + 1])

        return neighbors
