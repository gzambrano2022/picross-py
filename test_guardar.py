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
    # Configurar directorio esperado para guardar
    proyecto_directory = os.path.dirname(os.path.abspath(__file__))
    saved_files_directory = os.path.join(proyecto_directory, 'saved_files')
    subdirectory = f'saved_files_{grid_size}x{grid_size}'
    subdirectory_path = os.path.join(saved_files_directory, subdirectory)
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

    # Crear una solución simulada
    solution = [[1] * grid_size for _ in range(grid_size)]

    # Guardar el tablero
    filename = 'saved_board'
    assert board.guardar(filename, solution) == True

    # Verificar que el archivo se haya guardado en el subdirectorio correcto
    saved_files = os.listdir(subdirectory_path)
    print(f"Archivos guardados en {subdirectory_path}: {saved_files}")  # Añadir depuración
    assert any(filename in f for f in saved_files)

    # Verificar contenido del archivo guardado
    saved_file_path = os.path.join(subdirectory_path, saved_files[0])
    import pickle
    with open(saved_file_path, 'rb') as file:
        data = pickle.load(file)
        assert data['current_state'] == game_instance.current_state
        assert data['solution'] == solution

    # Limpiar archivos guardados después del test
    for f in saved_files:
        os.remove(os.path.join(subdirectory_path, f))
