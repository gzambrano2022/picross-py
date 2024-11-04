from idlelib.colorizer import color_config

import pygame


class Title:
    def __init__(self, width, height, texto, fuente, tamaño=None):
        # Si no se especifica un tamaño, se calcula como una fracción del alto de la ventana
        if tamaño is None:
            tamaño = height // 12  # Por ejemplo, una doceava parte de la altura de la ventana

        # Usar la fuente y el tamaño proporcionados o calculados
        self.font = pygame.font.Font(fuente, tamaño)
        self.text = self.font.render(texto, True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(width // 2, height // 8))

    def draw(self, window):
        window.blit(self.text, self.text_rect)

class Button:
    def __init__(self, x, y, text, font, width=140, height=40, color=(100, 100, 100), text_color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text_color = text_color
        self.font = font
        self.text = self.font.render(text, True, self.text_color)

    def draw(self, window):
        # Dibuja el rectángulo del botón
        pygame.draw.rect(window, self.color, [self.x, self.y, self.width, self.height])
        # Coloca el texto en el botón (centrado)
        window.blit(self.text, (self.x + (self.width - self.text.get_width()) // 2, self.y + (self.height - self.text.get_height()) // 2))

    def is_over(self, pos):
        # Verifica si el mouse está sobre el botón
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height
