import numpy as np
import pytest
from GUI import LogicalBoard
from unittest.mock import patch

@pytest.fixture
def logical_board():
    return LogicalBoard(3)

def test_find_numbers_r(logical_board):
    logical_board.board_l = np.array([[0, 0, 0],
                                      [0, 0, 0],
                                      [0, 0, 0]])
    result = logical_board.find_numbers_r()
    assert result == [[0], [0], [0]]

def test_find_numbers_c(logical_board):
    logical_board.board_l = np.array([[1, 1, 0],
                                      [0, 1, 1],
                                      [1, 0, 0]])
    result = logical_board.find_numbers_c()
    assert result == [[1,1], [2], [1]]

@patch('GUI.LogicalBoard.fill_board')
def test_fill_board(mock_fill_board,logical_board):
    mock_fill_board.return_value = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    result = logical_board.fill_board()
    assert np.array_equal(result, np.array([[0,0,0], [0,0,0], [0,0,0]]))
