from typing import List, Dict, Tuple
import numpy as np
from numpy import float64

def midpoint(startpoint: np.ndarray, endpoint: np.ndarray) -> np.ndarray:
    return (startpoint + endpoint) / 2

def get_triangulation_quad(triangulation: List[List[int]]) -> List[List[int]]:
    """
    Improved version...
    """

    def add_midpoint_nodes(triangulation: List[List[int]], maxnode: int) -> List[List[int]]:
        edge_to_midnode = {}
        quad_triangulation = []

        for tri in triangulation:
            quad_tri = []
            for i in range(3):
                start, end = tri[i], tri[(i + 1) % 3]
                edge = tuple(sorted((start, end)))
                # Add the original vertex
                quad_tri.append(start)
                # Add or find the midpoint node
                if edge in edge_to_midnode:
                    midnode = edge_to_midnode[edge]
                else:
                    maxnode += 1
                    midnode = maxnode
                    edge_to_midnode[edge] = midnode
                quad_tri.append(midnode)
            quad_triangulation.append(quad_tri)

        return quad_triangulation

    maxnode = max(max(tri) for tri in triangulation)
    quad_triangulation = add_midpoint_nodes(triangulation, maxnode)

    return quad_triangulation

def get_triangulation_quad_init(triangulation: List[List[int]], sys_nodes: np.ndarray) -> (
        Tuple[List[List[int]], np.array(np.array(float64))]):
    """
    This function returns a triangulation for quadratic elements from a linear element triangulation
    :param triangulation_lin:
    :return:
    """
    # initialize new_nodes_array
    sys_nodes_new = np.zeros((6 * len(triangulation), 2), dtype=np.double)  # max possible number = 6 * nbr_elemenets
    sys_nodes_new[:len(sys_nodes)] = sys_nodes
    # get maxnode
    maxnode = 0
    for e1 in triangulation:
        for e2 in e1:
            if e2 > maxnode:
                maxnode = e2
    maxnode = int(maxnode)

    link_dict = {}
    common_node_dict = {}
    new_nodes_dict = {}
    maxnode += 1
    triangulation = [[int(elem[0]), int(elem[1]), int(elem[2])] for elem in triangulation]
    triangulation_quad = [[int(elem[0]), 0, int(elem[1]), 0, int(elem[2]), 0] for elem in triangulation]
    for nbr, nodes in enumerate(triangulation):
        triangulation_quad_nodes = triangulation_quad[nbr]
        for nbr_l, nodes_l in enumerate(triangulation):
            if len(set(nodes + nodes_l)) == 4:  # Sharing one side
                try:
                    link_dict[nbr].append(nbr_l)
                except KeyError:
                    link_dict[nbr] = [nbr_l]
                common_nodes = sorted(list(set(nodes).intersection(set(nodes_l))))
                if common_nodes and (nbr_l, nbr) not in list(common_node_dict.keys()):
                    common_node_dict[(nbr, nbr_l)] = common_nodes

        nn_1 = sorted([triangulation_quad_nodes[0], triangulation_quad_nodes[2]])
        nn_2 = sorted([triangulation_quad_nodes[2], triangulation_quad_nodes[4]])
        nn_3 = sorted([triangulation_quad_nodes[4], triangulation_quad_nodes[0]])
        if nn_1 in common_node_dict.values():
            if tuple(nn_1) in new_nodes_dict.keys():
                triangulation_quad_nodes[1] = new_nodes_dict[tuple(nn_1)]
            else:
                triangulation_quad_nodes[1] = maxnode
                new_nodes_dict[tuple(nn_1)] = maxnode
                new_node = midpoint(sys_nodes[nn_1[0]], sys_nodes[nn_1[1]])
                sys_nodes_new[maxnode] = new_node
                maxnode += 1
        else:
            triangulation_quad_nodes[1] = maxnode
            new_node = midpoint(sys_nodes[nn_1[0]], sys_nodes[nn_1[1]])
            sys_nodes_new[maxnode] = new_node
            maxnode += 1
        if nn_2 in common_node_dict.values():
            if tuple(nn_2) in new_nodes_dict.keys():
                triangulation_quad_nodes[3] = new_nodes_dict[tuple(nn_2)]
            else:
                triangulation_quad_nodes[3] = maxnode
                new_nodes_dict[tuple(nn_2)] = maxnode
                new_node = midpoint(sys_nodes[nn_2[0]], sys_nodes[nn_2[1]])
                sys_nodes_new[maxnode] = new_node
                maxnode += 1
        else:
            triangulation_quad_nodes[3] = maxnode
            new_node = midpoint(sys_nodes[nn_2[0]], sys_nodes[nn_2[1]])
            sys_nodes_new[maxnode] = new_node
            maxnode += 1
        if nn_3 in common_node_dict.values():
            if tuple(nn_3) in new_nodes_dict.keys():
                triangulation_quad_nodes[5] = new_nodes_dict[tuple(nn_3)]
            else:
                triangulation_quad_nodes[5] = maxnode
                new_nodes_dict[tuple(nn_3)] = maxnode
                new_node = midpoint(sys_nodes[nn_3[0]], sys_nodes[nn_3[1]])
                sys_nodes_new[maxnode] = new_node
                maxnode += 1
        else:
            triangulation_quad_nodes[5] = maxnode
            new_node = midpoint(sys_nodes[nn_3[0]], sys_nodes[nn_3[1]])
            sys_nodes_new[maxnode] = new_node
            maxnode += 1

    sys_nodes_new = sys_nodes_new[:maxnode]

    for elem in sys_nodes_new:
        print(elem)


    return triangulation_quad, sys_nodes_new




if __name__ == '__main__':

    triangulation = [[3, 5, 10],
                     [0, 5, 10],
                     [3, 8, 10],
                     [2, 3, 9],
                     [2, 3, 5],
                     [2, 4, 5],
                     [3, 8, 9],
                     [1, 2, 9],
                     [1, 6, 9],
                     [6, 8, 9],
                     [6, 7, 8]]

    nodes = np.array([[0,0], [1,1]])

    triangulation_quad_old = get_triangulation_quad_init(triangulation, nodes)
    triangulation_quad = get_triangulation_quad(triangulation)

    print('\n')
    for elem, elem_old in zip(triangulation_quad, triangulation_quad_old):
        if elem != elem_old:
            print(elem, elem_old, "ERROR!")
        else:
            print(elem, elem_old)






