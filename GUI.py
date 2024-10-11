import pygame
from enum import Enum

from Components import Button


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

        # Crear botones usando la clase Button
        self.play_button = Button(200, 300, 'Play', self.font)
        self.exit_button = Button(200, 400, 'Exit', self.font)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.play_button.is_over(mouse_pos):
                        return 'play'  # Iniciar juego
                    elif self.exit_button.is_over(mouse_pos):
                        self.running = False
                        return 'exit'

    def draw(self):
        self.window_manager.fill()
        window = self.window_manager.get_window()

        # Dibuja los botones
        self.play_button.draw(window)
        self.exit_button.draw(window)

        # Actualiza la ventana
        self.window_manager.update()

    def run(self):
        while self.running:
            result = self.handle_events()
            if result == 'play':
                menu_niveles = Levels(self.window_manager)  # Mostrar menú de niveles
                selected_level = menu_niveles.run()  # Ejecuta el menú y retorna el nivel seleccionado
                print(f"Nivel seleccionado: {selected_level}x{selected_level}")
                # Aquí podrías iniciar el juego con el nivel seleccionado
                game = Game(self.window_manager, selected_level)  # Transición a la sección de juego con el nivel seleccionado
                game.run()  # Ejecuta el juego
            elif result == 'exit':
                return 'exit'
            self.draw()
class Levels:
    def __init__(self, window_manager):
        self.window_manager = window_manager
        self.running = True
        self.font = pygame.font.SysFont('Corbel', 35)

        # Crear botones para los niveles
        self.button_5x5 = Button(200, 200, '5x5', self.font)
        self.button_10x10 = Button(200, 300, '10x10', self.font)
        self.button_15x15 = Button(200, 400, '15x15', self.font)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.button_5x5.is_over(mouse_pos):
                        return 5  # Nivel 5x5
                    elif self.button_10x10.is_over(mouse_pos):
                        return 10  # Nivel 10x10
                    elif self.button_15x15.is_over(mouse_pos):
                        return 15  # Nivel 15x15

    def draw(self):
        self.window_manager.fill()
        window = self.window_manager.get_window()

        # Dibuja los botones de nivel
        self.button_5x5.draw(window)
        self.button_10x10.draw(window)
        self.button_15x15.draw(window)

        # Actualiza la ventana
        self.window_manager.update()

    def run(self):
        while self.running:
            result = self.handle_events()
            if result in [5, 10, 15]:
                return result  # Retorna el nivel seleccionado
            self.draw()
