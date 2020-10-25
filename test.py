import pygame
import sys
import a_star_pathfinding_algorithm as a_algorithm
import random

pygame.init()

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (190, 190, 190)
GREEN = (0, 128, 0)
ORANGE = (255,140,0)
PURPLE = (150, 0, 210)

finish = False
width = 800
rows = 50
columns = 50
if rows < columns:
    margin = width // rows
else:
    margin = width // columns

screen = pygame.display.set_mode((800, 800))

class grid():
    def __init__(self, pos,rows,columns, color = WHITE):
        self.x, self.y = pos
        self.color = color
        self.neighbors = []
        self.rows = rows
        self.columns = columns
        self.gCost = 0
        self.hCost = 0
        self.fCost = 0
    def closeSet(self):
        self.color = YELLOW
    def openSet(self):
        self.color = RED
    def startPos(self):
        self.color = YELLOW
    def endPos(self):
        self.color = BLUE
    def getPath(self):
        self.color = PURPLE
    def maze(self):
        self.color = WHITE
    def getPos(self):
        return [self.x, self.y]
    def isMaze(self):
        return self.color == WHITE
    def walls(self):
        self.color = BLACK
    def isWalls(self):
        return self.color == BLACK
    def draw(self, screen, margin):
        pygame.draw.rect(screen, self.color, (self.x * margin, self.y * margin, margin, margin))
    def getNeighbors(self, grids):
        self.neighbors = []
        if self.x < self.rows - 1 and not grids[self.x + 1][self.y].isWalls():
            self.neighbors.append(grids[self.x + 1][self.y])    # NEIGHBOR AT RIGHT
        if self.x > 0 and not grids[self.x - 1][self.y].isWalls():
            self.neighbors.append(grids[self.x - 1][self.y])    # NEIGHBOR AT LEFT
        if self.y < self.columns - 1 and not grids[self.x][self.y + 1].isWalls():
            self.neighbors.append(grids[self.x][self.y + 1])    # NEIGHBOR AT BOTTOM
        if self.y > 0 and not grids[self.x][self.y - 1].isWalls():
            self.neighbors.append(grids[self.x][self.y - 1])    # NEIGHBOR AT TOP

class MazeGenerator:
    def __init__(self, start, columns, rows, grids, draw):
        self.draw = draw
        self.columns = columns
        self.rows = rows
        self.start = start
        self.visitedGrids = []
        self.grids = grids
        self.stack = []
        # self._dir_one = [                         #in Prims' algorithm
        #     lambda x, y: [x + 1, y],
        #     lambda x, y: [x - 1, y],
        #     lambda x, y: [x, y - 1],
        #     lambda x, y: [x, y + 1]
        # ]
        # self._dir_two = [
        #     lambda x, y: [x + 2, y],
        #     lambda x, y: [x - 2, y],
        #     lambda x, y: [x, y - 2],
        #     lambda x, y: [x, y + 2]
        # ]
        # self._range = list(range(3))

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

        while len(self.stack) > 0:
            each_grid = []
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

            self.draw()


    def out_of_bounds(self, pos):
        return pos[0] < 0 or pos[1] < 0 or pos[0] >= self.rows or pos[1] >= self.columns

def drawGrid(screen, margin, rows, columns):
    for i in range(rows):
        pygame.draw.line(screen, BLACK, (i * margin, 0), (i* margin, width))
        for j in range(columns):
            pygame.draw.line(screen, BLACK, (0, j * margin), (width, j * margin))

def createGrids(columns, rows):
    grids = []
    for x in range(rows):
        grids.append([])
        for y in range(columns):
            each_grid = grid([x, y], rows, columns)
            grids[x].append(each_grid)
    return grids

def getPosByMouse(pos, margin):
    pos[0] = pos[0] // margin
    pos[1] = pos[1] // margin
    return [pos[0], pos[1]]

def draw_update(screen, grids, rows, columns, margin):
    for grid in grids:
        for each_grid in grid:
            each_grid.draw(screen, margin)

    drawGrid(screen, margin, rows, columns)
    pygame.display.update()

start = None
end = None
grids = createGrids(columns,rows)
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if pygame.mouse.get_pressed()[0]:
            x, y = getPosByMouse(list(pygame.mouse.get_pos()), margin)
            new_grid = grids[x][y]
            if not start and not end:
                start = new_grid
                start.startPos()
            elif start and not end:
                end = new_grid
                end.endPos()
                algorithm = a_algorithm.a_pathfinding(start, end, grids, lambda : draw_update(screen, grids, rows, columns, margin))
            elif start and end:
                for grid in grids:
                    for each_grid in grid:
                        each_grid.getNeighbors(grids)

                algorithm.pathfinder()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mazegenerator = MazeGenerator(start, columns, rows, grids, lambda : draw_update(screen, grids, rows, columns, margin))
                for grid in grids:
                    for each_grid in grid:
                        each_grid.getNeighbors(grids)
                mazegenerator.generator()


    draw_update(screen, grids, rows, columns, margin)
