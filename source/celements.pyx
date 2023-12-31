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
Definitions of elements for regions and boundaries
#######################################################################
"""

import numpy as np
from typing import Tuple, Union, List
from numpy import float64
import math
import warnings
warnings.filterwarnings("error", category=RuntimeWarning)

class ElementMatrices:
    """
    Collection of element matrices
    """
    def __init__(self):
        ...

    # @staticmethod
    # def calc_2d_triangular_heatflow_p1(conductivity: float, nodes: list) -> Tuple[np.array, None]:
    #     """
    #     Calculates element matrix for heat equation for order p and triangular elements
    #     :param conductivity: k
    #     :param nodes: [[x_1, y_1],[x_2, y_2],[x_3, y_3]]
    #     :return: np.array
    #     """
    #
    #     x_1 = nodes[0][0]
    #     y_1 = nodes[0][1]
    #     x_2 = nodes[1][0]
    #     y_2 = nodes[1][1]
    #     x_3 = nodes[2][0]
    #     y_3 = nodes[2][1]
    #     k = conductivity
    #
    #     val11 = -((k * (x_2 - x_3 - y_2 + y_3) ** 2) / (2 * (x_3 * (-y_1 + y_2)
    #                                                          + x_2 * (y_1 - y_3) + x_1 * (-y_2 + y_3))))
    #     val12 = (k * (-x_2 + x_3 + y_2 - y_3) * (x_1 - x_3 - y_1 + y_3)) / (
    #             2 * (x_3 * (y_1 - y_2) + x_1 * (y_2 - y_3) + x_2 * (-y_1 + y_3)))
    #     val13 = -((k * (x_1 - x_2 - y_1 + y_2) * (x_2 - x_3 - y_2 + y_3)) / (
    #             2 * (x_3 * (-y_1 + y_2) + x_2 * (y_1 - y_3) + x_1 * (-y_2 + y_3))))
    #     val21 = val12
    #     val22 = -((k * (x_1 - x_3 - y_1 + y_3) ** 2) / (2 * (x_3 * (-y_1 + y_2)
    #                                                          + x_2 * (y_1 - y_3) + x_1 * (-y_2 + y_3))))
    #     val23 = (k * (x_1 - x_2 - y_1 + y_2) * (x_1 - x_3 - y_1 + y_3)) / (
    #             2 * (x_3 * (-y_1 + y_2) + x_2 * (y_1 - y_3) + x_1 * (-y_2 + y_3)))
    #     val31 = val13
    #     val32 = val23
    #     val33 = -((k * (x_1 - x_2 - y_1 + y_2) ** 2) / (2 * (x_3 * (-y_1 + y_2) +
    #                                                          x_2 * (y_1 - y_3) + x_1 * (-y_2 + y_3))))
    #     stiffness_mat = np.array([[val11, val12, val13], [val21, val22, val23], [val31, val32, val33]], dtype=np.double)
    #
    #     mass_mat = None
    #
    #     return stiffness_mat, mass_mat


    @staticmethod
    def calc_2d_triangular_heatflow_p1(val_k: float, nodes: List[List[float]]) -> Tuple[np.array, np.array]:
        """
        Calculates element matrix for heat equation for order p and triangular elements
        :param nodes: [[x_1, y_1],[x_2, y_2],[x_3, y_3]]
        """

        def n1(xi1: float, xi2: float) -> float:
            """
            Calculates form function for node 1 and order 1 for triangular elements
            """

            return 1 - xi1 - xi2

        def n2(xi1: float, xi2: float) -> float:
            """
            Calculates form function for node 2 and order 1 for triangular elements
            """

            return xi1

        def n3(xi1: float, xi2: float) -> float:
            """
            Calculates form function for node 3 and order 1 for triangular elements
            """

            return xi2

        def ngrad1(xi1: float, xi2: float) -> np.array:
            """
            Calculates gradient of form function for node 1 and order 1 for triangular elements
            """

            return np.array([-1, -1], dtype=np.double)

        def ngrad2(xi1: float, xi2: float) -> np.array:
            """
            Calculates gradient of form function for node 2 and order 1 for triangular elements
            """

            return np.array([1, 0], dtype=np.double)

        def ngrad3(xi1: float, xi2: float) -> np.array:
            """
            Calculates gradient of form function for node 3 and order 1 for triangular elements
            """

            return np.array([0, 1], dtype=np.double)

        def gradmat(xi1: Union[np.array, float], xi2: Union[np.array, float],
                    x1: float, x2: float, x3: float, y1: float, y2: float, y3: float) -> np.array:
            """
            Calculates grad matrix for calculation of element stiffness matrices
            :return: np.array -> [[_, _],[_, _],[_, _]]
            """

            jacobi_inverse_transpose_matrix = np.array(
                [[(y1 - y3) / (x2 * y1 - x3 * y1 - x1 * y2 + x3 * y2 + x1 * y3 - x2 * y3),
                  (y1 - y2) / (x3 * (y1 - y2) + x1 * (y2 - y3) + x2 * (-y1 + y3))],
                 [(x1 - x3) / (x3 * (y1 - y2) + x1 * (y2 - y3) + x2 * (-y1 + y3)),
                  (x1 - x2) / (x2 * y1 - x3 * y1 - x1 * y2 + x3 * y2 + x1 * y3 - x2 * y3)]], dtype=np.double)
            ngrad = np.array([ngrad1(xi1, xi2), ngrad2(xi1, xi2),
                              ngrad3(xi1, xi2)], dtype=np.double)

            return np.transpose(np.dot(jacobi_inverse_transpose_matrix, np.transpose(ngrad)))

        def phiqequdistarray(xi1: Union[np.array, float], xi2: Union[np.array, float]) -> np.array:
            """
            Calculates matrix for calculation of element mass matrices
            :return: np.array -> [[_],[_],[_]]
            """

            return np.array([[n1(xi1, xi2)], [n2(xi1, xi2)], [n3(xi1, xi2)]], dtype=np.double)

        x_1 = nodes[0][0]
        y_1 = nodes[0][1]
        x_2 = nodes[1][0]
        y_2 = nodes[1][1]
        x_3 = nodes[2][0]
        y_3 = nodes[2][1]

        integration_nodes = np.array([[0, 0], [1, 0], [0, 1]])
        integration_weights = np.array([1 / 6, 1 / 6, 1 / 6])

        jacobi_det = -x_2 * y_1 + x_3 * y_1 + x_1 * y_2 - x_3 * y_2 - x_1 * y_3 + x_2 * y_3

        stiffness_mat = np.zeros((3, 3), dtype=np.double)
        for i in range(3):
            xi_1 = integration_nodes[i, 0]
            xi_2 = integration_nodes[i, 1]
            gr = gradmat(xi_1, xi_2, x_1, x_2, x_3, y_1, y_2, y_3)
            grt = np.transpose(gr)
            grxgrt = gr @ grt
            fp = grxgrt * jacobi_det * integration_weights
            stiffness_mat = stiffness_mat + fp
        stiffness_mat = stiffness_mat * val_k

        return stiffness_mat, None

    @staticmethod
    def calc_2d_triangular_acoustic_p1(val_c: float, val_rho: float, nodes: List[List[float64]]) -> Tuple[
        np.ndarray[np.ndarray[np.float64, np.intp], np.intp],
        np.ndarray[np.ndarray[np.float64, np.intp], np.intp]]:
        """
        Calculates element matrix for heat equation for order p and triangular elements
        todo: val_c und val_rho in Gleichungen fehlen!!!
        :param nodes: [[x_1, y_1],[x_2, y_2],[x_3, y_3]]
        """

        def n1(xi1: float, xi2: float) -> float:
            """
            Calculates form function for node 1 and order 1 for triangular elements
            """

            return 1 - xi1 - xi2

        def n2(xi1: float, xi2: float) -> float:
            """
            Calculates form function for node 2 and order 1 for triangular elements
            """

            return xi1

        def n3(xi1: float, xi2: float) -> float:
            """
            Calculates form function for node 3 and order 1 for triangular elements
            """

            return xi2

        def ngrad1(xi1: float, xi2: float) -> np.array:
            """
            Calculates gradient of form function for node 1 and order 1 for triangular elements
            """

            return np.array([-1, -1], dtype=np.double)

        def ngrad2(xi1: float, xi2: float) -> np.array:
            """
            Calculates gradient of form function for node 2 and order 1 for triangular elements
            """

            return np.array([1, 0], dtype=np.double)

        def ngrad3(xi1: float, xi2: float) -> np.array:
            """
            Calculates gradient of form function for node 3 and order 1 for triangular elements
            """

            return np.array([0, 1], dtype=np.double)

        def gradmat(xi1: float, xi2: float,
                    x1: float64, x2: float64, x3: float64, y1: float64, y2: float64, y3: float64) -> np.ndarray[np.ndarray[np.float64, np.intp], np.intp]:
            """
            Calculates grad matrix for calculation of element stiffness matrices
            :return: np.array -> [[_, _],[_, _],[_, _]]
            """

            jacobi_inverse_transpose_matrix = np.array(
                [[(y1 - y3) / (x2 * y1 - x3 * y1 - x1 * y2 + x3 * y2 + x1 * y3 - x2 * y3),
                  (y1 - y2) / (x3 * (y1 - y2) + x1 * (y2 - y3) + x2 * (-y1 + y3))],
                 [(x1 - x3) / (x3 * (y1 - y2) + x1 * (y2 - y3) + x2 * (-y1 + y3)),
                  (x1 - x2) / (x2 * y1 - x3 * y1 - x1 * y2 + x3 * y2 + x1 * y3 - x2 * y3)]], dtype=np.double)
            ngrad = np.array([ngrad1(xi1, xi2), ngrad2(xi1, xi2),
                              ngrad3(xi1, xi2)], dtype=np.double)

            return np.transpose(np.dot(jacobi_inverse_transpose_matrix, np.transpose(ngrad)))

        def phiqequdistarray(xi1: float, xi2: float) -> np.ndarray[np.ndarray[np.float64, np.intp], np.intp]:
            """
            Calculates matrix for calculation of element mass matrices
            :return: np.array -> [[_],[_],[_]]
            """

            return np.array([[n1(xi1, xi2)], [n2(xi1, xi2)], [n3(xi1, xi2)]], dtype=np.double)

        x_1 = nodes[0][0]
        y_1 = nodes[0][1]
        x_2 = nodes[1][0]
        y_2 = nodes[1][1]
        x_3 = nodes[2][0]
        y_3 = nodes[2][1]

        integration_nodes = np.array([[0, 0], [1, 0], [0, 1]])
        integration_weights = np.array([1 / 6, 1 / 6, 1 / 6])

        jacobi_det = -x_2 * y_1 + x_3 * y_1 + x_1 * y_2 - x_3 * y_2 - x_1 * y_3 + x_2 * y_3

        stiffness_mat = np.zeros((3, 3), dtype=np.double)
        for i in range(3):
            xi_1 = float(integration_nodes[i, 0])
            xi_2 = float(integration_nodes[i, 1])
            gr = gradmat(xi_1, xi_2, x_1, x_2, x_3, y_1, y_2, y_3)
            grt = np.transpose(gr)
            grxgrt = gr @ grt
            fp = grxgrt * jacobi_det * integration_weights
            stiffness_mat = stiffness_mat + fp

        mass_mat = np.zeros((3, 3), dtype=np.double)
        for i in range(3):
            xi_1 = integration_nodes[i, 0]
            xi_2 = integration_nodes[i, 1]
            phi = phiqequdistarray(xi_1, xi_2)
            phit = np.transpose(phiqequdistarray(xi_1, xi_2))
            phixphit = phi @ phit
            fp = phixphit * jacobi_det * integration_weights
            mass_mat = mass_mat + fp

        stiffness_mat = stiffness_mat * 1/val_rho
        mass_mat = mass_mat * 1/val_rho * 1/(val_c**2)
        return stiffness_mat, mass_mat

    @staticmethod
    def calc_2d_triangular_acoustic_p1_simp(val_c: float, val_rho: float, nodes: List[List[float64]]) -> Tuple[
        np.ndarray[np.ndarray[np.float64, np.intp], np.intp],
        np.ndarray[np.ndarray[np.float64, np.intp], np.intp]]:
        """
        Calculates element matrix for heat equation for order p and triangular elements
        todo: val_c und val_rho in Gleichungen fehlen!!!
        :param nodes: [[x_1, y_1],[x_2, y_2],[x_3, y_3]]
        """
        x1 = nodes[0][0]
        y1 = nodes[0][1]
        x2 = nodes[1][0]
        y2 = nodes[1][1]
        x3 = nodes[2][0]
        y3 = nodes[2][1]

        # entries stiffnessmat
        try:
            eq11 = -((x2 ** 2 - 2 * x2 * x3 + x3 ** 2 + (y2 - y3) ** 2) / (
                        2 * val_rho * (x3 * (-y1 + y2) + x2 * (y1 - y3) + x1 * (-y2 + y3))))
            eq12 = (x1 * (x2 - x3) - x2 * x3 + x3 ** 2 + y1 * y2 - y1 * y3 - y2 * y3 + y3 ** 2) / (
                        2 * val_rho * (x3 * (-y1 + y2) + x2 * (y1 - y3) + x1 * (-y2 + y3)))
            eq13 = (x2 ** 2 - x2 * x3 + x1 * (-x2 + x3) - (y1 - y2) * (y2 - y3)) / (
                        2 * val_rho * (x3 * (-y1 + y2) + x2 * (y1 - y3) + x1 * (-y2 + y3)))
            eq21 = eq12
            eq22 = -((x1 ** 2 - 2 * x1 * x3 + x3 ** 2 + (y1 - y3) ** 2) / (
                        2 * val_rho * (x3 * (-y1 + y2) + x2 * (y1 - y3) + x1 * (-y2 + y3))))
            eq23 = (x1 ** 2 + x2 * x3 - x1 * (x2 + x3) + (y1 - y2) * (y1 - y3)) / (
                        2 * val_rho * (x3 * (-y1 + y2) + x2 * (y1 - y3) + x1 * (-y2 + y3)))
            eq31 = eq13
            eq32 = eq23
            eq33 = -((x1 ** 2 - 2 * x1 * x2 + x2 ** 2 + (y1 - y2) ** 2) / (
                        2 * val_rho * (x3 * (-y1 + y2) + x2 * (y1 - y3) + x1 * (-y2 + y3))))
        except RuntimeWarning as rw:
            print(f"RuntimeWarning for element {nodes}: {rw}\n"
                  f"Warning: Elementmatrix set to 0 -> Errors in Solution!")
            eq11 = 0
            eq12 = 0
            eq13 = 0
            eq21 = 0
            eq22 = 0
            eq23 = 0
            eq31 = 0
            eq32 = 0
            eq33 = 0
        stiffness_mat = np.array([[eq11, eq12, eq13], [eq21, eq22, eq23], [eq31, eq32, eq33]])

        # entries massmat
        eq11 = (x3 * (y1 - y2) + x1 * (y2 - y3) + x2 * (-y1 + y3)) / (6 * val_c ** 2 * val_rho)
        eq12 = 0
        eq13 = 0
        eq21 = 0
        eq22 = (x3 * (y1 - y2) + x1 * (y2 - y3) + x2 * (-y1 + y3)) / (6 * val_c ** 2 * val_rho)
        eq23 = 0
        eq31 = 0
        eq32 = 0
        eq33 = (x3 * (y1 - y2) + x1 * (y2 - y3) + x2 * (-y1 + y3)) / (6 * val_c ** 2 * val_rho)
        mass_mat = np.array([[eq11, eq12, eq13], [eq21, eq22, eq23], [eq31, eq32, eq33]])

        return stiffness_mat, mass_mat

    @staticmethod
    def calc_2d_triangular_heatflow_p1_simp(val_k: float, nodes: List[List[float]]) -> Tuple[np.array, np.array]:
        """
        Calculates element matrix for heat equation for order p and triangular elements
        :param nodes: [[x_1, y_1],[x_2, y_2],[x_3, y_3]]
        """
        x1 = nodes[0][0]
        y1 = nodes[0][1]
        x2 = nodes[1][0]
        y2 = nodes[1][1]
        x3 = nodes[2][0]
        y3 = nodes[2][1]

        # entries stiffnessmat
        try:
            eq11 = -(val_k * (x2 ** 2 - 2 * x2 * x3 + x3 ** 2 + (y2 - y3) ** 2)) / (
                        2 * (x3 * (-y1 + y2) + x2 * (y1 - y3) + x1 * (-y2 + y3)))
            eq12 = (val_k * (x1 * (x2 - x3) - x2 * x3 + x3 ** 2 + y1 * y2 - y1 * y3 - y2 * y3 + y3 ** 2)) / (
                        2 * (x3 * (-y1 + y2) + x2 * (y1 - y3) + x1 * (-y2 + y3)))
            eq13 = (val_k * (x2 ** 2 - x2 * x3 + x1 * (-x2 + x3) - (y1 - y2) * (y2 - y3))) / (
                        2 * (x3 * (-y1 + y2) + x2 * (y1 - y3) + x1 * (-y2 + y3)))
            eq21 = eq12
            eq22 = -(val_k * (x1 ** 2 - 2 * x1 * x3 + x3 ** 2 + (y1 - y3) ** 2)) / (
                        2 * (x3 * (-y1 + y2) + x2 * (y1 - y3) + x1 * (-y2 + y3)))
            eq23 = (val_k * (x1 ** 2 + x2 * x3 - x1 * (x2 + x3) + (y1 - y2) * (y1 - y3))) / (
                        2 * (x3 * (-y1 + y2) + x2 * (y1 - y3) + x1 * (-y2 + y3)))
            eq31 = eq13
            eq32 = eq23
            eq33 = -(val_k * (x1 ** 2 - 2 * x1 * x2 + x2 ** 2 + (y1 - y2) ** 2)) / (
                        2 * (x3 * (-y1 + y2) + x2 * (y1 - y3) + x1 * (-y2 + y3)))
        except RuntimeWarning as rw:
            print(f"RuntimeWarning for element {nodes}: {rw}\n"
                  f"Warning: Elementmatrix set to 0 -> Errors in Solution!")
            eq11 = 0
            eq12 = 0
            eq13 = 0
            eq21 = 0
            eq22 = 0
            eq23 = 0
            eq31 = 0
            eq32 = 0
            eq33 = 0
        stiffness_mat = np.array([[eq11, eq12, eq13], [eq21, eq22, eq23], [eq31, eq32, eq33]])

        return stiffness_mat, None

    @staticmethod
    def boundary_element_p1(nodes: list, bc_std_a: float, bc_std_b: float, bc_std_g: float) -> np.array:
        """
        todo: transformation for inclined boundary correct / necessary?

        value_A: input from self.boundary_parameters[...]['bc']['value'] -> Value from Tuple[0] for Robin BC, Value for Neumann BC
        value_B: input from self.boundary_parameters[...]['bc']['value'] -> Value from Tuple[1] for Robin BC, None for Neumann BC
        value_C: corresponding Materials parameter, e.g. k for HE, placeholder, currently not necessary
        Creates boundary element (e.g. for impedance)
        :param nodes: [[x_1, y_1],[x_2, y_2]]
        :param value: value for the boundary element
        :return:
        """

        def phi_p1(node: int, xi: float):
            """
            form function for 1D line element
            :param node: node for formfunction
            :param xi:
            :return:
            """

            node = int(node)
            if node == 1:
                f = 1.0 - xi
            elif node == 2:
                f = xi

            return f

        def phi_grad_p1(node: int, xi: float):
            """
            form function for 1D line element
            todo: transformation for inclined boundary correct?
            :param node: node for formfunction
            :param xi:
            :return:
            """

            node = int(node)
            if node == 1:
                f = - 1
            elif node == 2:
                f = 1

            return f

        numintgld1 = np.array([[0.21132486, 0.78867513], [0.50000000, 0.50000000]],
                              dtype=np.double)
        intnodes = numintgld1[0]
        intweights = numintgld1[1]

        x_1 = nodes[0][0]
        y_1 = nodes[0][1]
        x_2 = nodes[1][0]
        y_2 = nodes[1][1]

        # get length and angle of element
        delta_x = x_2 - x_1
        delta_y = y_2 - y_1
        angle = math.atan2(delta_y, delta_x)  # angle between horizontal axis and boundary
        angle = (angle + 2 * math.pi) % (2 * math.pi)  # angle cant be greater than 360°
        length = math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)  # length of boundary

        # calculate element matrix
        element_mat = np.zeros((2, 2), dtype=np.double)
        nb = np.zeros((2, 2))
        for j in range(0, 2):
            for i in range(0, 2):
                for ii in range(0, 2):
                    val = phi_p1(i + 1, intnodes[j]) * phi_p1(ii + 1, intnodes[j]) * intweights[j]
                    nb[i, ii] = val
            element_mat = element_mat + nb
        element_mat = element_mat * length * bc_std_a

        # calculate contribution to force vector, convective part
        force_vector_mat_conv = np.zeros((2, 1), dtype=np.double)
        nb = np.zeros((2, 1))
        for j in range(0, 2):
            for i in range(0, 2):
                val = phi_p1(i + 1, intnodes[j]) * intweights[j]
                nb[i, 0] = val
            force_vector_mat_conv = force_vector_mat_conv + nb
        force_vector_mat_conv = force_vector_mat_conv * length * bc_std_g

        # calculate contribution to force vector, conductive part
        # force_vector_mat_cond = np.zeros((2, 1), dtype=np.double)
        # nb = np.zeros((2, 1))
        # for j in range(0, 2):
        #     for i in range(0, 2):
        #         val = phi_grad_p1(i + 1, intnodes[j]) * phi_p1(i + 1, intnodes[j]) * intweights[j]
        #         nb[i, 0] = val
        #     force_vector_mat_cond = force_vector_mat_cond + nb
        # force_vector_mat_cond = force_vector_mat_cond * length * value_B

        force_vector_mat = force_vector_mat_conv

        # transform element to angle
        # transformation_matrix = np.array([[math.cos(angle), -1 * math.sin(angle)],
        #                                   [math.sin(angle), math.cos(angle)]])
        # transformed_element = transformation_matrix @ element_mat

        return element_mat, force_vector_mat


if __name__ == "__main__":
    # Example output
    nodes_element = [[0, 0], [1.1, -0.1], [0.5, 0.6]]
    nodes_boundary = [[0, 0], [0.5, 0]]
    bc_val_a = 0.5
    bc_val_b = 0.25
    bc_val_g = 2
    k = 0.5
    c = 330.0
    rho = 1.21
    elements = ElementMatrices()
    stiffness_heat_flow_p1, mass_heat_flow_p1 = elements.calc_2d_triangular_heatflow_p1(k, nodes_element)
    stiffness_heat_flow_p1_simp, mass_heat_flow_p1_simp = elements.calc_2d_triangular_heatflow_p1_simp(k, nodes_element)
    stiffness_acoustic_flow_p1, mass_acoustic_flow_p1 = elements.calc_2d_triangular_acoustic_p1(c, rho, nodes_element)
    stiffness_acoustic_flow_p1_simp, mass_acoustic_flow_p1_simp = elements.calc_2d_triangular_acoustic_p1_simp(c, rho, nodes_element)
    boundary_element = elements.boundary_element_p1(nodes_boundary, bc_val_a, bc_val_b, bc_val_g)
    print(f"Heat flow element, p = 1: \n{stiffness_heat_flow_p1}\n{mass_heat_flow_p1}")
    print(f"Heat flow element, p = 1: \n{stiffness_heat_flow_p1_simp}\n{mass_heat_flow_p1_simp}")
    print(f"\nAcoustic element, p = 1: \n{stiffness_acoustic_flow_p1}\n{mass_acoustic_flow_p1}")
    print(f"\nAcoustic element, p = 1: \n{stiffness_acoustic_flow_p1_simp}\n{mass_acoustic_flow_p1_simp}")
    print(f"\nBoundary element, p = 1: \n{boundary_element}")
