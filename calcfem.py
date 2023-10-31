from scipy.interpolate import griddata
import numpy as np
from elements import ElementMatrices
import matplotlib.tri as tri
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import math
from typing import List, Tuple, Union
from scipy.sparse import coo_matrix


class CalcFEM:

    def __init__(self, params_mesh, params_boundaries_materials):
        """

        :param params:
        """
        # von GUI übergebene Werte aus CreateMesh:
        self.nodes_mesh_gen = params_mesh[0]
        self.single_nodes_dict = params_mesh[1]
        self.boundary_nodes_dict = params_mesh[2]
        self.triangulation = params_mesh[3]
        self.triangulation_region_dict = params_mesh[4]
        # von GUI übergebene Werte aus Boundary/Materials/Calculation Defintion
        self.region_parameters = params_boundaries_materials[0]
        self.boundary_parameters = params_boundaries_materials[1]
        self.node_parameters = params_boundaries_materials[2]
        self.calculation_parameters = params_boundaries_materials[3]
        # Instance vars created
        self.all_element_matrices_steif = None
        self.all_element_matrices_mass = None
        self.force_vector = None
        self.syssteifarray = None
        self.sysmassarray = None
        self.sysarray = None

    def calc_fem(self):
        """
        main method for calculation, calculates elementmatrices, assembly of system matrices,
        implements boundary conditions, solves linear system
        :return:
        """
        self.equation = self.calculation_parameters['equation']  # either HE (HeatEquation) or HH (HelmHoltz)

        # calculate element matrices
        self.calc_elementmatrices()
        
        # assembly system matrices
        self.calc_system_matrices()

        # create force vector
        self.create_force_vector()

        # implement boundary conditions
        self.implement_boundary_conditions()

    def create_force_vector(self):
        maxnode = len(self.nodes_mesh_gen)
        self.force_vector = np.zeros(maxnode, dtype=np.single)

    def implement_boundary_conditions(self):
        ...
    
    def calc_system_matrices(self):
        """
        
        :return: 
        """
        maxnode = len(self.nodes_mesh_gen)
        nbr_of_elements = len(self.triangulation)
        alloc_mat = self.triangulation
        self.syssteifarray = np.zeros((maxnode, maxnode), dtype=np.single)
        self.sysmassarray = np.zeros((maxnode, maxnode), dtype=np.single)
        self.sysarray = np.zeros((maxnode, maxnode), dtype=np.single)


        for ielem in range(nbr_of_elements):
            elesteifmat = self.all_element_matrices_steif[ielem]
            elemassmat = self.all_element_matrices_mass[ielem]
            for a in range(3):
                for b in range(3):
                    zta = int(alloc_mat[ielem, a])
                    ztb = int(alloc_mat[ielem, b])
                    self.syssteifarray[zta, ztb] = self.syssteifarray[zta, ztb] + elesteifmat[a, b]
                    self.sysmassarray[zta, ztb] = self.sysmassarray[zta, ztb] + elemassmat[a, b]

        if self.equation == 'HE':
            self.sysarray = self.syssteifarray
        elif self.equation == 'HH':  # todo: include in elementmatrices
            ...


    def calc_elementmatrices(self):
        """

        :return:
        """

        def get_region_number(idx: int):
            """

            :param idx:
            :return:
            """
            for region, triangles in self.triangulation_region_dict.items():
                if idx in triangles:
                    return region

        nbr_of_elements = len(self.triangulation)

        self.all_element_matrices_steif = np.zeros((nbr_of_elements, 3, 3), dtype=np.single)
        self.all_element_matrices_mass = np.zeros((nbr_of_elements, 3, 3), dtype=np.single)

        elemsteif = None
        elemmass = None
        for idx, triangle in enumerate(self.triangulation):
            b_region = get_region_number(idx)
            materials = self.region_parameters[b_region]['material']
            k = materials['k']
            c = materials['c']
            rho = materials['rho']
            p1, p2, p3 = triangle[0], triangle[1], triangle[2]
            x1 = self.nodes_mesh_gen[p1][0]
            y1 = self.nodes_mesh_gen[p1][1]
            x2 = self.nodes_mesh_gen[p2][0]
            y2 = self.nodes_mesh_gen[p2][1]
            x3 = self.nodes_mesh_gen[p3][0]
            y3 = self.nodes_mesh_gen[p3][1]
            nodes = [[x1, y1], [x2, y2], [x3, y3]]
            if self.equation == 'HE':
                elemsteif, elemmass = ElementMatrices.calc_2d_triangular_heatflow_p1(k, nodes)
            elif self.equation == 'HH':
                elemsteif, elemmass = ElementMatrices.calc_2d_triangular_acoustic_p1(c, rho, nodes)
            self.all_element_matrices_steif[idx] = elemsteif
            if elemmass is not None:  # since it might be a np.array
                self.all_element_matrices_mass[idx] = elemmass



if __name__ == '__main__':
    calcfem = CalcFEM((0,0,0,0,0), (0,0,0,0))  # Develop

    calcfem.nodes_mesh_gen = [[0.5, 0.5], [0.,  0. ], [0.5, 0. ], [1.,  0. ], [1.,  0.5], [1.,  1. ], [0.5, 1. ], [0.,  1. ], [0.,  0.5], [1.,  1.5], [1.,  2. ], [0.5, 1.5]]
    calcfem.single_nodes_dict = {'0': 1, '1': 3, '2': 5, '3': 7, '4': 10}
    calcfem.boundary_nodes_dict = {'0': [[1, np.array([0., 0.])], [2, np.array([0.5, 0. ])], [3, np.array([1., 0.])]], '1': [[3, np.array([1., 0.])], [4, np.array([1. , 0.5])], [5, np.array([1., 1.])]], '2': [[5, np.array([1., 1.])], [6, np.array([0.5, 1. ])], [7, np.array([0., 1.])]], '3': [[7, np.array([0., 1.])], [8, np.array([0. , 0.5])], [1, np.array([0., 0.])]], '4': [[5, np.array([1., 1.])], [9, np.array([1. , 1.5])], [10, np.array([1., 2.])]], '5': [[10, np.array([1., 2.])], [11, np.array([0.5, 1.5])], [7, np.array([0., 1.])]]}
    calcfem.triangulation = np.array([[2,4,0],[4,2,3],[4,6,0],[6,4,5],[8,2,0],[2,8,1],[6,8,0],[8,6,7],[6,11,7],[11,9,10],[6,9,11],[9,6,5]])
    calcfem.triangulation_region_dict = {'0': range(0, 8), '1': range(8, 12)}
    calcfem.calculation_parameters = {'mesh_density': 1, 'freq': None, 'equation': 'HE'}
    calcfem.region_parameters = {
            '0': {'coordinates': [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)], 'area_neg_pos': 'Positive',
                  'material'   : {'k': 1.0, 'c': 0, 'rho': 0}},
            '1': {'coordinates': [(0.0, 1.0), (1.0, 1.0), (1.0, 2.0)], 'area_neg_pos': 'Positive',
                  'material'   : {'k': 2.0, 'c': 0, 'rho': 0}}}
    calcfem.boundary_parameters = {'0': {'coordinates': [(0.0, 0.0), (1.0, 0.0)], 'bc': {'type': None, 'value': None}},
                                '1': {'coordinates': [(1.0, 0.0), (1.0, 1.0)], 'bc': {'type': None, 'value': None}},
                                '2': {'coordinates': [(1.0, 1.0), (0.0, 1.0)], 'bc': {'type': None, 'value': None}},
                                '3': {'coordinates': [(0.0, 1.0), (0.0, 0.0)],
                                      'bc'         : {'type': 'Dirichlet', 'value': 3.0}},
                                '4': {'coordinates': [(1.0, 1.0), (1.0, 2.0)],
                                      'bc'         : {'type': 'Dirichlet', 'value': 4.0}},
                                '5': {'coordinates': [(1.0, 2.0), (0.0, 1.0)], 'bc': {'type': None, 'value': None}}}
    calcfem.node_parameters = {'0': {'coordinates': (0.5, 0.5), 'bc': {'type': None, 'value': None}},
                            '1': {'coordinates': (0.0, 0.0), 'bc': {'type': None, 'value': None}},
                            '2': {'coordinates': (1.0, 0.0), 'bc': {'type': None, 'value': None}},
                            '3': {'coordinates': (1.0, 1.0), 'bc': {'type': None, 'value': None}},
                            '4': {'coordinates': (0.0, 1.0), 'bc': {'type': None, 'value': None}},
                            '5': {'coordinates': (1.0, 2.0), 'bc': {'type': None, 'value': None}}}
    calcfem.calculation_parameters = {'mesh_density': 1, 'freq': None, 'equation': 'HE'}

    calcfem.calc_fem()
