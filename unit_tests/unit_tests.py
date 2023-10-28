import numpy as np
from meshgen import CreateMesh
import unittest

region_parameters1 = {'0': {'coordinates': [(-4.0, -3.0), (1.0, -2.5), (2.5, 1.0), (-2.5, 1.0), (-4.2, -1.5)],
                            'area_neg_pos': 'Positive', 'material': {'k': 0, 'c': 0, 'rho': 0}},
                      '1': {'coordinates': [(2.5, 1.0), (0.0, 3.0), (-2.5, 1.0)], 'area_neg_pos': 'Positive',
                            'material': {'k': 0, 'c': 0, 'rho': 0}},
                      '2': {'coordinates': [(-1.0, 0.0), (0.0, 0.0), (0.0, 0.75), (-1.0, 0.5)],
                            'area_neg_pos': 'Negative', 'material': {'k': 0, 'c': 0, 'rho': 0}}}
boundary_parameters1 = {'0': {'coordinates': [(-4.0, -3.0), (1.0, -2.5)], 'bc': {'type': None, 'value': None}},
                        '1': {'coordinates': [(1.0, -2.5), (2.5, 1.0)], 'bc': {'type': None, 'value': None}},
                        '2': {'coordinates': [(2.5, 1.0), (-2.5, 1.0)], 'bc': {'type': None, 'value': None}},
                        '3': {'coordinates': [(-2.5, 1.0), (-4.2, -1.5)], 'bc': {'type': None, 'value': None}},
                        '4': {'coordinates': [(-4.2, -1.5), (-4.0, -3.0)], 'bc': {'type': None, 'value': None}},
                        '5': {'coordinates': [(2.5, 1.0), (0.0, 3.0)], 'bc': {'type': None, 'value': None}},
                        '6': {'coordinates': [(0.0, 3.0), (-2.5, 1.0)], 'bc': {'type': None, 'value': None}},
                        '7': {'coordinates': [(-1.0, 0.0), (0.0, 0.0)], 'bc': {'type': None, 'value': None}},
                        '8': {'coordinates': [(0.0, 0.0), (0.0, 0.75)], 'bc': {'type': None, 'value': None}},
                        '9': {'coordinates': [(0.0, 0.75), (-1.0, 0.5)], 'bc': {'type': None, 'value': None}},
                        '10': {'coordinates': [(-1.0, 0.5), (-1.0, 0.0)], 'bc': {'type': None, 'value': None}}}
node_parameters1 = {'0': {'coordinates': (-3.0, -2.0), 'bc': {'type': None, 'value': None}},
                    '1': {'coordinates': (0.0, 1.5), 'bc': {'type': None, 'value': None}},
                    '2': {'coordinates': (1.0, -1.0), 'bc': {'type': None, 'value': None}},
                    '3': {'coordinates': (-4.0, -3.0), 'bc': {'type': None, 'value': None}},
                    '4': {'coordinates': (1.0, -2.5), 'bc': {'type': None, 'value': None}},
                    '5': {'coordinates': (2.5, 1.0), 'bc': {'type': None, 'value': None}},
                    '6': {'coordinates': (-2.5, 1.0), 'bc': {'type': None, 'value': None}},
                    '7': {'coordinates': (-4.2, -1.5), 'bc': {'type': None, 'value': None}},
                    '8': {'coordinates': (0.0, 3.0), 'bc': {'type': None, 'value': None}},
                    '9': {'coordinates': (-1.0, 0.0), 'bc': {'type': None, 'value': None}},
                    '10': {'coordinates': (0.0, 0.0), 'bc': {'type': None, 'value': None}},
                    '11': {'coordinates': (0.0, 0.75), 'bc': {'type': None, 'value': None}},
                    '12': {'coordinates': (-1.0, 0.5), 'bc': {'type': None, 'value': None}}}
calculation_parameters1 = {'mesh_density': 2, 'freq': None}
params1 = (region_parameters1, boundary_parameters1, node_parameters1, calculation_parameters1)
createmesh = CreateMesh(*params1)  # Todo - Develop: For testing mesh

class TestCreateMesh(unittest.TestCase):
    def test_check_vertice_in_polygon_area1(self):
        createmesh = CreateMesh(*params1)
        polygon = [[0, 0], [1, 0], [1, 1], [0, 1]]
        point = [0.5, 0.5]  # inside polygon
        result = createmesh.check_vertice_in_polygon_area(point, polygon)
        self.assertEqual(result, True)

    def test_check_vertice_in_polygon_area2(self):
        polygon = [[0, 0], [1, 0], [1, 1], [0, 1]]
        point = [0.5, 0.0]  # on boundary
        result = createmesh.check_vertice_in_polygon_area(point, polygon)
        self.assertEqual(result, False)

    def test_check_vertice_in_polygon_area3(self):
        polygon = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])  # as np.array
        point = np.array([0.5, 0.5])  # as np.array
        result = createmesh.check_vertice_in_polygon_area(point, polygon)
        self.assertEqual(result, True)

    def test_check_vertice_in_polygon_area4(self):
        polygon = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])  # as np.array
        point = np.array([0.5, 0.0])  # as np.array, on boundary
        result = createmesh.check_vertice_in_polygon_area(point, polygon)
        self.assertEqual(result, False)

    def test_check_vertice_in_polygon_area5(self):
        polygon = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])  # as np.array
        point = np.array([0.5, 0.00000001])  # as np.array, very close to boundary
        result = createmesh.check_vertice_in_polygon_area(point, polygon)
        self.assertEqual(result, True)

    def test_check_vertice_in_polygon_area6(self):
        polygon = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])  # as np.array
        point = np.array([1, 1])  # on point 1, 1 -> True for some reason...
        result = createmesh.check_vertice_in_polygon_area(point, polygon)
        self.assertEqual(result, True)

    def test_check_vertice_in_polygon_area7(self):
        polygon = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])  # as np.array
        point = np.array([0, 0])  # on point 0, 0 -> False for some reason...
        result = createmesh.check_vertice_in_polygon_area(point, polygon)
        self.assertEqual(result, False)

