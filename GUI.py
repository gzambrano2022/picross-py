import pygame
from abc import ABC, abstractmethod
from enum import Enum
import numpy as np
import random
from pygame.examples.moveit import WIDTH, HEIGHT
from Components import Button


class SettingsManager(Enum):
    GRID_SIZE = 10
    CELL_SIZE = 20
    WIDTH = 1280
    HEIGHT = 750
    DEFAULT_COLOR = (255, 255, 255)  # blanco
    CLICKED_COLOR = (0, 0, 0)  # negro
    MARKED_COLOR = (255, 0, 0)  # Rojo
    BACKGROUND_COLOR = 'gray'

class Scene(ABC):
    def __init__(self, frame_manager):
        self.frame_manager = frame_manager
        self.running = True
        self.font = pygame.font.SysFont('Corbel', 35)

    @abstractmethod
    def handle_events(self):
        """Method para manejar eventos, implementado por las subclases"""
        pass

    @abstractmethod
    def draw(self):
        """Method para dibujar en la pantalla, implementado por las subclases"""
        pass

    def run(self):
        """Ciclo principal de ejecución de la escena"""
        while self.running:
            self.handle_events()
            self.draw()

# Instancia de ejecucion del tablero del nonograma
class Game(Scene):
    def __init__(self, frame_manager, grid_size=SettingsManager.GRID_SIZE.value):
        super().__init__(frame_manager)
        self.clock = pygame.time.Clock()

        cell_size = min(
            SettingsManager.WIDTH.value // grid_size,
            SettingsManager.HEIGHT.value // grid_size
        )

        logical_board = LogicalBoard(grid_size)
        logical_board.fill_board()

        self.board = Board(grid_size,WIDTH,HEIGHT,logical_board)  # Usa el tamaño del grid recibido
        self.backButton = Button(50, 600, 'Back', self.font)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.frame_manager.current_scene = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.backButton.is_over(mouse_pos):
                        self.frame_manager.switch_to(
                            Levels(self.frame_manager))  # Cambia a ventana al menu de niveles
                        self.running = False
                    else:
                        # Aquí manejamos el clic izquierdo en el tablero
                        self.board.handle_click(event.pos, 1)  # Pasamos el clic izquierdo (1) a board
                elif event.button == 3:
                    self.board.handle_click(event.pos, 2)

    def draw(self):
        self.frame_manager.screen.fill((30, 30, 60))  # Fondo azul oscuro
        self.board.draw(self.frame_manager.screen)
        self.backButton.draw(self.frame_manager.screen)
        pygame.display.flip()

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

# Seleccion de niveles
class Levels(Scene):
    def __init__(self, frame_manager):
        # Crear botones para los niveles
        super().__init__(frame_manager)
        self.button_5x5 = Button(200, 200, '5x5', self.font)
        self.button_10x10 = Button(200, 300, '10x10', self.font)
        self.button_15x15 = Button(200, 400, '15x15', self.font)
        self.backButton = Button(50, 600, 'Back', self.font)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.frame_manager.current_scene = None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.backButton.is_over(mouse_pos):
                        self.frame_manager.switch_to(Menu(self.frame_manager))  # Cambia a ventana Menu
                        self.running = False  # Detenemos la ventana
                    elif self.button_5x5.is_over(mouse_pos):
                        self.frame_manager.switch_to(Game(self.frame_manager, grid_size=5))  # 5x5 grid
                        self.running = False
                    elif self.button_10x10.is_over(mouse_pos):
                        self.frame_manager.switch_to(Game(self.frame_manager, grid_size=10))  # 10x10 grid
                        self.running = False
                    elif self.button_15x15.is_over(mouse_pos):
                        self.frame_manager.switch_to(Game(self.frame_manager, grid_size=15))  # 15x15 grid
                        self.running = False

    def draw(self):
        self.frame_manager.screen.fill((30, 30, 60))  # Fondo azul oscuro
        # Dibuja los botones de nivel
        self.button_5x5.draw(self.frame_manager.screen)
        self.button_10x10.draw(self.frame_manager.screen)
        self.button_15x15.draw(self.frame_manager.screen)
        self.backButton.draw(self.frame_manager.screen)
        # Actualiza la ventana
        pygame.display.flip()

# Menú Principal
class Menu(Scene):
    def __init__(self, frame_manager):
        super().__init__(frame_manager)
        # Crear botones usando la clase Button
        self.play_button = Button(200, 300, 'Play', self.font)
        self.exit_button = Button(200, 400, 'Exit', self.font)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.frame_manager.current_scene = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.play_button.is_over(mouse_pos):
                        self.frame_manager.switch_to(Levels(self.frame_manager))  # Cambia a ventana Selector de niveles
                        self.running = False  # Detenemos la ventana
                    elif self.exit_button.is_over(mouse_pos):
                        self.running = False
                        self.frame_manager.current_scene = None  # Para cerrar el programa

    def draw(self):
        self.frame_manager.screen.fill((60, 60, 60))
        # Dibuja los botones
        self.play_button.draw(self.frame_manager.screen)
        self.exit_button.draw(self.frame_manager.screen)
        pygame.display.flip()
        # Actualiza la ventana
        # self.window_manager.update()

class FrameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SettingsManager.WIDTH.value, SettingsManager.HEIGHT.value))
        self.current_scene = None

    def switch_to(self, new_window):
        self.current_scene = new_window

    def run(self):
        while self.current_scene is not None:
            self.current_scene.run()

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
    def __init__(self, grid_size, frame_width, frame_height, logicalboard):
        self.cell_size = min(frame_width // grid_size, frame_height // grid_size)
        self.grid_size = grid_size
        self.logical_board = logicalboard
        self.board = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]
        self.offset_x = (SettingsManager.WIDTH.value - self.grid_size * self.cell_size) // 2
        self.offset_y = (SettingsManager.HEIGHT.value - self.grid_size * self.cell_size) // 2 + 75

        self.rarray = self.logical_board.find_numbers_r()
        self.carray = self.logical_board.find_numbers_c()

        self.font = pygame.font.SysFont(None, 36)

    def draw(self, surface):
        for row, rowOfCells in enumerate(self.board):
            for col, cell in enumerate(rowOfCells):
                color = cell.get_color()
                pygame.draw.rect(surface, color, (
                    self.offset_x + col * self.cell_size,  # Coordenada x ajustada
                    self.offset_y + row * self.cell_size,  # Coordenada y ajustada
                    self.cell_size - 2, self.cell_size - 2))  # Tamaño de la celda con un borde pequeño

        for i,numbers in enumerate(self.rarray):
            text = "  ".join(map(str, numbers))
            row_number_surface = self.font.render(text, True, (255,0,255))
            surface.blit(row_number_surface, (
                self.offset_x + i - 180,
                self.offset_y + i * self.cell_size + self.cell_size // 2 - 10,
            ))

        for i,numbers in enumerate(self.carray):
            for j, number in enumerate(numbers):
                text = str(number)
                col_number_surface = self.font.render(text, True, (255,0,255))
                surface.blit(col_number_surface, (
                    self.offset_x + i * self.cell_size + self.cell_size // 2 - 10,
                    self.offset_y - 30 - (len(numbers) - j) * (self.font.get_height() + 5)
                ))

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