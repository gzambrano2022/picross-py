class WindowManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.current_window = None

    def switch_to(self, new_window):
        self.current_window = new_window

    def run(self):
        while self.current_window is not None:
            self.current_window.run()