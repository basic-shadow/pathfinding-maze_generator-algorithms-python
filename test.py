import pygame
import sys


pygame.init()

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
BACKGROUND_COLOR = (0,0,0)
GREY = (180, 180, 180)

finish = False
width = 900
rows = 30
margin = width // rows

screen = pygame.display.set_mode((width, width))

class drawGrid():
    def __init__(self, screen, rows, color = YELLOW):
        x = 0
        y = 0
        self.color = color
        for l in range(rows):
            x = x + margin
            y = y + margin
            pygame.draw.line(screen, (255,255,255), (x,0),(x,width))
            pygame.draw.line(screen, (255,255,255), (0,y),(width,y))

    def draw(self, pos):
        pos[0] = pos[0] // margin * margin
        pos[1] = pos[1] // margin * margin

        pygame.draw.rect(screen, self.color, (pos[0], pos[1], rows, rows))

grid = drawGrid(screen, rows)

while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
            grid.draw(list(pygame.mouse.get_pos()))


    # screen.fill(BACKGROUND_COLOR)
    pygame.display.update()
