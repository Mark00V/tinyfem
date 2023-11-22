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
maxnode = 10

link_dict = {}
new_node_dict = {}
for nbr, nodes in enumerate(triangulation):
    for nbr_l, nodes_l in enumerate(triangulation):
        if len(set(nodes + nodes_l)) == 4:  # Sharing one side
            try:
                link_dict[nbr].append(nbr_l)
            except KeyError:
                link_dict[nbr] = [nbr_l]


for k, v in link_dict.items():
    print(k, v)

# todo entweder linked list oder rekursiv