import os
import pytest
from GUI import Board


@pytest.mark.parametrize("grid_size", [5, 10, 15])
def test_guardar(grid_size):
    filename = f'test_{grid_size}x{grid_size}.bin'
    board = Board(cell_size=50, grid_size=grid_size, figure="test")

    # Cambiar el estado de algunas celdas para asegurarse de que se guarda correctamente
    board.board[0][0].click()
    assert board.guardar(filename) == True
    assert os.path.exists(filename)

    # Aquí podrías añadir la verificación del contenido del archivo si es necesario

    # Limpieza después de la prueba
    os.remove(filename)




