import pygame
import sys
from queue import PriorityQueue
import math

pygame.init()

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (180, 180, 180)
GREEN = (255, 0, 255)
ORANGE = (255,140,0)

finish = False
width = 800
rows = 10
columns = 10
margin = width // rows

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
        self.color = BLACK
    def openSet(self):
        self.color = YELLOW
    def startPos(self):
        self.color = GREEN
    def endPos(self):
        self.color = BLUE
    def getPath(self):
        self.color = RED
    def getPos(self):
        return [self.x, self.y]
    def draw(self, screen, margin):
        pygame.draw.rect(screen, self.color, (self.x * margin, self.y * margin, margin, margin))
    def getNeighbors(self, grids):
        self.neighbors = []
        if self.x < self.rows - 1:
            self.neighbors.append(grids[self.x + 1][self.y])    # NEIGHBOR AT RIGHT
        if self.x > 0:
            self.neighbors.append(grids[self.x - 1][self.y])    # NEIGHBOR AT LEFT
        if self.y < self.columns - 1:
            self.neighbors.append(grids[self.x][self.y + 1])    # NEIGHBOR AT BOTTOM
        if self.y > 0:
            self.neighbors.append(grids[self.x][self.y - 1])    # NEIGHBOR AT TOP
    def neighborsPos(self):
        pass



class a_pathfinding:
    def __init__(self, start, end, grids, draw):
        self.openQ = PriorityQueue()
        self.counter = 0
        self.closedSet = set()
        self.openQ.put((0, self.counter, start))
        self.all_path = {start}
        self.draw = draw
        self.start = start
        self.end = end
        # self.gCosts = {each_grid: float("inf") for grid in grids for each_grid in grid}
        # self.gCosts[start] = 0
        self.fCosts = {each_grid: float("inf") for grid in grids for each_grid in grid}
        self.fCosts[start] = self.distance_of_grids(self.start.getPos(), self.end.getPos())

    def pathfinder(self):
        while not self.openQ.empty():
            current = self.openQ.get()[2]
            currentIndex = 0
            self.all_path.add(current)
            self.closedSet.add(current)

            if current == self.end:
                while current in self.all_path:
                    current.getPath()
                    self.draw()

            for neighbor in current.neighbors:
                for closed_neighbor in self.closedSet:
                    if neighbor == closed_neighbor:
                        neighbor.closeSet()
                        continue

                neighbor.gCost = current.gCost + 1
                neighbor.hCost = self.distance_of_grids(neighbor.getPos(), self.end.getPos())
                neighbor.fCost = neighbor.gCost + neighbor.hCost
                if neighbor.fCost < self.fCosts[neighbor]:
                    self.all_path.add(neighbor)
                    self.fCosts[neighbor] = neighbor.fCost
                    # self.gCosts[neighbor] = neighbor.gCost
                    self.counter += 1
                    self.openQ.put((neighbor.fCost, self.counter, neighbor))
                    neighbor.openSet()
                    self.closedSet.add(neighbor)

            self.draw()
            if current != self.start:
                current.closeSet()

    def distance_of_grids(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x2 - x1) + abs(y2 - y1)

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
print(grids[1][2])
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
                algorithm = a_pathfinding(start, end, grids, lambda : draw_update(screen, grids, rows, columns, margin))
            elif start and end:
                for grid in grids:
                    for each_grid in grid:
                        each_grid.getNeighbors(grids)
                algorithm.pathfinder()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                start = None
                end = None
                grid = make_grid(ROWS, width)
    draw_update(screen, grids, rows, columns, margin)
