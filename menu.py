import pygame
import numpy as np
from board import *

def run():

    pygame.init()
    window = pygame.display.set_mode((1280, 720))
    x = 300
    y = 150
    tablero = Board(10, 'perro')
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                tablero.drawPuzzle(window)
                print("Tecla pulsada")

        pygame.display.update()

