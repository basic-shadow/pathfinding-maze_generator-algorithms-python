import random

class MazeGenerator:
    def __init__(self, start, columns, rows, grids, draw):
        self.draw = draw
        self.columns = columns
        self.rows = rows
        self.start = start
        self.visitedGrids = []
        self.grids = grids
        self.stack = []
        # self.one_grid = [                         #in Prims' algorithm
        #     lambda x, y: [x + 1, y],
        #     lambda x, y: [x - 1, y],
        #     lambda x, y: [x, y - 1],
        #     lambda x, y: [x, y + 1]
        # ]
        # self.two_grids = [
        #     lambda x, y: [x + 2, y],
        #     lambda x, y: [x - 2, y],
        #     lambda x, y: [x, y - 2],
        #     lambda x, y: [x, y + 2]
        # ]
        # self.list_grids = list(range(3))

    def divider(self):
        for x in range(self.rows):
            for y in range(self.columns):
                if x % 2 == 1 or y % 2 == 1:
                    self.grids[x][y].walls()

    def generator(self):
        self.divider()
        x = random.randrange(0, self.rows - 1, 2)
        y = random.randrange(0, self.columns - 1, 2)
        self.stack.append(self.grids[x][y])
        self.visitedGrids.append([self.grids[x][y].getPos()])
        current = self.grids[x][y]
        current.current()
        while len(self.stack) > 0:
            each_grid = []
            current.maze()
            x, y = current.getPos()[0], current.getPos()[1]
            if [x + 2, y] not in self.visitedGrids and not self.out_of_bounds([x + 2, y]) and not self.grids[x + 2][y].isWalls():
                each_grid.append("right")
            if [x - 2, y] not in self.visitedGrids and not self.out_of_bounds([x - 2, y]) and not self.grids[x - 2][y].isWalls():
                each_grid.append("left")
            if [x, y - 2] not in self.visitedGrids and not self.out_of_bounds([x, y - 2]) and not self.grids[x][y - 2].isWalls():
                each_grid.append("top")
            if [x, y + 2] not in self.visitedGrids and not self.out_of_bounds([x, y + 2]) and not self.grids[x][y + 2].isWalls():
                each_grid.append("bottom")

            if len(each_grid) > 0:
                random_grid = random.choice(each_grid)

                if random_grid == "right":
                    self.grids[x + 1][y].maze()
                    self.visitedGrids.append([x + 2, y])
                    self.stack.append(self.grids[x + 2][y])

                elif random_grid == "left":
                    self.grids[x - 1][y].maze()
                    self.visitedGrids.append([x - 2, y])
                    self.stack.append(self.grids[x - 2][y])

                elif random_grid == "top":
                    self.grids[x][y - 1].maze()
                    self.visitedGrids.append([x, y - 2])
                    self.stack.append(self.grids[x][y - 2])

                elif random_grid == "bottom":
                    self.grids[x][y + 1].maze()
                    self.visitedGrids.append([x, y + 2])
                    self.stack.append(self.grids[x][y + 2])
            else:
                current = self.stack.pop()
                current.current()

            self.draw()
        current.maze()

    def out_of_bounds(self, pos):
        return pos[0] < 0 or pos[1] < 0 or pos[0] >= self.rows or pos[1] >= self.columns
