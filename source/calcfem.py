"""
#######################################################################
LICENSE INFORMATION
This file is part of TinyFEM.

TinyFEM is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

TinyFEM is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with TinyFEM. If not, see <https://www.gnu.org/licenses/>.
#######################################################################

#######################################################################
Description:
File performs FEM calculations.
#######################################################################
"""


from scipy.interpolate import griddata
import numpy as np
#from source.celements import ElementMatrices  # little bit of improvement (10%)
from source.elements import ElementMatrices
import matplotlib.tri as tri
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import math
from typing import List, Tuple, Union
from scipy.sparse import coo_matrix
import copy
from source.guistatics import GUIStatics
import matplotlib  # delete later, only used for development in matplotlib.use('Qt5Agg')
import time
import scipy.sparse as sp
from scipy.sparse.linalg import spsolve
from scipy.sparse import csc_matrix

time_it_dict = dict()

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Call the original function
        end_time = time.time()  # Record the end time
        execution_time = end_time - start_time
        try:
            time_it_dict[func.__name__] += execution_time
        except KeyError:
            time_it_dict[func.__name__] = execution_time
        return result
    return wrapper

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

        # von GUI übergebene Werte aus Boundary/Materials/Calculation Definition
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
        self.boundaries_incidence_matrix = None  # Incidence matrix for boundary elements
        self.all_boundary_elements = None  # list contains all boundary element matrices
        self.sysboundaries = None  # Boundary matrix e.g. impedance matrix for system

        # development
        self.file_path_dev = r'K:/OneDrive/Science/PyCharmProjects/tinyfem/testing/output_gui_4_calcfem_' + '14' + '.txt'

    @timing_decorator
    def calc_fem(self):
        """
        main method for calculation, calculates elementmatrices, assembly of system matrices,
        implements boundary conditions, solves linear system
        :return:
        """

        # set equation
        self.equation = self.calculation_parameters['equation']  # either HE (HeatEquation) or HH (HelmHoltz)

        ########################################################################
        # Raw System matrix and force vector (without any boundary conditions)
        # calculate element matrices
        self.calc_elementmatrices()

        # initialize force vector
        self.create_force_vector()

        # assembly system matrices
        self.calc_system_matrices_init()

        # -> self.force_vector | self.syssteifarray | self.sysmassarray
        ########################################################################

        ########################################################################
        # calculate boundary elements for system matrix and frore vector
        self.calc_boundary_elements()

        # assembly boundary system matrix
        self.assembly_system_matrix_boundaries()

        # -> self.sysboundaries                         system boundary matrix with Neumann/Robin BCs
        # -> self.allboundary_elements_forcevektor      positions and values added to force vector for robin bc
        ########################################################################

        ########################################################################
        # Systemmatrix and force vector with added Neumann/Robin BCs
        # implement Neumann/robin into raw system matrix
        self.calc_system_matrices_robin_neumann_bc()

        # # implement acoustic sources if helmholtz equation
        if self.equation =='HH':
            self.calculate_acoustic_sources()
            self.implement_acoustic_sources()

        # # implement robin boundary condition in force vector
        self.implement_robin_force_vector()

        # -> self.sysarray_neumann_robin        System matrix with implemented neumann /robin BCs
        # -> self.force_vector_neumann_robin    Force vector with implemented neumann/robin Bcs
        ########################################################################

        ########################################################################
        # implement dirichlet boundary conditions
        self.implement_dirichlet_boundary_conditions()

        # -> self.sysmatrix_diri | self.force_vector_diri
        ########################################################################

        ########################################################################
        # solve system
        #self.develop_print_input()
        self.print_matrix(self.sysmatrix_diri)
        self.solve_linear_system()

        ########################################################################

        ########################################################################
        # # plot solution
        # # self.plot_solution(self.solution, self.nodes_mesh_gen, self.triangulation)

        # self.print_solution_nodes()  # for dev
        return self.solution
        ########################################################################

    @timing_decorator
    def calc_system_matrices_robin_neumann_bc(self):
        """

        :return:
        """

        if self.equation == 'HE':
            self.sysarray_neumann_robin = self.syssteifarray + self.sysboundaries
        elif self.equation == 'HH':  # todo: include in elementmatrices
            freq = float(self.calculation_parameters['freq'])
            omega = freq * 2 * math.pi
            self.sysarray_neumann_robin = self.syssteifarray - omega ** 2 * self.sysmassarray + omega * 1j * self.sysboundaries


        # Sparse takes longer...
        # syssteif_s = csc_matrix(self.syssteifarray)
        # sysmass_s = csc_matrix(self.sysmassarray)
        # sysbound_s = csc_matrix(self.sysboundaries)
        #
        # if self.equation == 'HE':
        #     self.sysarray_neumann_robin = (syssteif_s + sysbound_s).toarray()
        # elif self.equation == 'HH':  # todo: include in elementmatrices
        #     freq = float(self.calculation_parameters['freq'])
        #     omega = freq * 2 * math.pi
        #     self.sysarray_neumann_robin = (syssteif_s - omega ** 2 * sysmass_s + omega * 1j * sysbound_s).toarray()


    @timing_decorator
    def calc_boundary_elements(self):
        """
        calculates the boundary elements for neumann / robin BC
        todo: Vermutlich muss hier noch Vorzeichen geändert werden abhängig davon ob normalenvektor in Region zeigt oder aus Region raus...?!?
        :return:
        """

        self.boundaries_incidence_matrix = list()  # contains incidence matrix for assembly boundary elements for addition to systemmatrix
        self.all_boundary_elements = list()  # contains boundary elements for implementation in systemmatrx
        self.allboundary_elements_forcevektor = list()  # contains the contributions to the force vector for robin bcs -> [[pos],[values]]
        bc_val_A, bc_val_B, bc_val_C = None, None, None
        for bc_nbr, vals in self.boundary_parameters.items():
            bc_type = vals['bc']['type']
            if bc_type == 'Neumann':
                bc_val_A = vals['bc']['value']
                if self.equation == 'HH':
                    try:
                        bc_val_A = 1 / bc_val_A  # neumann value is 1/Z
                    except ZeroDivisionError:
                        bc_val_A = 10e10
                bc_val_B = 0
            elif bc_type == 'Robin':
                bc_val_A = vals['bc']['value'][0]
                bc_val_B = vals['bc']['value'][1]
            if bc_type in {'Neumann', 'Robin'}:
                bc_nodes = self.boundary_nodes_dict[bc_nbr]
                bc_node_mid = self.boundary_nodes_dict[bc_nbr][1][0]  # since every boundary has at least 3 nodes -> node 1 to determine which region boundary belongs to
                region = self.get_region_for_node_nbr(bc_node_mid)
                mats = self.region_parameters[region]['material']
                if self.equation == 'HE':
                    bc_val_C = mats['k']
                    # transform values A, B, C into standard ROBIN form
                    bc_std_a = bc_val_B  # corresponds to h
                    bc_std_b = bc_val_C  # corresponds to k
                    bc_std_g = bc_val_B * bc_val_A  # corresponds to h * T_ext
                elif self.equation == 'HH':
                    # transform values A, B, C into standard ROBIN form
                    bc_std_a = bc_val_A  # only impedance implemented
                    bc_std_b = 0  # only impedance
                    bc_std_g = 0  # only impedance
                for e0, e1 in zip(bc_nodes[:-1], bc_nodes[1:]):
                    self.boundaries_incidence_matrix.append([e0[0], e1[0]])
                    boundary_element_matrix, force_vector_matrix = ElementMatrices.boundary_element_p1([e0[1], e1[1]], bc_std_a, bc_std_b, bc_std_g)
                    self.all_boundary_elements.append(boundary_element_matrix)
                    if bc_type == 'Robin':
                        #self.allboundary_elements_forcevektor.append([[e0[0], e1[0]], force_vector_matrix])
                        self.allboundary_elements_forcevektor.append([e0[0], force_vector_matrix[0][0]])  # todo, only works for p=1
                        self.allboundary_elements_forcevektor.append([e1[0], force_vector_matrix[1][0]])

    @timing_decorator
    def assembly_system_matrix_boundaries(self):
        """
        Assembles the system boundaries matrix e.g. for impedance of boundaries
        :return:
        """
        maxnode = len(self.nodes_mesh_gen)
        nbr_of_elements = len(self.all_boundary_elements)
        alloc_mat = np.array(self.boundaries_incidence_matrix)
        self.sysboundaries = np.zeros((maxnode, maxnode), dtype=np.double)

        for ielem in range(nbr_of_elements):
            boundary_mat = self.all_boundary_elements[ielem]
            for a in range(2):
                for b in range(2):
                    zta = int(alloc_mat[ielem, a])
                    ztb = int(alloc_mat[ielem, b])
                    self.sysboundaries[zta, ztb] = self.sysboundaries[zta, ztb] + boundary_mat[a, b]

    @timing_decorator
    def implement_robin_force_vector(self):
        """

        :return:
        """

        self.force_vector_neumann_robin = np.copy(self.force_vector)

        for idx, elem in enumerate(self.allboundary_elements_forcevektor):
            pos = elem[0]
            value = elem[1]
            self.force_vector_neumann_robin[pos] = self.force_vector_neumann_robin[pos] + value

    @timing_decorator
    def implement_acoustic_sources(self):
        """
        Implements acoustic source, if any, into force vector for calculation Helmholtz equation
        :return:
        """
        for pos, val in self.acoustic_source:
            self.force_vector[pos] = self.force_vector[pos] + val

    @timing_decorator
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

    @timing_decorator
    def implement_dirichlet_boundary_conditions(self):
        """

        :return:
        """

        # create dirichlet list for implementation of dirichlet boundary conditions
        dirichlet_dict = dict()
        for boundary_nbr, params in self.boundary_parameters.items():  # Todo: Für C6 ist hier ein Fehler bei der Ermittlung der zugehörigen Knoten zu einem Boundary, vermutlich bei Netzerstellung...
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
        dirichlet_list = [[key, val] for key, val in dirichlet_dict.items()]

        if dirichlet_list:
            dirichlet_list = np.array(dirichlet_list)
            self.sysmatrix_diri, self.force_vector_diri = self.implement_dirichlet_condition(dirichlet_list, self.sysarray_neumann_robin, self.force_vector_neumann_robin)
        else:  # no dirichlet conditions specified
            self.sysmatrix_diri, self.force_vector_diri = self.sysarray_neumann_robin, self.force_vector_neumann_robin


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
        # CalcFEM.print_matrix(force_vector_adj)

        return sysmatrix_adj, force_vector_adj

    @timing_decorator
    def solve_linear_system(self):
        """

        :return:
        """
        print(f"Solving system...")
        sysmat = sp.csr_matrix(self.sysmatrix_diri)
        forcevec = self.force_vector_diri
        self.solution = spsolve(sysmat, forcevec)

    @timing_decorator
    def create_force_vector(self):
        maxnode = len(self.nodes_mesh_gen)
        self.force_vector = np.zeros(maxnode, dtype=np.double)

    @timing_decorator
    def calc_system_matrices_init(self):
        """

        :return:
        """
        maxnode = len(self.nodes_mesh_gen)
        nbr_of_elements = len(self.triangulation)
        alloc_mat = self.triangulation
        self.syssteifarray = np.zeros((maxnode, maxnode), dtype=np.double)
        self.sysmassarray = np.zeros((maxnode, maxnode), dtype=np.double)
        self.sysarray = np.zeros((maxnode, maxnode), dtype=np.double)

        for ielem in range(nbr_of_elements):
            elesteifmat = self.all_element_matrices_steif[ielem]
            elemassmat = self.all_element_matrices_mass[ielem]
            for a in range(3):
                for b in range(3):
                    zta = int(alloc_mat[ielem, a])
                    ztb = int(alloc_mat[ielem, b])
                    self.syssteifarray[zta, ztb] = self.syssteifarray[zta, ztb] + elesteifmat[a, b]
                    self.sysmassarray[zta, ztb] = self.sysmassarray[zta, ztb] + elemassmat[a, b]

    @timing_decorator
    def calc_elementmatrices(self):
        """

        :return:
        """

        @timing_decorator
        def get_region_number(idx: int):
            """

            :param idx:
            :return:
            """
            for region, triangles in self.triangulation_region_dict.items():
                if idx in triangles:
                    return region

        nbr_of_elements = len(self.triangulation)

        self.all_element_matrices_steif = np.zeros((nbr_of_elements, 3, 3), dtype=np.double)
        self.all_element_matrices_mass = np.zeros((nbr_of_elements, 3, 3), dtype=np.double)

        elemsteif = None
        elemmass = None
        print(f"Calculating element matrices...")
        for idx, triangle in enumerate(self.triangulation):
            print(f"{idx} / {len(self.triangulation)}", end='\r')  # This does not show in pycharm, only via cmd / .exe
            b_region = get_region_number(idx)
            materials = self.region_parameters[b_region]['material']
            k = float(materials['k'])
            c = float(materials['c'])
            rho = float(materials['rho'])
            p1, p2, p3 = int(triangle[0]), int(triangle[1]), int(triangle[2])
            x1 = self.nodes_mesh_gen[p1][0]
            y1 = self.nodes_mesh_gen[p1][1]
            x2 = self.nodes_mesh_gen[p2][0]
            y2 = self.nodes_mesh_gen[p2][1]
            x3 = self.nodes_mesh_gen[p3][0]
            y3 = self.nodes_mesh_gen[p3][1]
            nodes = [[x1, y1], [x2, y2], [x3, y3]]
            if self.equation == 'HE':
                elemsteif, elemmass = ElementMatrices.calc_2d_triangular_heatflow_p1_simp(k, nodes)
            elif self.equation == 'HH':
                elemsteif, elemmass = ElementMatrices.calc_2d_triangular_acoustic_p1_simp(c, rho, nodes)
            self.all_element_matrices_steif[idx] = elemsteif
            if elemmass is not None:  # since it might be a np.array
                self.all_element_matrices_mass[idx] = elemmass

    @timing_decorator
    def get_region_for_node_nbr(self, node):
        """
        Gets the region number for a node
        :param node:
        :return:
        """
        for key, val in self.triangulation_region_dict.items():
            if node in val:
                return key

    @timing_decorator
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

    def plot_solution_dev2(self):
        solution = self.solution
        all_points = self.nodes_mesh_gen

        x = all_points[:, 0]
        y = all_points[:, 1]
        z = solution
        contour = plt.tricontourf(x, y, z, levels=20, cmap='viridis')

        plt.xlabel("X-axis Label")
        plt.ylabel("Y-axis Label")
        plt.title("Contour Plot Example")
        plt.colorbar(contour)  # Add a colorbar for reference
        plt.show()

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

        contour = ax.tricontourf(triang_mpl, values, cmap='viridis', levels=50)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.2)
        cbar = fig.colorbar(contour, cax=cax)

        ax.scatter(all_points[:, 0], all_points[:, 1], c=values, cmap='viridis', marker='.',
                             edgecolors='w', s=10)
        ax.triplot(triang_mpl, 'w-', linewidth=0.1)

        plt.show()

    def print_solution_nodes(self, gap=1, setx=None, sety=None):
        """
        prints nodes and their solution, can ge a gap...
        :return:
        """
        nodes = self.nodes_mesh_gen
        sol_nodes = np.column_stack((self.nodes_mesh_gen, self.solution))
        print(f"N: {'x:'.ljust(10)}  {'y:'.ljust(10)}  {'sol:'.ljust(10)}")
        for n, (x, y, sol) in enumerate(sol_nodes[::gap]):
            if not setx and not sety:
                print(f"{n}  {str(x).ljust(10)}  {str(y).ljust(10)}  {str(sol).ljust(10)}")
            elif not sety:
                if x == setx:
                    print(f"{n}  {str(x).ljust(10)}  {str(y).ljust(10)}  {str(sol).ljust(10)}")
            elif not setx:
                if y == sety:
                    print(f"{n}  {str(x).ljust(10)}  {str(y).ljust(10)}  {str(sol).ljust(10)}")


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
    matplotlib.use('TkAgg')
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
    # timing for dev:
    print(f"\nTotal execution time          : {time_it_dict['calc_fem']:.4f}")

    print(f"\nTiming of functions: ")
    time_it_dict = dict(sorted(time_it_dict.items(), key=lambda x: x[1]))
    for func, exectime in time_it_dict.items():
        print(f"{str(func)[:29].ljust(30)}: {exectime:.4f}")
