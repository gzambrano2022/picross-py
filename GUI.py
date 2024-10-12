import pygame
from abc import ABC, abstractmethod
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
    def __init__(self, frame_manager, grid_size=SettingsManager.GRID_SIZE.value,
                 cell_size=SettingsManager.CELL_SIZE.value):
        super().__init__(frame_manager)
        self.clock = pygame.time.Clock()
        self.board = Board(cell_size, grid_size, "hola")  # Usa el tamaño del grid recibido
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