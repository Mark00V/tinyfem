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
from guistatics import GUIStatics
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
        self.sysmatrix_diri = None  # Systemmatrix after implementing Dirichlet Cond
        self.force_vector_diri = None  # Force Vector after implementing Dirichlet Cond
        self.solution = None
        self.acoustic_source = None  # sources if equation is 'HH'
        # development
        self.file_path_dev = r'testing\output_gui_4_calcfem_' + '2' + '.txt'

    def develop_print_input(self):
        print("\n\n\n------------------DEBUG--------------------")
        print(f"self.equation = {self.equation}")

        print(f"\nself.region_parameters = {self.region_parameters}")
        print(f"self.boundary_parameters = {self.boundary_parameters}")
        print(f"self.node_parameters = {self.node_parameters}")
        print(f"self.calculation_parameters = {self.calculation_parameters}")

        print(f"self.nodes_mesh_gen = {self.nodes_mesh_gen}")
        print(f"self.single_nodes_dict = {self.single_nodes_dict}")
        print(f"self.boundary_nodes_dict = {self.boundary_nodes_dict}")
        print(f"self.triangulation = {self.triangulation}")
        print(f"self.triangulation_region_dict = {self.triangulation_region_dict}")

    def develop(self):
        """
        loads data for development
        :return:
        """
        with open(self.file_path_dev, 'r') as f:
            content = f.read()
        exec(content)

    def calc_fem(self):
        """
        main method for calculation, calculates elementmatrices, assembly of system matrices,
        implements boundary conditions, solves linear system
        :return:
        """

        # set equation
        self.equation = self.calculation_parameters['equation']  # either HE (HeatEquation) or HH (HelmHoltz)
        #self.equation = 'HH' # todo for dev!

        # calculate element matrices
        self.calc_elementmatrices()
        
        # assembly system matrices
        self.calc_system_matrices()

        # create force vector
        self.create_force_vector()

        # implement acoustic sources if helmholtz equation
        if self.equation =='HH':
            self.calculate_acoustic_sources()
            self.implement_acoustic_sources()

        # implement boundary conditions
        self.implement_boundary_conditions()

        # self.print_matrix(self.sysmatrix_diri)
        # self.print_matrix(self.force_vector_diri)
        # self.develop_print_input()
        # Solve the system
        self.solve_linear_system()

        # plot solution
        # self.plot_solution(self.solution, self.nodes_mesh_gen, self.triangulation)

        return self.solution

    def get_region_for_node_nbr(self, node):
        """
        Gets the region number for a node
        :param node:
        :return:
        """
        for key, val in self.triangulation_region_dict.items():
            if node in val:
                return key

    def implement_acoustic_sources(self):
        """
        Implements acoustic source, if any, into force vector for calculation Helmholtz equation
        :return:
        """
        for pos, val in self.acoustic_source:
            self.force_vector[pos] = self.force_vector[pos] + val



    def calculate_acoustic_sources(self):
        """
        calculates acoustic source values
        :return:
        """

        freq = float(self.calculation_parameters['freq'])
        omega = freq * 2 * math.pi

        self.acoustic_source = list()
        for node_nbr, vals in self.node_parameters.items():
            val_bc = vals['bc']['value']
            if val_bc:
                node_pos = self.single_nodes_dict[node_nbr]
                region_nbr = self.get_region_for_node_nbr(node_pos)
                rho = self.region_parameters[region_nbr]['material']['rho']
                mpsource = 4 * math.pi / rho * ((2 * rho * omega) / ((2 * math.pi) ** 2)) ** 0.5
                self.acoustic_source.append([node_pos, mpsource])



    def plot_solution_dev(self):
        """
        Plots the solution via matplotlib
        """
        solution = self.solution
        all_points = self.nodes_mesh_gen
        triangles = self.triangulation

        dataz = np.real(solution)
        values = dataz
        aspectxy = 1
        triang_mpl = tri.Triangulation(all_points[:, 0], all_points[:, 1], triangles)

        fig, ax = plt.subplots(figsize=(12, 8))

        units = self.calculation_parameters['units']
        ax.set_title('solution')
        ax.set_xlabel(f"x [{units}]")
        ax.set_ylabel(f"y [{units}]")
        ax.set_aspect(aspectxy)

        contour = ax.tricontourf(triang_mpl, values, cmap='viridis', levels=20)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.2)
        cbar = fig.colorbar(contour, cax=cax)

        ax.scatter(all_points[:, 0], all_points[:, 1], c=values, cmap='viridis', marker='.',
                             edgecolors='w', s=10)
        ax.triplot(triang_mpl, 'w-', linewidth=0.1)

        plt.show()

    @staticmethod
    def plot_solution(solution, all_points, triangles):
        """
        Plots the solution via matplotlib
        """


        dataz = np.real(solution)
        values = dataz
        aspectxy = 1
        triang_mpl = tri.Triangulation(all_points[:, 0], all_points[:, 1], triangles)

        fig, ax = plt.subplots(figsize=(12, 8))

        ax.set_title('solution')
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_aspect(aspectxy)

        contour = ax.tricontourf(triang_mpl, values, cmap='viridis', levels=20)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.2)
        cbar = fig.colorbar(contour, cax=cax)

        ax.scatter(all_points[:, 0], all_points[:, 1], c=values, cmap='viridis', marker='.',
                             edgecolors='w', s=10)
        ax.triplot(triang_mpl, 'w-', linewidth=0.1)

        plt.show()

    def solve_linear_system(self):

        self.solution = np.linalg.solve(self.sysmatrix_diri, self.force_vector_diri)
        # print(self.solution)

    def implement_boundary_conditions(self):
        """

        :return:
        """

        # create dirichlet list for implementation of dirichlet boundary conditions
        dirichlet_dict = dict()
        print(self.boundary_parameters)
        for boundary_nbr, params in self.boundary_parameters.items():
            bc = params['bc']
            bc_type = bc['type']
            bc_value = bc['value']
            bc_pos_nodes = self.boundary_nodes_dict[boundary_nbr]
            bc_pos = [elem[0] for elem in bc_pos_nodes]
            if bc_type == 'Dirichlet':
                for node in bc_pos:
                    try:
                        dirichlet_dict[node] = (dirichlet_dict[node] + bc_value) / 2
                    except KeyError:
                        dirichlet_dict[node] = bc_value
        dirichlet_list = np.array([[key, val] for key, val in dirichlet_dict.items()])

        if dirichlet_list:
            self.sysmatrix_diri, self.force_vector_diri = self.implement_dirichlet_condition(dirichlet_list, self.sysarray, self.force_vector)
        else:
            self.sysmatrix_diri, self.force_vector_diri = self.sysarray, self.force_vector

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

        return sysmatrix_adj, force_vector_adj


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
            # print(elesteifmat)
        if self.equation == 'HE':
            self.sysarray = self.syssteifarray
        elif self.equation == 'HH':  # todo: include in elementmatrices
            freq = float(self.calculation_parameters['freq'])
            omega = freq * 2 * math.pi
            self.sysarray = self.syssteifarray - omega**2 * self.sysmassarray


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
            p1, p2, p3 = int(triangle[0]), int(triangle[1]), int(triangle[2])
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
    calcfem.develop()  # read date via exec(!)
    calcfem.calc_fem()
    calcfem.plot_solution_dev()
    # calcfem.nodes_mesh_gen = [[0.5, 0.5], [0.,  0. ], [0.5, 0. ], [1.,  0. ], [1.,  0.5], [1.,  1. ], [0.5, 1. ], [0.,  1. ], [0.,  0.5], [1.,  1.5], [1.,  2. ], [0.5, 1.5]]
    # calcfem.single_nodes_dict = {'0': 1, '1': 3, '2': 5, '3': 7, '4': 10}
    # calcfem.boundary_nodes_dict = {'0': [[1, np.array([0., 0.])], [2, np.array([0.5, 0. ])], [3, np.array([1., 0.])]], '1': [[3, np.array([1., 0.])], [4, np.array([1. , 0.5])], [5, np.array([1., 1.])]], '2': [[5, np.array([1., 1.])], [6, np.array([0.5, 1. ])], [7, np.array([0., 1.])]], '3': [[7, np.array([0., 1.])], [8, np.array([0. , 0.5])], [1, np.array([0., 0.])]], '4': [[5, np.array([1., 1.])], [9, np.array([1. , 1.5])], [10, np.array([1., 2.])]], '5': [[10, np.array([1., 2.])], [11, np.array([0.5, 1.5])], [7, np.array([0., 1.])]]}
    # calcfem.triangulation = np.array([[2,4,0],[4,2,3],[4,6,0],[6,4,5],[8,2,0],[2,8,1],[6,8,0],[8,6,7],[6,11,7],[11,9,10],[6,9,11],[9,6,5]])
    # calcfem.triangulation_region_dict = {'0': range(0, 8), '1': range(8, 12)}
    # calcfem.calculation_parameters = {'mesh_density': 1, 'freq': None, 'equation': 'HE'}
    # calcfem.region_parameters = {
    #         '0': {'coordinates': [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)], 'area_neg_pos': 'Positive',
    #               'material'   : {'k': 1.0, 'c': 0, 'rho': 0}},
    #         '1': {'coordinates': [(0.0, 1.0), (1.0, 1.0), (1.0, 2.0)], 'area_neg_pos': 'Positive',
    #               'material'   : {'k': 3.0, 'c': 0, 'rho': 0}}}
    # calcfem.boundary_parameters = {'0': {'coordinates': [(0.0, 0.0), (1.0, 0.0)], 'bc': {'type': None, 'value': None}},
    #                             '1': {'coordinates': [(1.0, 0.0), (1.0, 1.0)], 'bc': {'type': None, 'value': None}},
    #                             '2': {'coordinates': [(1.0, 1.0), (0.0, 1.0)], 'bc': {'type': None, 'value': None}},
    #                             '3': {'coordinates': [(0.0, 1.0), (0.0, 0.0)],
    #                                   'bc'         : {'type': 'Dirichlet', 'value': 3.0}},
    #                             '4': {'coordinates': [(1.0, 1.0), (1.0, 2.0)],
    #                                   'bc'         : {'type': 'Dirichlet', 'value': 4.0}},
    #                             '5': {'coordinates': [(1.0, 2.0), (0.0, 1.0)], 'bc': {'type': None, 'value': None}}}
    # calcfem.node_parameters = {'0': {'coordinates': (0.5, 0.5), 'bc': {'type': None, 'value': None}},
    #                         '1': {'coordinates': (0.0, 0.0), 'bc': {'type': None, 'value': None}},
    #                         '2': {'coordinates': (1.0, 0.0), 'bc': {'type': None, 'value': None}},
    #                         '3': {'coordinates': (1.0, 1.0), 'bc': {'type': None, 'value': None}},
    #                         '4': {'coordinates': (0.0, 1.0), 'bc': {'type': None, 'value': None}},
    #                         '5': {'coordinates': (1.0, 2.0), 'bc': {'type': None, 'value': None}}}
    # calcfem.calculation_parameters = {'mesh_density': 1, 'freq': None, 'equation': 'HE'}

