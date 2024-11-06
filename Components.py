from idlelib.colorizer import color_config

import pygame


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
    def __init__(self, x, y, text, font, width=140, height=40, color=(0, 37, 53), text_color=(210, 255, 77),
                 border_color=(210, 255, 77), border_width=3, shadow_offset=(8,8), shadow_color=(0, 51, 37)):
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
        self.text = self.font.render(text, True, self.text_color)
        self.border_color = border_color
        self.border_width = border_width
        self.shadow_offset = shadow_offset
        self.shadow_color = shadow_color
        self.is_hovered = False
        self.is_clicked = False

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

        # Renderiza el texto en el botón (centrado)
        window.blit(self.text, (
        x + (current_width - self.text.get_width()) // 2, y + (current_height - self.text.get_height()) // 2))

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
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_clicked = False
