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
        return self.neighbors
    def neighborsPos(self):

def distance_of_grids(pos1, pos2):
    return math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)

def a_pathfinding(start, end, grids):
    openSet = []
    closedSet = []
    start.fCost = start.gCost = start.hCost = 0
    end.fCost = end.gCost = end.hCost = 0
    openList.append(start)
    count = 0
    path = set()
    path.add(start)

    while len(openList) > 0:
        current = openList[count]
        currentIndex = count

        for index, item in enumerate(openList):
            if item.fCost < current.fCost:
                current = itemvnm
                currentIndex = index

        openList.pop(currentIndex)
        closedList.append(current)

        if current == end:
            path
            while current is not None:
                path.append(current.getPos())
                current = current.parent

            return path[::-1]

        for neighbor in current.getNeighbors(grids):
            for closed_neighbor in closedList:
                if neighbor == closed_neighbor:
                    continue

            neighbor.gCost = current.gCost + 1
            neighbor.hCost = distance_of_grids(neighbor.)
            neighbor.fCost = neighbor.gCost + neighbor.hCost

            for openGrids in openList:
                if neighbor == openGrids and neighbor.gCost > openGrids.gCost:
                    continue
            openList.append(neighbor)



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
            elif start and end:
                pass
    draw_update(screen, grids, rows, columns, margin)
