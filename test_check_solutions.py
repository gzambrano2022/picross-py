import unittest
from unittest.mock import MagicMock
import pygame
import pytest

from GUI import Board

@pytest.fixture(scope='module', autouse=True)
def setuppygame():
    pygame.init()
    yield
    pygame.quit()

@pytest.mark.parametrize('grid_size', [5,10,15])
def test_check_solutions(grid_size):
    logical_board = MagicMock()
    logical_board.get_matrix.return_value = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    logical_board.get_solution.return_value = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    board = Board(
        grid_size=grid_size,
        frame_width=500,
        frame_height=500,
        logicalboard= logical_board,
    )


    board.board_l[0][0] = 1
    board.board_s[0][0] = 1

    result = board.check_solution(grid_size=grid_size)
    assert result is True