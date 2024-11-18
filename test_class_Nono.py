import pickle
import unittest
from io import BytesIO
from unittest.mock import MagicMock, patch
from GUI import Nonos
import pygame

class TestNonos(unittest.TestCase):

    # Inicializa Pygame antes de cada prueba
    def setUp(self):
        pygame.init()  # Inicializamos Pygame

    # Cierra Pygame después de cada prueba
    def tearDown(self):
        pygame.quit()

        # Caso donde carga correctamente una solución
    @patch('os.listdir')
    def test_iniciar_sucess(self, mock_listdir):
        # Mockear la lista de soluciones
        mock_listdir.return_value = ['solution1.pkl', 'solution2.pkl']

        # Crear objeto Nonos
        nonos = Nonos(frame_manager=MagicMock(), grid_size=5)

        # Mockear el contenido del archivo .pkl
        mock_solution = {'solution':'data'}
        mock_file = BytesIO(pickle.dumps(mock_solution))

        # Mockear la función open para devolver el archivo falso
        with patch('builtins.open', return_value=mock_file):
            solution = nonos.IniciarNono(0) #Llamamos a IniciarNono con el primer botón
            self.assertEqual(solution, mock_solution)
            mock_file.close()

    # Caso donde no carga el archivo porque el índice está fuera de rango
    @patch('os.listdir')
    def test_iniciar_fail_index(self, mock_listdir):
        mock_listdir.return_value = ['solution1.pkl', 'solution2.pkl']
        nonos = Nonos(frame_manager=MagicMock(), grid_size=5)

        solution = nonos.IniciarNono(5)
        self.assertIsNone(solution)

    # Caso donde no carga el archivo porque no existe
    @patch('os.listdir')
    @patch('builtins.open',side_effect=FileNotFoundError)
    def test_iniciar_fail_archivo(self,mock_open, mock_listdir):
        mock_listdir.return_value = ['solution1.pkl', 'solution2.pkl']
        nonos = Nonos(frame_manager=MagicMock(), grid_size=5)
        solution = nonos.IniciarNono(0)
        self.assertIsNone(solution)