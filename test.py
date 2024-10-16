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
    os.makedirs('saved_files', exist_ok=True)

    mock_logicalboard = MagicMock()

    board = Board(
        grid_size=grid_size,
        frame_width=500,
        frame_height=500,
        logicalboard=mock_logicalboard
    )


    board.board[0][0].click()
    filename = 'saved_board'
    assert board.guardar(filename) == True
    assert any(filename in f for f in os.listdir('saved_files'))

    for f in os.listdir('saved_files'):
        if filename in f:
            os.remove(os.path.join('saved_files', f))



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
