# output parameters
self.single_nodes_dict = None
self.nodes = None
self.boundary_nodes = None
self.boundary_nodes_pos = None
self.triangulation = None
self.triangulation_region_dict = None


def create_mesh(self):
    self.boundary_nodes = list()
    self.normalize_density()
    self.get_negative_areas()
    self.triangulate_regions()
    self.get_single_nodes_pos()
    self.get_boundary_nodes_pos()