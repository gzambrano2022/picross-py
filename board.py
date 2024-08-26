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
                pygame.draw.rect(window, 'black', (space+(720/2), 50+140, 5, 505)) # recta vertical (valores iniciales: space, 50, 5, 505)
                pygame.draw.rect(window, 'black', (50+(720/2), space+140, 500, 5)) # recta horizontal (valores inciales: 50, space, 500, 5)
                space += 50
        elif(self.size == 5):
            window.fill('white')
            space = 60
            for i in range(self.size+1):
                pygame.draw.rect(window, 'black', (space, 10, 5, 500)) # recta vertical
                pygame.draw.rect(window, 'black', (30, space, 500, 5)) # recta horizontal
                space += 60