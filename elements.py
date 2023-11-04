import numpy as np
from typing import Tuple, Union
import math

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
    #     stiffness_mat = np.array([[val11, val12, val13], [val21, val22, val23], [val31, val32, val33]], dtype=np.single)
    #
    #     mass_mat = None
    #
    #     return stiffness_mat, mass_mat

    @staticmethod
    def calc_2d_triangular_heatflow_p1(val_k: float, nodes: list) -> Tuple[np.array, np.array]:
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

            return np.array([-1, -1], dtype=np.single)

        def ngrad2(xi1: float, xi2: float) -> np.array:
            """
            Calculates gradient of form function for node 2 and order 1 for triangular elements
            """

            return np.array([1, 0], dtype=np.single)

        def ngrad3(xi1: float, xi2: float) -> np.array:
            """
            Calculates gradient of form function for node 3 and order 1 for triangular elements
            """

            return np.array([0, 1], dtype=np.single)

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
                  (x1 - x2) / (x2 * y1 - x3 * y1 - x1 * y2 + x3 * y2 + x1 * y3 - x2 * y3)]], dtype=np.single)
            ngrad = np.array([ngrad1(xi1, xi2), ngrad2(xi1, xi2),
                              ngrad3(xi1, xi2)], dtype=np.single)

            return np.transpose(np.dot(jacobi_inverse_transpose_matrix, np.transpose(ngrad)))

        def phiqequdistarray(xi1: Union[np.array, float], xi2: Union[np.array, float]) -> np.array:
            """
            Calculates matrix for calculation of element mass matrices
            :return: np.array -> [[_],[_],[_]]
            """

            return np.array([[n1(xi1, xi2)], [n2(xi1, xi2)], [n3(xi1, xi2)]], dtype=np.single)

        x_1 = nodes[0][0]
        y_1 = nodes[0][1]
        x_2 = nodes[1][0]
        y_2 = nodes[1][1]
        x_3 = nodes[2][0]
        y_3 = nodes[2][1]

        integration_nodes = np.array([[0, 0], [1, 0], [0, 1]])
        integration_weights = np.array([1 / 6, 1 / 6, 1 / 6])

        jacobi_det = -x_2 * y_1 + x_3 * y_1 + x_1 * y_2 - x_3 * y_2 - x_1 * y_3 + x_2 * y_3

        stiffness_mat = np.zeros((3, 3), dtype=np.single)
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
    def calc_2d_triangular_acoustic_p1(val_c: float, val_rho: float, nodes: list) -> Tuple[np.array, np.array]:
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

            return np.array([-1, -1], dtype=np.single)

        def ngrad2(xi1: float, xi2: float) -> np.array:
            """
            Calculates gradient of form function for node 2 and order 1 for triangular elements
            """

            return np.array([1, 0], dtype=np.single)

        def ngrad3(xi1: float, xi2: float) -> np.array:
            """
            Calculates gradient of form function for node 3 and order 1 for triangular elements
            """

            return np.array([0, 1], dtype=np.single)

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
                  (x1 - x2) / (x2 * y1 - x3 * y1 - x1 * y2 + x3 * y2 + x1 * y3 - x2 * y3)]], dtype=np.single)
            ngrad = np.array([ngrad1(xi1, xi2), ngrad2(xi1, xi2),
                              ngrad3(xi1, xi2)], dtype=np.single)

            return np.transpose(np.dot(jacobi_inverse_transpose_matrix, np.transpose(ngrad)))

        def phiqequdistarray(xi1: Union[np.array, float], xi2: Union[np.array, float]) -> np.array:
            """
            Calculates matrix for calculation of element mass matrices
            :return: np.array -> [[_],[_],[_]]
            """

            return np.array([[n1(xi1, xi2)], [n2(xi1, xi2)], [n3(xi1, xi2)]], dtype=np.single)

        x_1 = nodes[0][0]
        y_1 = nodes[0][1]
        x_2 = nodes[1][0]
        y_2 = nodes[1][1]
        x_3 = nodes[2][0]
        y_3 = nodes[2][1]

        integration_nodes = np.array([[0, 0], [1, 0], [0, 1]])
        integration_weights = np.array([1 / 6, 1 / 6, 1 / 6])

        jacobi_det = -x_2 * y_1 + x_3 * y_1 + x_1 * y_2 - x_3 * y_2 - x_1 * y_3 + x_2 * y_3

        stiffness_mat = np.zeros((3, 3), dtype=np.single)
        for i in range(3):
            xi_1 = integration_nodes[i, 0]
            xi_2 = integration_nodes[i, 1]
            gr = gradmat(xi_1, xi_2, x_1, x_2, x_3, y_1, y_2, y_3)
            grt = np.transpose(gr)
            grxgrt = gr @ grt
            fp = grxgrt * jacobi_det * integration_weights
            stiffness_mat = stiffness_mat + fp

        mass_mat = np.zeros((3, 3), dtype=np.single)
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
    def boundary_element_p1(nodes: list, value: float) -> np.array:
        """
        Creates boundary element (e.g. for impedance)
        :param nodes: [[x_1, y_1],[x_2, y_2]]
        :param value: value for the boundary element
        :return:
        """

        def phi_p1(node: int, xi: float):
            """
            form function for 1D line element
            todo: transformation for inclined boundary correct?
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

        numintgld1 = np.array([[0.21132486, 0.78867513], [0.50000000, 0.50000000]],
                              dtype=np.single)
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
        element_mat = np.zeros((2, 2), dtype=np.single)
        nb = np.zeros((2, 2))
        for j in range(0, 2):
            for i in range(0, 2):
                for ii in range(0, 2):
                    val = phi_p1(i + 1, intnodes[j]) * phi_p1(ii + 1, intnodes[j]) * intweights[j]
                    nb[i, ii] = val
            element_mat = element_mat + nb
        element_mat = element_mat * length * value

        # transform element to angle
        transformation_matrix = np.array([[math.cos(angle), -1 * math.sin(angle)],
                                          [math.sin(angle), math.cos(angle)]])
        transformed_element = transformation_matrix @ element_mat

        return transformed_element


if __name__ == "__main__":
    # Example output
    nodes_element = [[0, 0], [1.1, -0.1], [0.5, 0.6]]
    nodes_boundary = [[0, 0], [2, 1]]
    boundary_value = 2.5
    k = 0.5
    c = 300.0
    rho = 1.0
    elements = ElementMatrices()
    stiffness_heat_flow_p1, mass_heat_flow_p1 = elements.calc_2d_triangular_heatflow_p1(k, nodes_element)
    stiffness_acoustic_flow_p1, mass_acoustic_flow_p1 = elements.calc_2d_triangular_acoustic_p1(c, rho, nodes_element)
    boundary_element = elements.boundary_element_p1(nodes_boundary, boundary_value)
    print(f"Heat flow element, p = 1: \n{stiffness_heat_flow_p1}\n{mass_heat_flow_p1}")
    print(f"\nAcoustic element, p = 1: \n{stiffness_acoustic_flow_p1}\n{mass_acoustic_flow_p1}")
    print(f"\nBoundary element, p = 1: \n{boundary_element}")
