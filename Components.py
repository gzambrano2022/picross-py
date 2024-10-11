import pygame


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
