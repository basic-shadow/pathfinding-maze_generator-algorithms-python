import random
import pygame

class MazeGenerator:
    def __init__(self, columns, rows, grids, draw):
        self.draw = draw
        self.columns = columns
        self.rows = rows
        self.toVisitGrids = []
        self.grids = grids
        self.connectedGrids = []
        self.one_grid = [
            lambda x, y: [x + 1, y],
            lambda x, y: [x - 1, y],
            lambda x, y: [x, y - 1],
            lambda x, y: [x, y + 1]
        ]
        self.two_grids = [
            lambda x, y: [x + 2, y],
            lambda x, y: [x - 2, y],
            lambda x, y: [x, y - 2],
            lambda x, y: [x, y + 2]
        ]
        self.list_grids = list(range(4))
        self.clock = pygame.time.Clock()

    def generator(self):

        # Initial maze
        x, y = random.randint(0, self.rows - 1), random.randint(0, self.columns - 1)
        self.getWalls(x, y)
        self.getNeighbors(x, y)

        self.connectedGrids.append(self.grids[x][y])
        k = 20
        # Connecting mazes
        while len(self.toVisitGrids) > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        k = 100
            self.clock.tick(k)
            self.getWalls(x, y)
            self.getNeighbors(x, y)

            # Random neighbor connection
            for index in self.shuffle_range():
                dx, dy = self.two_grids[index](x, y)
                if not self.out_of_bounds([dx, dy]) and self.grids[dx][dy] in self.connectedGrids and self.grids[x][y].isNeighbor():
                    if dx > x:
                        self.grids[dx - 1][dy].maze()
                        self.grids[x][y].maze()
                        break
                    elif dx < x:
                        self.grids[dx + 1][dy].maze()
                        self.grids[x][y].maze()
                        break
                    elif dy > y:
                        self.grids[x][dy - 1].maze()
                        self.grids[x][y].maze()
                        break
                    elif dy < y:
                        self.grids[x][dy + 1].maze()
                        self.grids[x][y].maze()
                        break

            random.shuffle(self.toVisitGrids)
            next = self.toVisitGrids.pop()
            x, y = next.getPos()
            self.connectedGrids.append(next)
            self.draw()
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grids[i][j].isRemaining():
                    self.grids[i][j].walls()

    def getWalls(self, x, y):
        for neighbor in self.one_grid:
            dx, dy = neighbor(x, y)
            if not self.out_of_bounds([dx, dy]) and not self.grids[dx][dy].isMaze():
                self.grids[dx][dy].walls()

    def getNeighbors(self, x, y):
        for neighbor in self.two_grids:
            dx, dy = neighbor(x, y)
            if not self.out_of_bounds([dx, dy]) and not self.grids[dx][dy].isWalls() and not self.grids[dx][dy].isMaze():
                self.toVisitGrids.append(self.grids[dx][dy])
                self.grids[dx][dy].neighbor()

    def shuffle_range(self):
        random.shuffle(self.list_grids)
        return self.list_grids

    def out_of_bounds(self, pos):
        return pos[0] < 0 or pos[1] < 0 or pos[0] >= self.rows or pos[1] >= self.columns
