import os
import pygame
from abc import ABC, abstractmethod
from enum import Enum
import pickle
import numpy as np
import random
from pygame.examples.moveit import WIDTH, HEIGHT
from Components import Button, Title, Slider

# Inicializa Pygame y su mixer
#pygame.init()
pygame.mixer.init()

# Reproduce música de fondo al inicio
pygame.mixer.music.load("sounds/backgroundSong1.mp3")  # Ruta de tu música
pygame.mixer.music.play(-1)  # -1 Para que la música se reproduzca en loop



class SettingsManager(Enum):
    GRID_SIZE = 10
    CELL_SIZE = 20
    WIDTH = 1280
    HEIGHT = 720
    DEFAULT_COLOR = (255, 255, 255)  # blanco
    CLICKED_COLOR = (0, 0, 0)  # negro
    MARKED_COLOR = (255, 0, 0)  # Rojo
    NUMBERS_COLOR = (250, 250, 114) # Amarillo claro
    BACKGROUND_COLOR = (25, 25, 35) # Gris Azulado




class Scene(ABC):
    def __init__(self, frame_manager):
        self.frame_manager = frame_manager
        self.running = True
        self.font = pygame.font.Font('fonts/monogram.ttf', 35)

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
    def __init__(self, frame_manager, grid_size=SettingsManager.GRID_SIZE.value, solution=None):
        super().__init__(frame_manager)
        self.clock = pygame.time.Clock()

        cell_size = min(
            SettingsManager.WIDTH.value // grid_size,
            SettingsManager.HEIGHT.value // grid_size
        )

        if solution is not None:
            logical_board = LogicalBoard(grid_size,solution)  # Crear una instancia de LogicalBoard
        else:
            logical_board = LogicalBoard(np.zeros((grid_size, grid_size)))  # o alguna lógica para inicializar

        self.board = Board(grid_size,WIDTH,HEIGHT,logical_board)  # Usa el tamaño del grid recibido
        self.backButton = Button(50, 600, 'Back', self.font)
        self.saveButton = Button(50, 550, 'Save', self.font)

    def handle_events(self):
        for event in pygame.event.get():

            # Manejar eventos para los botones
            self.saveButton.handle_event(event)
            self.backButton.handle_event(event)

            if event.type == pygame.QUIT:
                self.running = False
                self.frame_manager.current_scene = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.backButton.is_over(mouse_pos):
                        self.frame_manager.switch_to(
                            Levels(self.frame_manager))  # Cambia a ventana al menu de niveles
                        self.running = False
                    elif self.saveButton.is_over(mouse_pos):
                        filename = 'saved_board'
                        if self.board.guardar(filename):
                            print("Tablero guardado correctamente.")
                        else:
                            print("Error al guardar el tablero.")
                    else:
                        # Aquí manejamos el clic izquierdo en el tablero
                        self.board.handle_click(event.pos, 1)  # Pasamos el clic izquierdo (1) a board
                elif event.button == 3:
                    self.board.handle_click(event.pos, 2)

    def draw(self):
        self.frame_manager.screen.fill(SettingsManager.BACKGROUND_COLOR.value)  # Fondo morado oscuro
        self.board.draw(self.frame_manager.screen)
        self.backButton.draw(self.frame_manager.screen)
        self.saveButton.draw(self.frame_manager.screen)
        pygame.display.flip()

class LogicalBoard:
    def __init__(self, grid_size,solution=None):
        self.grid_size = grid_size

        if solution is not None:
            self.board_l = np.array(solution)
        else:
            self.board_l = np.zeros((grid_size,grid_size))

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
        self.button_5x5 = Button(185, 200, '5x5', self.font)
        self.button_10x10 = Button(565, 200, '10x10', self.font)
        self.button_15x15 = Button(935, 200, '15x15', self.font)
        self.backButton = Button(50, 600, 'Back', self.font)

        # Crear imagenes referencia
        pry_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_imagen1 = os.path.join(pry_dir, 'imagenes gui', 'tam1.png')
        ruta_imagen2 = os.path.join(pry_dir, 'imagenes gui', 'tam2.png')
        ruta_imagen3 = os.path.join(pry_dir, 'imagenes gui', 'tam3.png')
        self.imagen1 = pygame.image.load(ruta_imagen1)
        self.imagen2 = pygame.image.load(ruta_imagen2)
        self.imagen3 = pygame.image.load(ruta_imagen3)
        self.imagen1 = pygame.transform.scale(self.imagen1, (216, 220))
        self.imagen2 = pygame.transform.scale(self.imagen2, (216, 220))
        self.imagen3 = pygame.transform.scale(self.imagen3, (216, 220))

        # Crear el texto del título
        self.SubTitle = Title(SettingsManager.WIDTH.value, SettingsManager.HEIGHT.value, "LEVELS", "fonts/ka1.ttf")

    def handle_events(self):
        for event in pygame.event.get():

            # Manejar eventos para los botones
            self.button_5x5.handle_event(event)
            self.button_10x10.handle_event(event)
            self.button_15x15.handle_event(event)
            self.backButton.handle_event(event)

            if event.type == pygame.QUIT:
                self.running = False
                self.frame_manager.current_scene = None


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.backButton.is_over(mouse_pos):
                        self.frame_manager.switch_to(Menu(self.frame_manager))  # Cambia a ventana Menu
                        self.running = False  # Detenemos la ventana
                    elif self.button_5x5.is_over(mouse_pos):
                        self.frame_manager.switch_to(Nonos(self.frame_manager,grid_size=5))  # nonogramas de tam 5x5
                        self.running = False
                    elif self.button_10x10.is_over(mouse_pos):
                        self.frame_manager.switch_to(Nonos(self.frame_manager,grid_size=10))  # nonogramas de tam 10x10
                        self.running = False
                    elif self.button_15x15.is_over(mouse_pos):
                        self.frame_manager.switch_to(Nonos(self.frame_manager,grid_size=15))  # nonogramas de tam 15x15
                        self.running = False

    def draw(self):
        self.frame_manager.screen.fill(SettingsManager.BACKGROUND_COLOR.value)  # Fondo morado oscuro
        # Dibuja los botones de nivel
        self.button_5x5.draw(self.frame_manager.screen)
        self.button_10x10.draw(self.frame_manager.screen)
        self.button_15x15.draw(self.frame_manager.screen)
        self.backButton.draw(self.frame_manager.screen)
        self.SubTitle.draw(self.frame_manager.screen)

        # Dibuja título
        #self.frame_manager.screen.blit(self.title, (80,50))

        #  Dibuja imagenes
        self.frame_manager.screen.blit(self.imagen1, (150, 300))
        self.frame_manager.screen.blit(self.imagen2, (530, 300))
        self.frame_manager.screen.blit(self.imagen3, (900, 300))

        # Actualiza la ventana
        pygame.display.flip()

# Menú Principal
class Menu(Scene):
    def __init__(self, frame_manager, ):
        super().__init__(frame_manager)
        # Crear botones usando la clase Button
        self.mainTitle = Title(SettingsManager.WIDTH.value, SettingsManager.HEIGHT.value + 1000, "PYCROSS",
                               "fonts/Cube.ttf", 50)
        self.play_button = Button(200, 400, 'Play', self.font)
        self.exit_button = Button(200, 600, 'Exit', self.font)
        self.option_button = Button(200, 500, 'Option', self.font)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.frame_manager.current_scene = None

            # Manejar eventos para los botones
            self.play_button.handle_event(event)
            self.exit_button.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Verifica si se hace clic con el botón izquierdo del mouse
                    mouse_pos = pygame.mouse.get_pos()
                    if self.play_button.is_over(mouse_pos):
                        self.frame_manager.switch_to(
                            Levels(self.frame_manager))  # Cambia a la ventana del selector de niveles
                        self.running = False  # Detenemos la ventana
                    elif self.option_button.is_over(mouse_pos):
                        self.frame_manager.switch_to(
                            Options(self.frame_manager))  # Cambia a la ventana del selector de niveles
                        self.running = False  # Detenemos la ventana
                    elif self.exit_button.is_over(mouse_pos):
                        self.running = False
                        self.frame_manager.current_scene = None  # Cierra el programa

    def draw(self):
        
        self.frame_manager.screen.fill(SettingsManager.BACKGROUND_COLOR.value)


        # Dibuja los elementos en la pantalla
        self.mainTitle.draw(self.frame_manager.screen)
        self.play_button.draw(self.frame_manager.screen)
        self.exit_button.draw(self.frame_manager.screen)
        self.option_button.draw(self.frame_manager.screen)
        pygame.display.flip()  # Actualiza la ventana

class Nonos(Scene):
    def __init__(self, frame_manager, grid_size=SettingsManager.GRID_SIZE.value, ):
        super().__init__(frame_manager)
        self.grid_size = grid_size
        self.button_custom = Button(650, 80, 'Personalizado', self.font,width=200,height=60)
        self.backButton = Button(50, 600, 'Back', self.font)
        self.buttons = []

        # Crear botones de cada nonograma solución dentro de la carpeta solutions
        folder_path = os.path.join('solutions',f's_{grid_size}x{grid_size}')
        solutions_files = [file for file in os.listdir(folder_path) if file.endswith('.pkl')]
        self.solutions_files = [os.path.join(folder_path, file) for file in solutions_files]
        for i,file in enumerate(solutions_files):
            button = Button(650, 120+(i+1)*90, f'{i+1}',self.font,width=200, height=60)
            self.buttons.append(button)

    def IniciarNono(self,number):
        if 0 <= number < len(self.solutions_files):
            file_path = self.solutions_files[number]
            with open(file_path, 'rb') as f:
                solution = pickle.load(f)
            return solution
        else:
            print("No se enocntró archivo.")

    def handle_events(self):
        for event in pygame.event.get():
            # Manejar eventos para los botones
            for button in self.buttons:
                button.handle_event(event)
            self.button_custom.handle_event(event)
            self.backButton.handle_event(event)

            if event.type == pygame.QUIT:
                self.running = False
                self.frame_manager.current_scene = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.backButton.is_over(mouse_pos):
                        self.frame_manager.switch_to(Levels(self.frame_manager)) # Cambia a ventana Levels
                        self.running = False
                    elif self.button_custom.is_over(mouse_pos):
                        self.frame_manager.switch_to(Levels(self.frame_manager)) # Por el momento cambia a ventana Levels
                        self.running = False
                    # Verificar si se hizo click en cualquiera de los botones de la lista
                    else:
                        for i,button in enumerate(self.buttons):
                            if button.is_over(mouse_pos):
                                solution = self.IniciarNono(i)
                                print(f"Se cargó la solución {i+1}.")
                                self.frame_manager.switch_to(Game(self.frame_manager,self.grid_size, solution=solution))
                                self.running = False
                        break



    def draw(self):
        self.frame_manager.screen.fill(SettingsManager.BACKGROUND_COLOR.value)  # Fondo morado oscuro
        # Dibuja los botones de cada nonograma a resolver
        self.button_custom.draw(self.frame_manager.screen)
        self.backButton.draw(self.frame_manager.screen)
        for button in self.buttons:
            button.draw(self.frame_manager.screen)

        # Actualiza la ventana
        pygame.display.flip()







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
    save_cont = {} # Diccionario para llevar la cuenta de los archivos guardados.

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
        board_width = self.grid_size * self.cell_size

        # Dibujar las celdas
        for row, rowOfCells in enumerate(self.board):
            for col, cell in enumerate(rowOfCells):
                color = cell.get_color()
                pygame.draw.rect(surface, color, (
                    self.offset_x + col * self.cell_size,  # Coordenada x ajustada
                    self.offset_y + row * self.cell_size,  # Coordenada y ajustada
                    self.cell_size - 2, self.cell_size - 2))  # Tamaño de la celda con un borde pequeño
        # Dibujar lineas de separacion (cada 5x5)
        line_color = (0,0,0)
        for i in range(0, self.grid_size+1,5):
            # Línea vertical cada 5 celdas
            pygame.draw.line(surface, line_color,
                             (self.offset_x + i * self.cell_size, self.offset_y),
                             (self.offset_x + i * self.cell_size, self.offset_y + board_width), 3)
            # Línea horizontal cada 5 celdas
            pygame.draw.line(surface, line_color,
                             (self.offset_x, self.offset_y + i * self.cell_size),
                             (self.offset_x + board_width, self.offset_y + i * self.cell_size), 3)

        #Dibujar numeros en filas
        for i,numbers in enumerate(self.rarray):
            text = "  ".join(map(str, numbers))
            row_number_surface = self.font.render(text, True, SettingsManager.NUMBERS_COLOR.value)
            surface.blit(row_number_surface, (
                self.offset_x + i - 180,
                self.offset_y + i * self.cell_size + self.cell_size // 2 - 10,
            ))

        #Dibujar numeros en columnas
        for i,numbers in enumerate(self.carray):
            for j, number in enumerate(numbers):
                text = str(number)
                col_number_surface = self.font.render(text, True, SettingsManager.NUMBERS_COLOR.value)
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

    def guardar(self, filename):
        # Obtener el directorio del proyecto
        proyecto_directory = os.path.dirname(os.path.abspath(__file__))
        saved_files_directory = os.path.join(proyecto_directory, 'saved_files')

        # Crear el subdirectorio si no existe
        if not os.path.exists(saved_files_directory):
            os.makedirs(saved_files_directory)

        # Agregar timestamp al nombre del archivo
        if self.grid_size not in Board.save_cont:
            Board.save_cont[self.grid_size] = 1
        else:
            Board.save_cont[self.grid_size] += 1

        full_name = f"{filename}_{self.grid_size}x{self.grid_size}_{Board.save_cont[self.grid_size]}.pkl" # Ejemplo: saved_board_5x5_1.pkl
        full_path = os.path.join(saved_files_directory, full_name) # Combinar ruta del subdirectorio con nombre archivo

        try:
            print("Guardando archivo en:", full_path)
            with open(full_path, 'wb') as file: # Abre en modo binario para guardar con pickle
                pickle.dump(self.board, file) # Guarda el tablero en el archivo
            return True
        except Exception as e:
            print(f"Error al guardar el tablero: {e}")
            return False

class Options(Scene):
    def __init__(self, frame_manager):
        super().__init__(frame_manager)
        self.slider = Slider(500, 300, 300, min_value=0, max_value=1, initial_value=0.5)
        self.song_name = "Darude - Sandstorm"  # Nombre del archivo que se está reproduciendo
        self.text_x = SettingsManager.WIDTH.value  # Comienza fuera de la pantalla, a la derecha
        self.text_y = SettingsManager.HEIGHT.value - 40  # Ubicación vertical en la parte inferior

        self.back_button = Button(200, 500, 'Back', self.font)

    def handle_events(self):
        for event in pygame.event.get():
            self.back_button.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Verifica si se hace clic con el botón izquierdo del mouse
                    mouse_pos = pygame.mouse.get_pos()
                    if self.back_button.is_over(mouse_pos):
                        self.frame_manager.switch_to(
                            Menu(self.frame_manager))  # Cambia a la ventana del selector de niveles
                        self.running = False  # Detenemos la ventana

            if event.type == pygame.QUIT:
                self.running = False
                self.frame_manager.current_scene = None
            self.slider.handle_event(event)

    def draw(self):
        self.frame_manager.screen.fill(SettingsManager.BACKGROUND_COLOR.value)
        self.slider.draw(self.frame_manager.screen)
        self.back_button.draw(self.frame_manager.screen)

        # Muestra el valor del volumen
        font = pygame.font.Font("fonts/monogram.ttf", 36)
        text = font.render(f"Volume: {int(self.slider.value * 100)}%", True, (255, 255, 255))
        self.frame_manager.screen.blit(text, (self.slider.x, self.slider.y - 40))

        # Ajusta el volumen de la música
        pygame.mixer.music.set_volume(self.slider.value)

        # Deslizar el texto del nombre del archivo
        self.draw_sliding_text(self.song_name)

        pygame.display.flip()

    def draw_sliding_text(self, text):
        font = pygame.font.Font("fonts/monogram.ttf", 36)
        rendered_text = font.render(text, True, (210, 255, 77))

        # Dibujar el texto deslizando hacia la izquierda
        self.frame_manager.screen.blit(rendered_text, (self.text_x, self.text_y))

        # Actualizar la posición para el deslizamiento
        self.text_x -= 0.25  # Ajusta la velocidad de deslizamiento
        if self.text_x < -rendered_text.get_width():
            self.text_x = SettingsManager.WIDTH.value  # Restablecer la posición al lado derecho cuando se ha deslizado completamente