import pygame

class Board:
    def __init__(self, size, figure):
        self.size = size
        self.figure = figure

    def drawPuzzle(self, window):
        window.fill('white')
        space = 50
        for i in range(self.size):
            pygame.draw.rect(window, 'black', (space, 10, 5, 500))
            pygame.draw.rect(window, 'black', (30, space, 500, 5))
            space += 50