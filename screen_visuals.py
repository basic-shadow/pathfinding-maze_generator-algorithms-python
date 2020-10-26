import pygame
import sys
import a_star_pathfinding_algorithm as a_star_algorithm
import recursive_backtracking_maze_generator as recursive_maze
import prims_algorithm_maze_generator as prims_maze

pygame.init()
pygame.display.set_caption("basic_shadow_______________________________isla")


RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
BLACK = (0,0,0)
WHITE = (200,200,200)
BLACK_L = (1, 1, 1)
GREEN = (0, 128, 0)
ORANGE = (255,140,0)
PURPLE = (150, 0, 210)
GREY = (60, 60, 60)

finish = False
width = 800
rows = 20
columns = 20
if rows < columns:
    margin = width // rows
else:
    margin = width // columns

screen = pygame.display.set_mode((800, 800))

class grid():
    def __init__(self, pos,rows,columns, color = BLACK_L):
        self.x, self.y = pos
        self.color = color
        self.neighbors = []
        self.rows = rows
        self.columns = columns
        self.gCost = 0
        self.hCost = 0
        self.fCost = 0
    def current(self):
        self.color = RED
    def closeSet(self):
        self.color = YELLOW
    def startPos(self):
        self.color = PURPLE
    def endPos(self):
        self.color = BLUE
    def getPath(self):
        self.color = RED
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
    def neighbor(self):
        self.color = BLACK_L
    def isNeighbor(self):
        return self.color == BLACK_L
    def isRemaining(self):
        return self.color == BLACK_L
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

def drawGrid(screen, margin, rows, columns):
    for i in range(rows):
        pygame.draw.line(screen, GREY, (i * margin, 0), (i* margin, width))
        for j in range(columns):
            pygame.draw.line(screen, GREY, (0, j * margin), (width, j * margin))

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
            elif start and end:
                for grid in grids:
                    for each_grid in grid:
                        each_grid.getNeighbors(grids)

                algorithm = a_star_algorithm.a_pathfinding(start, end, grids, lambda : draw_update(screen, grids, rows, columns, margin))
                algorithm.pathfinder()
        if pygame.mouse.get_pressed()[2]:
            x, y = getPosByMouse(list(pygame.mouse.get_pos()), margin)
            new_grid = grids[x][y]
            if start and not end:
                end = new_grid
                end.endPos()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                maze_generator = recursive_maze.MazeGenerator(columns, rows, grids, lambda : draw_update(screen, grids, rows, columns, margin))
                maze_generator.generator()
            if event.key == pygame.K_c:
                maze_generator = prims_maze.MazeGenerator(columns, rows, grids, lambda : draw_update(screen, grids, rows, columns, margin))
                maze_generator.generator()

    draw_update(screen, grids, rows, columns, margin)
