import os

import pygame
import pytest
from unittest.mock import MagicMock
from GUI import Board, Cell

@pytest.fixture(scope="module", autouse=True)
def setuppygame():
    # Inicializamos Pygame antes de los tests
    pygame.init()
    yield
    # Cerramos Pygame después de los tests
    pygame.quit()

@pytest.mark.parametrize("grid_size", [5, 10, 15])
def test_guardar(grid_size):
    subdirectory_path = os.path.join('saved_files', f'saved_files_{grid_size}x{grid_size}')
    os.makedirs(subdirectory_path, exist_ok=True)

    mock_logicalboard = MagicMock()
    game_instance = MagicMock()
    game_instance.current_state = [[0] * grid_size for _ in range(grid_size)]

    board = Board(
        grid_size=grid_size,
        frame_width=500,
        frame_height=500,
        logicalboard=mock_logicalboard,
        game_instance=game_instance
    )

    board.board[0][0].clicked = True
    filename = 'saved_board'
    assert board.guardar(filename) == True

    # Verificar que el archivo se haya guardado en el subdirectorio correcto
    saved_files = os.listdir(subdirectory_path)
    print(f"Archivos guardados en {subdirectory_path}: {saved_files}")  # Añadir depuración
    assert any(filename in f for f in saved_files)

    # Limpiar archivos guardados después del test
    for f in saved_files:
        if filename in f:
            os.remove(os.path.join(subdirectory_path, f))




@pytest.mark.parametrize("grid_size", [5, 10, 15])
def test_cargar(grid_size):
    os.makedirs('saved_files', exist_ok=True)

    board = Board(cell_size=50, grid_size=grid_size)

    board.board[0][0].click()
    filename = f'saved_board{grid_size}x{grid_size}_1.pkl'
    board.guardar('saved_board')

    new_board = Board(cell_size=50, grid_size=grid_size)
    assert new_board.cargar(filename) == True

    assert new_board.board[0][0].is_clicked()

    os.remove(os.path.join('saved_files', filename))
