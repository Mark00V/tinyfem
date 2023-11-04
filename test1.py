

single_nodes_dict = {'0': 4, '1': 9, '2': 13, '3': 17, '4': 21, '5': 41}
triangulation_region_dict = {'0': range(0, 32), '1': range(32, 49)}
def get_region_for_node_nbr(node):

    for key, val in triangulation_region_dict.items():
        if node in val:
            return key

node = 33
res = get_region_for_node_nbr(node)
print(res)