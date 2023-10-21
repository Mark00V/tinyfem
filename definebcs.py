"""
Define the boundarie conditions and region parameters
This class is independend from GUI and only prepares output to be flagged and set in boundary and parameter gui

Input: Geometry from class Geometry: e.g.:
geometry_input =
{"polygons": {
"0": {"coordinates": [[0.1, -0.2], [1.5, -0.2], [1.5, 1.1], [0.0, 1.1]], "area_neg_pos": "Positive"},
"1": {"coordinates": [[0.6, 0.5], [0.8, 0.8], [0.8, 0.2]], "area_neg_pos": "Negative"},
"2": {"coordinates": [[1.5, -1.5], [2.5, 0.0], [2.5, 2.5], [1.5, 2.5], [1.5, 1.1], [1.5, -0.2]], "area_neg_pos": "Positive"}
                },
"points": {
"0": [0.5, 0.5],
"1": [2.0, 0.2]
            },
"units": "m",
"other": null}
"polygons" cannot be empty and coordinates have at least 3 nodes
"points" can be empty
e.g:
Output:
1) Input from class Geometry for boundary conditions GUI
2) List of unique nodes and their membership in method create_nodes()
3) List of boundaries and their membership in method create_boundaries()
self.regions: {'0': {'coordinates': [(0.1, -0.2), (1.5, -0.2), (1.5, 1.1), (0.0, 1.1)], 'area_neg_pos': 'Positive'}, '1': {'coordinates': [(0.6, 0.5), (0.8, 0.8), (0.8, 0.2)], 'area_neg_pos': 'Negative'}, '2': {'coordinates': [(1.5, -1.5), (2.5, 0.0), (2.5, 2.5), (1.5, 2.5), (1.5, 1.1), (1.5, -0.2)], 'area_neg_pos': 'Positive'}}
self.boundaries: {'0': ((0.1, -0.2), (1.5, -0.2)), '1': ((1.5, -0.2), (1.5, 1.1)), '2': ((1.5, 1.1), (0.0, 1.1)), '3': ((0.0, 1.1), (0.1, -0.2)), '4': ((0.6, 0.5), (0.8, 0.8)), '5': ((0.8, 0.8), (0.8, 0.2)), '6': ((0.8, 0.2), (0.6, 0.5)), '7': ((1.5, -1.5), (2.5, 0.0)), '8': ((2.5, 0.0), (2.5, 2.5)), '9': ((2.5, 2.5), (1.5, 2.5)), '10': ((1.5, 2.5), (1.5, 1.1)), '11': ((1.5, -0.2), (1.5, -1.5))}
self.nodes: {'0': (0.5, 0.5), '1': (2.0, 0.2), '2': (0.1, -0.2), '3': (1.5, -0.2), '4': (1.5, 1.1), '5': (0.0, 1.1), '6': (0.6, 0.5), '7': (0.8, 0.8), '8': (0.8, 0.2), '9': (1.5, -1.5), '10': (2.5, 0.0), '11': (2.5, 2.5), '12': (1.5, 2.5)}

no nodes:
"""


class CompatibilityError(Exception):
    """
    Custom Raise Error class
    """
    pass


class CreateBCParams:
    """
    Reformats input from class geometry: All nodes, boundaries and regions are now unique and have new numbering
    """

    def __init__(self, geometry_input: dict):
        self.geometry_input = geometry_input  # Input from class Geometry
        self.polygons = geometry_input["polygons"]  # Polygons from input
        self.points = geometry_input["points"]  # points from input
        if self.points == {'None'}:  # input from gui, reformat for this class
            self.points = {}
        self.units = geometry_input["units"]  # units, needed for plotting
        self.other = geometry_input["other"]  # Other stuff, may be needed in future
        self.nodes = None  # All unique nodes
        self.boundaries = None  # All unique boundaries
        self.regions = None  # All unique regions (unique from geometry restriction!) todo: check in class Geometry)
        self.regions_counter = 0
        self.boundaries_counter = 0
        self.nodes_counter = 0

    def main(self):
        """
        main method
        :return:
        """

        self.create_regions()  # erst region kreiren dami später evtl auch überschneidungen berücichtigt werden können
        self.create_boundaries()
        self.create_nodes()
        check_compatibility = self.check_uniqueness()
        if not check_compatibility:
            raise CompatibilityError("COMPATIBILITY ERROR FOR NODES/BOUNDARIES: NOT UNIQUE!")

        return self.regions, self.boundaries, self.nodes

    def create_nodes(self):
        """
        creates a unique list of nodes including polygon nodes and single points. Declares membership
        e.g. member of polygon-node (including numbers of polygon from input) and/or member of single point
        (number from input)
        :return:
        """

        vertices_dict = dict()
        all_vertices_coordinates = set()
        for point_key in self.points.keys():
            point_coords = self.points[point_key]
            point_coords = (point_coords[0], point_coords[1])
            if point_coords in all_vertices_coordinates:
                continue
            all_vertices_coordinates.add(point_coords)
            vertices_dict[str(self.nodes_counter)] = point_coords
            self.nodes_counter += 1

        for boundary, nodes in self.boundaries.items():
            for point_coords in nodes:
                if point_coords in all_vertices_coordinates:
                    continue
                all_vertices_coordinates.add(point_coords)
                vertices_dict[str(self.nodes_counter)] = point_coords
                self.nodes_counter += 1

        self.nodes = vertices_dict

    def create_boundaries(self):
        """
        creates numbered boundaries for self.boundaries. Duplicate boundaries ((point1, point2),(point2, point1)
        is duplicate!) will be disregarded -> boundaries of adjacent regions count as one boundary!
        :return:
        """

        boundaries_dict = dict()
        all_boundary_coordinates = set()
        for region_number in self.regions.keys():
            region_coordinates = self.regions[region_number]['coordinates']
            for section_start_node, section_end_node in zip(region_coordinates[:-1], region_coordinates[1:]):
                if (section_start_node, section_end_node) in all_boundary_coordinates \
                        or (section_end_node, section_start_node) in all_boundary_coordinates:
                    continue
                boundaries_dict[str(self.boundaries_counter)] = (section_start_node, section_end_node)
                all_boundary_coordinates.add((section_start_node, section_end_node))
                self.boundaries_counter += 1
            if (region_coordinates[-1], region_coordinates[0]) in all_boundary_coordinates \
                    or (region_coordinates[0], region_coordinates[-1]) in all_boundary_coordinates:
                pass
            else:
                boundaries_dict[str(self.boundaries_counter)] = (region_coordinates[-1], region_coordinates[0])
                all_boundary_coordinates.add((region_coordinates[0], region_coordinates[-1]))
                self.boundaries_counter += 1

        self.boundaries = boundaries_dict

    def create_regions(self):
        """
        Creates numbered regions dict
        :return:
        """

        region_dict = dict()
        for poly_key in self.polygons.keys():
            polygon_nodes = self.polygons[poly_key]['coordinates']
            polygon_nodes = [(node[0], node[1]) for node in polygon_nodes]
            polygon_neg_pos_area = self.polygons[poly_key]['area_neg_pos']
            region_dict[str(self.regions_counter)] = {'coordinates': polygon_nodes,
                                                      'area_neg_pos': polygon_neg_pos_area}
            self.regions_counter += 1
        self.regions = region_dict

    def check_uniqueness(self):
        """
        checks if nodes and boundaries are unique, returns True if all okay, else False
        :return:
        """
        # check nodes
        all_nodes = [node for node in self.nodes.values()]
        all_nodes_set = set(all_nodes)
        all_nodes_keys = set([key for key in self.nodes.keys()])
        check_nodes = True if len(all_nodes) == len(all_nodes_set) == len(all_nodes_keys) else False

        # check boundaries
        all_boundaries_normal = [nodes for nodes in self.boundaries.values()]
        all_boundaries_reversed = [(nodes[1], nodes[0]) for nodes in self.boundaries.values()]
        all_boundaries_comb = all_boundaries_normal + all_boundaries_reversed
        all_boundaries_normal_len = len(set(all_boundaries_normal))
        all_boundaries_reversed_len = len(set(all_boundaries_reversed))
        all_boundaries_comb_len = len(set(all_boundaries_comb))
        all_boundaries_keys_len = len(set([key for key in self.boundaries.keys()]))
        check_boundaries = True if all_boundaries_normal_len == all_boundaries_reversed_len == \
                                   all_boundaries_comb_len / 2 == all_boundaries_keys_len else False

        return True if check_nodes and check_boundaries else False

    def debug(self):
        """
        For debugging
        :return:
        """
        print(f"self.regions: {self.regions}")
        print(f"self.boundaries: {self.boundaries}")
        print(f"self.nodes: {self.nodes}")


if __name__ == '__main__':
    test_input_1 = {
        "polygons": {
            "0": {"coordinates": [[0.1, -0.2], [1.5, -0.2], [1.5, 1.1], [0.0, 1.1]], "area_neg_pos": "Positive"},
            "1": {"coordinates": [[0.6, 0.5], [0.8, 0.8], [0.8, 0.2]], "area_neg_pos": "Negative"},
            "2": {"coordinates": [[1.5, -1.5], [2.5, 0.0], [2.5, 2.5], [1.5, 2.5], [1.5, 1.1], [1.5, -0.2]],
                  "area_neg_pos": "Positive"}}, "points": {"0": [0.5, 0.5], "1": [2.0, 0.2]}, "units": "m",
        "other": "None"}
    test_input_2 = {
        "polygons": {"0": {"coordinates": [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]], "area_neg_pos": "Positive"}},
        "points": {"None"}, "units": "m", "other": "None"}
    test_input_3 = {"polygons": {"0": {"coordinates": [[-4.0, -3.0], [1.0, -2.5], [2.5, 1.0], [-2.5, 1.0], [-4.2, -1.5]], "area_neg_pos": "Positive"}, "1": {"coordinates": [[2.5, 1.0], [0.0, 3.0], [-2.5, 1.0]], "area_neg_pos": "Positive"}, "2": {"coordinates": [[-1.0, 0.0], [0.0, 0.0], [0.0, 0.75], [-1.0, 0.5]], "area_neg_pos": "Negative"}}, "points": {"0": [-3.0, -2.0], "1": [0.0, 1.5], "2": [1.0, -1.0]}, "units": "m", "other": "None"}

    test_input = test_input_3
    createbcs = CreateBCParams(test_input)
    createbcs.main()
    createbcs.debug()
