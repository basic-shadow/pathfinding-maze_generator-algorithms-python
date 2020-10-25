from queue import PriorityQueue
import math

class a_pathfinding:
    def __init__(self, start, end, grids, draw):
        self.openQ = PriorityQueue()
        self.counter = 0
        self.openQ.put((0, self.counter, start))
        self.came_from = {}
        self.draw = draw
        self.start = start
        self.end = end
        self.fCosts = {each_grid: float("inf") for grid in grids for each_grid in grid}
        self.fCosts[start] = self.distance_of_grids(self.start.getPos(), self.end.getPos())
        self.closedSet = set()

    def pathfinder(self):
        while not self.openQ.empty():
            current = self.openQ.get()[2]

            if current == self.end:
                while current in self.came_from:
                    current = self.came_from[current]
                    current.getPath()
                    self.draw()

                self.end.endPos()
                self.start.startPos()
                return True

            for neighbor in current.neighbors:
                for closed_neighbor in self.closedSet:
                    if neighbor == closed_neighbor:
                        neighbor.closeSet()
                        continue

                neighbor.gCost = current.gCost + 1
                neighbor.hCost = self.distance_of_grids(neighbor.getPos(), self.end.getPos())
                neighbor.fCost = neighbor.gCost + neighbor.hCost
                if neighbor.fCost < self.fCosts[neighbor]:
                    self.came_from[neighbor] = current
                    self.fCosts[neighbor] = neighbor.fCost
                    if neighbor not in self.closedSet:
                        self.counter += 1
                        self.openQ.put((self.fCosts[neighbor], self.counter, neighbor))
                        self.closedSet.add(neighbor)

            self.draw()

        return False

    def distance_of_grids(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x2 - x1) + abs(y2 - y1)
