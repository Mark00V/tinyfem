from scipy.interpolate import griddata
import numpy as np
from elements import ElementMatrices
import matplotlib.tri as tri
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import math
from typing import List, Tuple, Union
from scipy.sparse import coo_matrix
import copy

class CalcFEM:

    def __init__(self, params_mesh, params_boundaries_materials):
        """
        Constructor

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


    def implement_boundary_conditions(self):
        """

        :return:
        """

        # create dirichlet list for implementation of dirichlet boundary conditions
        dirichlet_list = list()
        for boundary_nbr, params in self.boundary_parameters.items():
            bc = params['bc']
            bc_type = bc['type']
            bc_value = bc['value']
            bc_pos_nodes = self.boundary_nodes_dict[boundary_nbr]
            bc_pos = [elem[0] for elem in bc_pos_nodes]
            if bc_type == 'Dirichlet':
                for node in bc_pos:
                    dirichlet_list += [[node, bc_value]]
        dirichlet_list = np.array(dirichlet_list)
        self.implement_dirichlet_condition(dirichlet_list, self.sysarray, self.force_vector)


    @staticmethod
    def implement_dirichlet_condition(dirichlet_list: np.array, system_matrix: np.array, force_vector: np.array):
        """

        :param dirichlet: np.array([[node_nbr, value],[...],...,[...]])
        :param system_matrix: np.array ([[val_11, val12,...],[val21, val22,...],[val_max_1, ...]])
        :param force_vector: np.array ([[val_1],[val_2],...])
        :return:
        """
        dirichlet_list_positions = [int(elem[0]) for elem in dirichlet_list]
        dirichlet_list_values = dirichlet_list[:, 1]

        sysmatrix_orig = np.copy(system_matrix)
        sysmatrix_adj = np.copy(system_matrix)
        force_vector_adj = np.copy(force_vector)

        # sysmatrix
        for position, _ in dirichlet_list:
            sysmatrix_adj[:, int(position)] = 0
            sysmatrix_adj[int(position), :] = 0
            sysmatrix_adj[int(position), int(position)] = 1

        # force vector
        force_vector_adj = force_vector_adj - np.dot(sysmatrix_orig[:, dirichlet_list_positions], dirichlet_list_values)
        for pos, value in dirichlet_list:
            force_vector_adj[int(pos)] = value

        # Dev
        # CalcFEM.print_matrix(sysmatrix_adj)
        # CalcFEM.print_matrix(force_vector_adj)


    def create_force_vector(self):
        maxnode = len(self.nodes_mesh_gen)
        self.force_vector = np.zeros(maxnode, dtype=np.single)
    
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


    @staticmethod
    def print_matrix(matrix: Union[np.array, list]):
        """
        Prints matrix
        :param matrix: [[val1, val2, val3],[val4,...],[...]], either np.array or list
        """

        if not isinstance(matrix[0], np.ndarray):
            if len(matrix) < 50:
                print("[", end='')
                for idx, val in enumerate(matrix):
                    if idx < len(matrix) - 1:
                        print(f"+{abs(val):.2f}," if val >= 0 else f"-{abs(val):.2f},", end='')
                    else:
                        print(f"+{abs(val):.2f}" if val >= 0 else f"-{abs(val):.2f}", end='')
                print("]")

        else:
            if len(matrix) < 50:
                print("[", end='\n')
                for idx, elem in enumerate(matrix):
                    print("[", end='')
                    for idy, val in enumerate(elem):
                        if val == 0:
                            val_str = '_____'
                        else:
                            val_str = f"+{abs(val):.2f}" if val >= 0 else f"-{abs(val):.2f}"
                        if idy < len(elem) - 1:
                            print(f"{val_str},", end='')
                        elif idy >= len(elem) - 1 and idx < len(matrix) - 1:
                            print(f"{val_str}],", end='\n')
                        else:
                            print(f"{val_str}]", end='\n')
                print("]")


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
