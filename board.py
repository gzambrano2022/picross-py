import pygame

class Board:
    def __init__(self, size, figure):
        self.size = size
        self.figure = figure

    def drawPuzzle(self, window):

        if(self.size != 10 and self.size != 5): # disposiciones de tablero admitidas por ahora
            return

        elif(self.size == 10):
            window.fill('white')
            space = 50
            for i in range(self.size+1):
                pygame.draw.rect(window, 'black', (space, 10, 5, 540))
                pygame.draw.rect(window, 'black', (50, space, 540, 5))
                space += 50
        elif(self.size == 5+1):
            window.fill('white')
            space = 60
            for i in range(self.size):
                pygame.draw.rect(window, 'black', (space, 10, 5, 500))
                pygame.draw.rect(window, 'black', (30, space, 500, 5))
                space += 60