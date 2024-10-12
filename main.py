from GUI import *

pygame.init()

# Inicia pygame y Frame
manager = Frame()
menu = Menu(manager)
# Muestra el menú
manager.switch_to(menu)
manager.run()   # Se ejecuta el `Menu`
pygame.quit()

