from GUI import *

pygame.init()

# Inicia pygame y el WindowManager
window_manager = Frame(SettingsManager.WIDTH.value, SettingsManager.HEIGHT.value, SettingsManager.BACKGROUND_COLOR.value)

# Muestra el menú
menu = Menu(window_manager)
menu.run()  # La clase `Menu` ahora gestiona todo, incluyendo la transición al juego.

pygame.quit()

