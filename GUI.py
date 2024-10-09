import pygame
import random
import numpy as np
from enum import Enum

class SettingsManager(Enum):
    GRID_SIZE = 5
    CELL_SIZE = 50
    WIDTH = 800
    HEIGHT = 600
    DEFAULT_COLOR = (255, 255, 255)
    CLICKED_COLOR = (0, 0, 0)
    BACKGROUND_COLOR = 'gray'

class Cell:
    def __init__(self):
        self.clicked = False

    def click(self):
        self.clicked = not self.clicked

    def get_color(self):
        return SettingsManager.CLICKED_COLOR.value if self.clicked else SettingsManager.DEFAULT_COLOR.value

class LogicalBoard:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.board_l = np.zeros((grid_size, grid_size))

    def fill_board(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                num = random.randint(0,1)
                self.board_l[i][j] = num

    def find_numbers_r(self):
        rarray = []

        # contabilizar cuántos '1's hay en cada fila
        for i in range(self.grid_size):
            cont  = 0
            array = []
            for j in range(self.grid_size):
                if self.board_l[i][j] == 1:
                    cont += 1
                else:
                    if cont>0:
                        array.append(cont)
                        cont = 0
                if j == self.grid_size-1 and cont>0:
                    array.append(cont)
            if len(array)==0:
                array.append(0)

            rarray.append(array)

        return rarray

    def find_numbers_c(self):
        carray = []

        # contabilizar cuántos '1's hay en cada columna
        for i in range(self.grid_size):
            cont = 0
            array = []
            for j in range(self.grid_size):
                if self.board_l[j][i] == 1:
                    cont += 1
                else:
                    if cont > 0:
                        array.append(cont)
                        cont = 0
                if j == self.grid_size - 1 and cont > 0:
                    array.append(cont)
            if len(array)==0:
                array.append(0)

            carray.append(array)

        return carray


class Board:
    def __init__(self, cell_size, grid_size, figure, logicalboard):
        self.font = pygame.font.Font(None, 36)
        self.cell_size = cell_size
        self.grid_size = grid_size
        self.figure = figure
        self.board = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]
        self.board2 = logicalboard.fill_board()
        self.rarray = logicalboard.find_numbers_r()
        self.carray = logicalboard.find_numbers_c()
        self.offset_x = (SettingsManager.WIDTH.value - self.grid_size * self.cell_size) // 2
        self.offset_y = (SettingsManager.HEIGHT.value - self.grid_size * self.cell_size) // 2

    def draw(self, surface):
        for row, rowOfCells in enumerate(self.board):
            for col, cell in enumerate(rowOfCells):
                color = cell.get_color()
                pygame.draw.rect(surface, color, (
                    self.offset_x + col * self.cell_size,  # Coordenada x ajustada
                    self.offset_y + row * self.cell_size,  # Coordenada y ajustada
                    self.cell_size - 2, self.cell_size - 2))  # Tamaño de la celda con un borde pequeño
                # print(self.offset_x + col * self.cell_size)
                # print(self.offset_y + row * self.cell_size)
                # print(self.cell_size - 2, self.cell_size - 2)

        for i, numbers in enumerate(self.rarray):
            text = "  ".join(map(str, numbers))
            row_number_surface = self.font.render(text, True, (255, 0, 255))
            surface.blit(row_number_surface, (
                self.offset_x - 80,
                self.offset_y + i * self.cell_size + self.cell_size // 2 - 10
            ))

        for i, numbers in enumerate(self.carray):
            for j,number in enumerate(numbers):
                text = str(number)
                col_number_surface = self.font.render(text, True, (255, 0, 255))
                surface.blit(col_number_surface, (
                    self.offset_x +i * self.cell_size + self.cell_size // 2 - 10,
                    self.offset_y - 30 - (len(numbers) - j) * (self.font.get_height()+5)
                ))

    def handle_click(self, pos): # pos son coordenadas (x,y) en pygame
        row = (pos[1]-self.offset_y) // self.cell_size
        print(f"pos[1] // self.cell_size = {row}")
        col = (pos[0]-self.offset_x) // self.cell_size
        print(f"pos[0] // self.cell_size = {col}")
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            self.board[row][col].click()



class Game:
    def __init__(self, grid_size=SettingsManager.GRID_SIZE.value, cell_size=SettingsManager.CELL_SIZE.value):
        pygame.init()
        # self.window_size = grid_size * cell_size
        font = pygame.font.Font(None, 36)
        self.window = pygame.display.set_mode((SettingsManager.WIDTH.value, SettingsManager.HEIGHT.value))
        self.clock = pygame.time.Clock()
        self.board = Board(cell_size, grid_size, "hola", logicalboard=LogicalBoard(grid_size))
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.board.handle_click(event.pos)
                print(event.pos)

    def run(self):
        while self.running:
            self.clock.tick(120)
            self.handle_events()
            self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
            self.board.draw(self.window)
            pygame.display.flip()
        pygame.quit()