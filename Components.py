from idlelib.colorizer import color_config

import pygame
import os

class Title:
    def __init__(self, width, height, texto, fuente, tamaño=None):
        # Si no se especifica un tamaño, se calcula como una fracción del alto de la ventana
        if tamaño is None:
            tamaño = height // 12  # Por ejemplo, una doceava parte de la altura de la ventana

        # Usar la fuente y el tamaño proporcionados o calculados
        self.font = pygame.font.Font(fuente, tamaño)
        self.text = self.font.render(texto, True, (210, 255, 77))
        self.text_rect = self.text.get_rect(center=(width // 2, height // 8))

    def draw(self, window):
        window.blit(self.text, self.text_rect)




class Button:
    def __init__(self, x, y, text=None, font=None, width=140, height=40, color=(0, 37, 53), text_color=(210, 255, 77),
                 border_color=(210, 255, 77), border_width=3, shadow_offset=(8, 8), shadow_color=(0, 51, 37),
                 sound_path= None, sound_volume = 0.25, icon_path=None):  # Añadimos un parámetro para el sonido
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.default_width = width
        self.default_height = height
        self.color = color
        self.default_color = color
        self.hover_color = (
        min(color[0] + 30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255))  # Más claro al hacer hover
        self.click_color = (
        max(color[0] - 30, 0), max(color[1] - 30, 0), max(color[2] - 30, 0))  # Más oscuro al hacer click

        self.text_color = text_color
        self.font = font
        self.text = None

        # Solo renderiza el texto si se proporcionan texto y fuente
        if text and font:
            self.text = font.render(text, True, self.text_color)
        self.border_color = border_color
        self.border_width = border_width
        self.shadow_offset = shadow_offset
        self.shadow_color = shadow_color
        self.is_hovered = False
        self.is_clicked = False

        # Ruta por defecto para el sonido
        default_sound_path = os.path.join("sounds", "pickupCoin.wav")


        # Cargar sonido si se proporciona un path o si no se pasa se usa el predeterminado
        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)
        else:
            # Cargar el sonido por defecto
            self.sound = pygame.mixer.Sound(default_sound_path)
        self.sound.set_volume(sound_volume)

        # Ruta del icono (opcional)
        self.icon = None
        if icon_path:
            self.icon = pygame.image.load(icon_path)  # Carga la imagen del icono
            self.icon = pygame.transform.scale(self.icon, (self.width // 2, self.height // 2))  # Escala la imagen


    def draw(self, window):
        # Actualiza el tamaño y color del botón según el estado
        if self.is_clicked:
            current_color = self.click_color
            current_width = self.default_width * 0.95
            current_height = self.default_height * 0.95
        elif self.is_hovered:
            current_color = self.hover_color
            current_width = self.default_width * 1.05
            current_height = self.default_height * 1.05
        else:
            current_color = self.default_color
            current_width = self.default_width
            current_height = self.default_height

        # Calcular la posición para centrar el botón expandido
        x = self.x - (current_width - self.default_width) / 2
        y = self.y - (current_height - self.default_height) / 2

        # Dibuja la sombra del botón
        shadow_x = x + self.shadow_offset[0]
        shadow_y = y + self.shadow_offset[1]
        pygame.draw.rect(window, self.shadow_color, [shadow_x, shadow_y, current_width, current_height])

        # Dibuja el borde del botón
        pygame.draw.rect(window, self.border_color,
                         [x - self.border_width, y - self.border_width, current_width + 2 * self.border_width,
                          current_height + 2 * self.border_width])

        # Dibuja el rectángulo del botón
        pygame.draw.rect(window, current_color, [x, y, current_width, current_height])

        # Renderiza el texto en el botón (centrado), si existe
        if self.text:  # Solo dibuja el texto si está definido
            window.blit(self.text, (
                x + (current_width - self.text.get_width()) // 2, y + (current_height - self.text.get_height()) // 2))

        # Si hay un icono, dibújalo en el centro del botón
        if self.icon:
            icon_x = x + (current_width - self.icon.get_width()) // 2
            icon_y = y + (current_height - self.icon.get_height()) // 2
            window.blit(self.icon, (icon_x, icon_y))


    def is_over(self, pos):
        # Verifica si el mouse está sobre el botón
        return self.x <= pos[0] <= self.x + self.default_width and self.y <= pos[1] <= self.y + self.default_height

    def handle_event(self, event):
        # Cambia el estado de hover y click según el evento
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.is_over(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:  # Botón izquierdo del mouse
                self.is_clicked = True
                if self.sound:
                    self.sound.play()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_clicked = False  # Asegúrate de que esta línea tenga la misma indentación que el 'if'


class ToggleButton(Button):  # Heredamos de Button
    def __init__(self, x, y, text, font, icon_path_1=None, icon_path_2=None, width=140, height=40, color=(0, 37, 53),
                 text_color=(210, 255, 77), border_color=(210, 255, 77), border_width=3, shadow_offset=(8, 8),
                 shadow_color=(0, 51, 37), sound_path=None, sound_volume=0.25):
        # Inicializamos el Button original
        super().__init__(x, y, text, font, width, height, color, text_color, border_color, border_width,
                         shadow_offset, shadow_color, sound_path, sound_volume)

        # Cargamos los dos iconos para el toggle
        self.icon_1 = pygame.image.load(icon_path_1)  # Primer icono
        self.icon_2 = pygame.image.load(icon_path_2)  # Segundo icono
        self.icon_1 = pygame.transform.scale(self.icon_1,
                                             (self.width // 2, self.height // 2))  # Escala al tamaño adecuado
        self.icon_2 = pygame.transform.scale(self.icon_2,
                                             (self.width // 2, self.height // 2))  # Escala al tamaño adecuado

        # El estado del toggle: True significa mostrar icono 1, False significa mostrar icono 2
        self.is_toggled = False

    def toggle(self):
        # Cambia el estado del toggle (True -> False, o False -> True)
        self.is_toggled = not self.is_toggled

    def draw(self, window):
        # Dibuja el botón como el Button original
        super().draw(window)

        # Según el estado del toggle, dibujamos uno de los iconos
        if self.is_toggled:
            icon = self.icon_1
        else:
            icon = self.icon_2

        # Calcular la posición del icono en el centro del botón
        icon_x = self.x + (self.width - icon.get_width()) // 2
        icon_y = self.y + (self.height - icon.get_height()) // 2

        # Dibujar el icono en el botón
        window.blit(icon, (icon_x, icon_y))

    def handle_event(self, event):
        # Llamar al método handle_event original para detectar clics
        super().handle_event(event)

        # Si el botón es presionado, cambia el estado del toggle
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_over(event.pos):
            self.toggle()  # Cambiar el estado del toggle

# Clase Slider para controlar el volumen
class Slider:
    def __init__(self, x, y, width, min_value=0, max_value=1, initial_value=0.25):
        self.x = x
        self.y = y
        self.width = width
        self.height = 5
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value  # Valor inicial de volumen
        self.is_dragging = False  # Verifica si el slider está siendo arrastrado
        self.handle_width = 20  # Ancho del control deslizante

    def draw(self, window):
        # Dibuja la barra del slider
        pygame.draw.rect(window, (200, 200, 200), (self.x, self.y, self.width, self.height))

        # Dibuja el control del slider (circular)
        handle_x = self.x + (self.value * (self.width - self.handle_width))
        pygame.draw.circle(window, (255, 0, 66), (int(handle_x), self.y + self.height // 2), self.handle_width // 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_mouse_over(event.pos):
                self.is_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                self.update_value(event.pos)

    def update_value(self, mouse_pos):
        # Calcula el valor del slider basado en la posición del mouse
        x = mouse_pos[0] - self.x
        self.value = max(self.min_value, min(self.max_value, x / self.width))  # Limita el valor entre 0 y 1

    def is_mouse_over(self, pos):
        # Verifica si el mouse está sobre el slider
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height