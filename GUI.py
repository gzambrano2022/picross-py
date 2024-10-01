import pygame
from enum import Enum

class SettingsManager(Enum):
    GRID_SIZE = 10
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

class Board:
    def __init__(self, cell_size, grid_size, figure):
        self.cell_size = cell_size
        self.grid_size = grid_size
        self.figure = figure
        self.board = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]
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
        self.window = pygame.display.set_mode((SettingsManager.WIDTH.value, SettingsManager.HEIGHT.value))
        self.clock = pygame.time.Clock()
        self.board = Board(cell_size, grid_size, "hola")
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