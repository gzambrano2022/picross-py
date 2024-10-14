from GUI import *

pygame.init()

# Inicia pygame y Frame
manager = FrameManager()
menu = Menu(manager)
# Muestra el menú
manager.switch_to(menu)
manager.run()   # Se ejecuta el `Menu`
pygame.quit()

