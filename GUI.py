import pygame
from enum import Enum


class SettingsManager(Enum):
    GRID_SIZE = 10
    CELL_SIZE = 50
    WIDTH = 1280
    HEIGHT = 720
    DEFAULT_COLOR = (255, 255, 255)  # blanco
    CLICKED_COLOR = (0, 0, 0)  # negro
    MARKED_COLOR = (255, 0, 0)  # Rojo
    BACKGROUND_COLOR = 'gray'


class WindowManager:
    def __init__(self, width, height, background_color):
        # Inicializa pygame y crea la ventana
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        self.background_color = background_color

    def fill(self):
        # Llena la ventana con el color de fondo
        self.window.fill(self.background_color)

    def update(self):
        # Actualiza la ventana
        pygame.display.flip()

    def get_window(self):
        return self.window


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

    def handle_click(self, pos, num_click):  # pos son coordenadas (x,y) en pygame. num_click: 1 right, 2 left
        if num_click == 1:
            row = (pos[1] - self.offset_y) // self.cell_size
            col = (pos[0] - self.offset_x) // self.cell_size
            if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
                self.board[row][col].click()
        elif num_click == 2:
            row = (pos[1] - self.offset_y) // self.cell_size
            col = (pos[0] - self.offset_x) // self.cell_size
            if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
                self.board[row][col].mark()


class Game:
    def __init__(self, window_manager, grid_size=SettingsManager.GRID_SIZE.value,
                 cell_size=SettingsManager.CELL_SIZE.value):
        pygame.init()
        self.window = window_manager
        self.clock = pygame.time.Clock()
        self.board = Board(cell_size, grid_size, "hola")
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.board.handle_click(event.pos, 1)
                elif event.button == 3:
                    self.board.handle_click(event.pos, 2)

    def run(self):
        while self.running:
            self.clock.tick(120)
            self.handle_events()
            self.window.fill()
            self.board.draw(self.window.get_window())
            self.window.update()
        pygame.quit()


class Menu:
    def __init__(self, window_manager):
        self.window_manager = window_manager
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
                        return 'play'  # Elige iniciar el juego
                    elif self.is_over_button(mouse_pos, 200, 400):
                        self.running = False
                        return 'exit'

    def is_over_button(self, pos, x, y, w=140, h=40):
        return x <= pos[0] <= x + w and y <= pos[1] <= y + h

    def draw(self):
        self.window_manager.fill()
        window = self.window_manager.get_window()

        # Dibuja los botones
        pygame.draw.rect(window, (100, 100, 100), [200, 300, 140, 40])
        pygame.draw.rect(window, (100, 100, 100), [200, 400, 140, 40])

        # Coloca el texto sobre los botones
        window.blit(self.play_button, (220, 305))
        window.blit(self.exit_button, (220, 405))

        # Actualiza la ventana
        self.window_manager.update()

    def run(self):
        while self.running:
            result = self.handle_events()
            if result == 'play':
                game = Game(self.window_manager)  # Transición dentro de la clase
                game.run()  # Esto transfiere el control al juego, pero la clase `Menu` queda encargada de hacer esto.
                # return 'play'  # Transición al juego
            elif result == 'exit':
                return 'exit'
            self.draw()
