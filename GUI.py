import pygame
from enum import Enum

class SettingsManager(Enum):
    GRID_SIZE = 10
    CELL_SIZE = 50
    WIDTH = 1280
    HEIGHT = 720
    DEFAULT_COLOR = (255, 255, 255) #blanco
    CLICKED_COLOR = (0, 0, 0) #negro
    MARKED_COLOR = (255, 0, 0) #Rojo
    BACKGROUND_COLOR = 'gray'

class Cell:
    def __init__(self):
        self.clicked = False
        self.marked = False
    def click(self):
        self.clicked = not self.clicked
    def mark(self):
        self.marked = not self.marked
    def get_color(self):
        if self.clicked:
            return SettingsManager.CLICKED_COLOR.value
        elif self.marked:
            return SettingsManager.MARKED_COLOR.value
        else:
            return SettingsManager.DEFAULT_COLOR.value

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
                
    def handle_click(self, pos, num_click): # pos son coordenadas (x,y) en pygame. num_click: 1 right, 2 left
        if num_click == 1:
            row = (pos[1]-self.offset_y) // self.cell_size
            col = (pos[0]-self.offset_x) // self.cell_size
            if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
                self.board[row][col].click()
        elif num_click == 2:
            row = (pos[1]-self.offset_y) // self.cell_size
            col = (pos[0]-self.offset_x) // self.cell_size
            if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
                self.board[row][col].mark()


class Game:
    def __init__(self, grid_size=SettingsManager.GRID_SIZE.value, cell_size=SettingsManager.CELL_SIZE.value):
        pygame.init()
        self.window = pygame.display.set_mode((SettingsManager.WIDTH.value, SettingsManager.HEIGHT.value))
        self.clock = pygame.time.Clock()
        self.board = Board(cell_size, grid_size, "hola")
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.board.handle_click(event.pos,1)
                elif event.button == 3:
                    self.board.handle_click(event.pos, 2)

    def run(self):
        while self.running:
            self.clock.tick(120)
            self.handle_events()
            self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
            self.board.draw(self.window)
            pygame.display.flip()
        pygame.quit()


class Menu:
    def __init__(self):
        self.window = pygame.display.set_mode((SettingsManager.WIDTH.value, SettingsManager.HEIGHT.value))

        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont('Corbel', 35)
        self.play_button = self.font.render('Play', True, (255, 255, 255))
        self.exit_button = self.font.render('Exit', True, (255, 255, 255))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.is_over_button(mouse_pos, 200, 300):
                        return 'play'  # Este será el indicador para el botón de "Play"
                    elif self.is_over_button(mouse_pos, 200, 400):
                        self.running = False
                        return 'exit'

    def is_over_button(self, pos, x, y, w=140, h=40):
        return x <= pos[0] <= x + w and y <= pos[1] <= y + h

    def draw(self):
        self.window.fill(SettingsManager.BACKGROUND_COLOR.value)  # Rellenar el fondo
        # Dibuja los botones
        pygame.draw.rect(self.window, (100, 100, 100), [200, 300, 140, 40])  # Botón Play
        pygame.draw.rect(self.window, (100, 100, 100), [200, 400, 140, 40])  # Botón Exit

        # Coloca el texto sobre los botones
        self.window.blit(self.play_button, (220, 305))
        self.window.blit(self.exit_button, (220, 405))

        # Actualiza la pantalla
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(120)
            result = self.handle_events()  # Maneja los eventos
            self.draw()  # Dibuja el menú
            if result == 'play':
                return 'play'  # Este sería el resultado para indicar "Play"
            elif result == 'exit':
                return 'exit'  # Este sería el resultado para indicar "Exit"

