from tile import Tile
from player import Player
import ghost
import os
import random
import pygame
pygame.init()

screenWidth = 560
screenHeight = 620
rows = 31
cols = 28
scale = screenWidth // cols

player = Player(13, 23, -1, 0)
blinky = ghost.Ghost(13, 12, (255, 0, 0))
pinky = ghost.Ghost(14, 14, (255, 127, 255))
inky = ghost.Ghost(13, 13, (0, 255, 255))
clyde = ghost.Ghost(14, 13, (255, 155, 0))

mode = "c"
counter = 0

win = pygame.display.set_mode((screenWidth, screenHeight + 50))
game = pygame.Surface((screenWidth, screenHeight))
pygame.display.set_caption("Pacman")
font = pygame.font.SysFont("comicsans", 50)

clock = pygame.time.Clock()

background = pygame.image.load(os.path.join("pics", "pacman_background.png"))

grid = []
map_file = open("map.txt", "r")
map_text = []
for line in map_file:
    r = []
    for char in line:
        if not char == "\n":
            r.append(char)
    map_text.append(r)

for i in range(len(map_text[0])):
    c = []
    for j in range(len(map_text)):
        cur = map_text[j][i]
        wall = cur == "w"
        small = cur == "s"
        big = cur == "b"
        gate = cur == "g"
        c.append(Tile(i, j, wall, small, big, gate))
    grid.append(c)

ghost.init(grid)

def redrawGame(surface):
    global screenWidth, screenHeight, cols, rows, scale, grid, background, player, blinky, pinky

    #pygame.draw.rect(surface, (0, 0, 0), (0, 0, screenWidth, screenHeight))
    surface.blit(background, (0, 0, screenWidth, screenHeight))

    for i, col in enumerate(grid):
        for j, corowl in enumerate(col):
            if grid[i][j].small:
                pygame.draw.circle(surface, (255, 255, 0), (i * scale + scale // 2, j * scale + scale // 2), scale // 6)
            elif grid[i][j].big:
                pygame.draw.circle(surface, (255, 255, 0), (i * scale + scale // 2, j * scale + scale // 2), int(scale // 2.25))
            # ~ elif grid[i][j].wall:
                # ~ pygame.draw.rect(surface, (0, 0, 255), (i * scale, j * scale, scale, scale))
                # ~ pass


    player.show(surface)
    blinky.show(surface)
    pinky.show(surface)
    inky.show(surface)
    clyde.show(surface)

def redrawExtra(surface):
    global font, player, screenWidth

    scoreText = font.render("Score: " + str(player.score), True, (245, 245, 220), (0, 0, 0))
    lifeText = font.render("Lives: " + str(player.lives), True, (245, 245, 220), (0, 0, 0))

    surface.blit(scoreText, (10, 10))
    surface.blit(lifeText, (screenWidth - lifeText.get_width() - 10, 10))

def gameOver(condition):
    global game, screenWidth, screenHeight, win, player

    gameOverFont = pygame.font.SysFont("comicsans", 130)
    gameOverText = gameOverFont.render("Game Over", True, (245, 245, 245))
    conditionText = gameOverFont.render("You " + condition.capitalize(), True, (245, 245, 245))
    game.blit(gameOverText, (screenWidth // 2 - gameOverText.get_width() // 2, screenHeight // 2 - gameOverText.get_height()))
    game.blit(conditionText, (screenWidth // 2 - conditionText.get_width() // 2, screenHeight // 2))
    win.blit(game, (0, 50))
    pygame.display.update()

    newBest = False

    cur = player.score
    f = open("highscore.txt", "r")
    high = int(f.read())
    f.close
    if condition == "win" and cur > high:
        newBest = True
        high = cur
        f = open("highscore.txt", "w")
        f.write(str(cur))
        f.close()

    print(high)

    c = 0
    newBestFont = pygame.font.SysFont("comicsans", 30)
    newBestText = newBestFont.render("New Highscore!", True, (255, 0, 0), (0, 0, 0))
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()

        if newBest and c < 100:
            win.blit(newBestText, (screenWidth // 2 - newBestText.get_width() // 2, 25 - newBestText.get_height() // 2))
        else:
            pygame.draw.rect(win, (0, 0, 0), (screenWidth // 2 - newBestText.get_width() // 2, 25 - newBestText.get_height() // 2, newBestText.get_width(), newBestText.get_height()))
        pygame.display.update()
        c += 1
        if c >= 150:
            c = 0

def main():
    global win, player, clock, grid, mode, counter, game
    from ghost import distance

    run = True
    while run:
        clock.tick(15)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()


        # Player
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            if player.realX % scale == 10 and not grid[player.x][player.y - 1].blocked:
                player.xv, player.yv = 0, -1
            else:
                player.nextY = -1
        elif keys[pygame.K_DOWN]:
            if player.realX % scale == 10 and not grid[player.x][player.y + 1].blocked:
                player.xv, player.yv = 0, 1
            else:
                player.nextY = 1
        elif keys[pygame.K_LEFT]:
            if player.realY % scale == 10 and not grid[player.x - 1][player.y].blocked:
                player.xv, player.yv = -1, 0
            else:
                player.nextX = -1
        elif keys[pygame.K_RIGHT]:
            if player.realY % scale == 10 and not grid[player.x + 1][player.y].blocked:
                player.xv, player.yv = 1, 0
            else:
                player.nextX = 1


        top = not grid[player.x][player.y - 1].blocked
        bottom = not grid[player.x][player.y + 1].blocked
        if player.x == cols - 1:
            right = True
        else:
            right = not grid[player.x + 1][player.y].blocked
        if player.x == 0:
            left = True
        else:
            left = not grid[player.x - 1][player.y].blocked

        if player.nextX == 1 and right:
            player.xv = 1
            player.yv = 0
            player.nextX = 0

        if player.nextX == -1 and left:
            player.xv = -1
            player.yv = 0
            player.nextX = 0

        if player.nextY == -1 and top:
            player.xv = 0
            player.yv = -1
            player.nextY = 0

        if player.nextY == 1 and bottom:
            player.xv = 0
            player.yv = 1
            player.nextY = 0

        try:
            if not grid[player.x + player.xv][player.y + player.yv].blocked:
                player.move()
        except IndexError:
            player.move()

        if grid[player.x][player.y].small:
            grid[player.x][player.y].small = False
            player.score += 10

        if grid[player.x][player.y].big:
            grid[player.x][player.y].big = False
            mode = "f"
            counter = 0


        # Ghosts
        ghost.init(grid)
        targets = []
        ghosts = [blinky, pinky, inky, clyde]

        if mode == "c":
            pn = None
            c = 5
            while not pn:
                try:
                    if not grid[player.x + player.xv * c][player.y + player.yv * c].wall:
                        pn = (player.x + player.xv * c, player.y + player.yv * c)
                        if player.x + player.xv * c <= 0 or player.x + player.xv * c >= cols or player.y + player.yv * c <= 0 or player.y + player.yv * c >= rows:
                            c -= 1
                            pn = None
                            continue
                    else:
                        c -= 1
                except IndexError:
                    c -= 1

            dx = player.x - blinky.x
            dy = player.y - blinky.y
            ix = player.x + dx
            iy = player.y + dy
            if ix <= 0:
                ix = 0
            if iy <= 0:
                iy = 0
            if ix >= cols - 1:
                ix = cols - 1
            if iy >= rows - 1:
                iy = rows - 1

            c = 0
            while grid[ix][iy].wall:
                if abs(ix) == ix:
                    ix -= 1
                else:
                    ix += 1
                if abs(iy) == iy:
                    iy -= 1
                else:
                    iy += 1
                if c > max(dx, dy):
                    ix, iy = player.x, player.y

                c += 1


            if distance(player.x, player.y, clyde.x, clyde.y) <= 8:
                cn = (1, 29)
            else:
                cn = (player.x, player.y)

            targets = [(player.x, player.y), pn, (ix, iy), cn]
        elif mode == "f":
            for i in range(4):
                tempX, tempY = 0, 0
                while grid[tempX][tempY].wall or (tempX, tempY) == (ghosts[i].x, ghosts[i].y):
                    tempX = random.randint(1, cols - 2)
                    tempY = random.randint(1, rows - 2)
                targets.append((tempX, tempY))
        elif mode == "s":
            targets = [(1, 1), (26, 1), (26, 29), (1, 29)]

        if mode == "f":
            for i in ghosts:
                i.speed = 2
        else:
            for i in ghosts:
                i.speed = 4

        blinky.get_path(targets[0])
        ghost.init(grid)
        pinky.get_path(targets[1])
        ghost.init(grid)
        inky.get_path(targets[2])
        ghost.init(grid)
        clyde.get_path(targets[3])

        blinky.move()
        pinky.move()
        inky.move()
        clyde.move()


        # Game Over Conditions

        for i in ghosts:
            if distance(player.realX, player.realY, i.realX, i.realY) + 3 <= int(scale / 1.3) * 2:
                if not mode == "f":
                    l = player.lives
                    s = player.score
                    if l == 0:
                        gameOver("lose")
                    player.__init__(13, 23, -1, 0)
                    player.lives = l
                    player.score = s
                    mode = "c"
                    player.lives -= 1
                    pygame.time.delay(600)
                    break
                else:
                    i.__init__(13, 10, i.color)
                    player.score += 200

        c = 0
        for i in grid:
            for j in i:
                if j.small or j.big:
                    c += 1

        if c == 0:
            gameOver("win")

        # Counter for ghost modes
        counter += 1

        if mode == "f" and counter == 130:
            counter = 0
            mode = "c"
            for g in ghosts:
                g.realX = g.x * scale + 10
                g.realY = g.y * scale + 10

        if mode == "c" and counter == 1000:
            mode = "s"

        if mode == "s" and counter == 1100:
            mode = "c"
            counter = 0


        redrawGame(game)
        win.blit(game, (0, 50))
        redrawExtra(win)
        pygame.display.update()


if __name__ == "__main__":
    pygame.time.delay(3000)
    main()
