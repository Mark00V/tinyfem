from typing import List

def get_triangulation_quad(triangulation: List[List[int]]) -> List[List[int]]:
    """
    This function returns a triangulation for quadratic elements from a linear element triangulation
    :param triangulation_lin:
    :return:
    """

    # get maxnode
    maxnode = 0
    for e1 in triangulation:
        for e2 in e1:
            if e2 > maxnode:
                maxnode = e2

    link_dict = {}
    common_node_dict = {}
    new_nodes_dict = {}
    maxnode += 1
    triangulation_quad = [[elem[0], 0, elem[1], 0, elem[2], 0] for elem in triangulation]
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
                maxnode += 1
        else:
            triangulation_quad_nodes[1] = maxnode
            maxnode += 1
        if nn_2 in common_node_dict.values():
            if tuple(nn_2) in new_nodes_dict.keys():
                triangulation_quad_nodes[3] = new_nodes_dict[tuple(nn_2)]
            else:
                triangulation_quad_nodes[3] = maxnode
                new_nodes_dict[tuple(nn_2)] = maxnode
                maxnode += 1
        else:
            triangulation_quad_nodes[3] = maxnode
            maxnode += 1
        if nn_3 in common_node_dict.values():
            if tuple(nn_3) in new_nodes_dict.keys():
                triangulation_quad_nodes[5] = new_nodes_dict[tuple(nn_3)]
            else:
                triangulation_quad_nodes[5] = maxnode
                new_nodes_dict[tuple(nn_3)] = maxnode
                maxnode += 1
        else:
            triangulation_quad_nodes[5] = maxnode
            maxnode += 1

    return triangulation_quad


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

triangulation_quad = get_triangulation_quad(triangulation)


print('\n')
for elem in triangulation_quad:
    print(elem)






