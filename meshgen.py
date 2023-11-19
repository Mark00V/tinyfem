import numpy as np
import matplotlib.path as mpath
import math
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import struct  # for checking for duplicates since np.unique not very reliable
from typing import Union
import warnings
import copy
import time
import matplotlib  # delete later, only used for development in matplotlib.use('Qt5Agg')

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

class CreateMesh:


    # For more printing in Development
    DEV = False

    def __init__(self, region_parameters, boundary_parameters, node_parameters, calculation_parameters):
        # input parameters
        self.region_parameters = region_parameters
        self.boundary_parameters = boundary_parameters
        self.node_parameters = node_parameters
        self.calculation_parameters = calculation_parameters
        # mesh creation parameters
        self.density = None  # initialized by normalize_density()
        self.negative_areas = None  # initialized by get_negative_areas()

        #output parameters
        self.single_nodes_dict = None
        self.nodes = None
        self.boundary_nodes = None
        self.boundary_nodes_dict = None
        self.triangulation = None
        self.triangulation_region_dict = None

        # Develop
        self.file_path_dev = r'testing/output_gui_4_calcfem_HE_' + '1' + '.txt'

    @timing_decorator
    def create_mesh(self):
        self.boundary_nodes = list()
        self.normalize_density()
        self.get_negative_areas()
        self.adjust_density()
        self.triangulate_regions()
        self.get_single_nodes_pos()
        self.get_boundary_nodes_pos()


        return self.nodes, self.single_nodes_dict, self.boundary_nodes_dict, self.triangulation, self.triangulation_region_dict

    def adjust_density(self):
        """
        Adjust density for small areas (either x or y)
        :return:
        """
        self.region_size_dict = dict()
        for reg_nbr, values in self.region_parameters.items():
            region_nodes = np.array(values['coordinates'])
            min_x, min_y, max_x, max_y = self.get_min_max_values(region_nodes)
            rect_size_x = np.linalg.norm(max_x - min_x)
            rect_size_y = np.linalg.norm(max_y - min_y)
            self.region_size_dict[reg_nbr] = {'rect_size_x': rect_size_x, 'rect_size_y': rect_size_y}
        regions_max_x = max([elem['rect_size_x'] for elem in self.region_size_dict.values()])
        regions_max_y = max([elem['rect_size_y'] for elem in self.region_size_dict.values()])
        for reg_nbr, values in self.region_size_dict.items():
            self.region_size_dict[reg_nbr]['factor_x'] = self.region_size_dict[reg_nbr]['rect_size_x'] / regions_max_x
            self.region_size_dict[reg_nbr]['factor_y'] = self.region_size_dict[reg_nbr]['rect_size_y'] / regions_max_y

    @timing_decorator
    @staticmethod
    def check_vertice_in_polygon_area(point: Union[list, np.array], polygon: Union[list, np.array]) -> bool:
        """
        Checks if a given point is inside self.polygon:
        returns True if inside polygon, returns False if outside polygon

        Args:
        :param point:
        :return: bool
        """

        if isinstance(polygon, list):
            if polygon[0] != polygon[-1]:
                polygon.append(polygon[0])
        elif isinstance(polygon, np.ndarray):
            if not np.array_equal(polygon[0], polygon[-1]):
                polygon = np.append(polygon, polygon[0].reshape(1, -1), axis=0)
        polygon_path = mpath.Path(polygon)
        is_inside = polygon_path.contains_point(point)

        return is_inside

        return point_on_line

    @timing_decorator
    @staticmethod
    def check_vertice_in_polygon_outline(point: np.array, polygon: np.array, tolerance: float) -> bool:
        """
        Checks if a point is on outline of polygon or in close proximity defined by tolerance
        :param point:
        :return: bool
        """
        if isinstance(polygon, list):
            if polygon[0] != polygon[-1]:
                polygon.append(polygon[0])
            polygon = np.array(polygon)
        elif isinstance(polygon, np.ndarray):
            if not np.array_equal(polygon[0], polygon[-1]):
                polygon = np.append(polygon, polygon[0].reshape(1, -1), axis=0)

        point_on_line = False
        for nv, start_point in enumerate(polygon[:-1]):
            end_point = polygon[nv + 1]

            # check if point is close to start or endpoint, if -> True
            distance_start_point = np.linalg.norm(point - start_point)
            distance_end_point = np.linalg.norm(point - end_point)
            if distance_start_point <= tolerance or distance_end_point <= tolerance:
                return True

            # if point is on line -> True
            direction_vector = end_point - start_point
            with warnings.catch_warnings(record=True) as w:
                normal_vector = np.array([-direction_vector[1], direction_vector[0]])  # todo: manchmal hier runtime warning...
                normal_vector_ = normal_vector / np.linalg.norm(normal_vector)
                if w:
                    for warning in w:
                        if issubclass(warning.category, RuntimeWarning):
                            ...
            first_point_new_rect = np.array(
                [(start_point[0] - tolerance * normal_vector_[0]), (start_point[1] - tolerance * normal_vector_[1])])
            second_point_new_rect = np.array(
                [(end_point[0] - tolerance * normal_vector_[0]), (end_point[1] - tolerance * normal_vector_[1])])
            third_point_new_rect = np.array(
                [(start_point[0] + tolerance * normal_vector_[0]), (start_point[1] + tolerance * normal_vector_[1])])
            fourth_point_new_rect = np.array(
                [(end_point[0] + tolerance * normal_vector_[0]), (end_point[1] + tolerance * normal_vector_[1])])
            check_polygon = np.array([first_point_new_rect, second_point_new_rect, fourth_point_new_rect,
                                      third_point_new_rect, first_point_new_rect])
            is_on_line = CreateMesh.check_vertice_in_polygon_area(point, check_polygon)
            if is_on_line:
                point_on_line = True
                break

        return point_on_line

    @timing_decorator
    @staticmethod
    def point_in_list(point, node_list):
        point_is_in_list_q = np.all(node_list == point, axis=1)

        return True if np.any(point_is_in_list_q) else False

    @timing_decorator
    @staticmethod
    def check_for_duplicate_nodes_np(nodes):
        """

        :param nodes:
        :return:
        """
        complex_coordinates = nodes[:, 0] + 1j * nodes[:, 1]
        unique_complex_coordinates, counts = np.unique(complex_coordinates, return_counts=True)
        duplicate_indices = np.where(counts > 1)[0]
        if CreateMesh.DEV:
            if len(unique_complex_coordinates) != len(nodes):
                print("Duplicate coordinates found at indices:", duplicate_indices)
                print("Duplicate coordinates:", nodes[duplicate_indices])
            else:
                print("No duplicate coordinates found!")

    @timing_decorator
    @staticmethod
    def check_for_duplicate_triangles(triangles):
        """

        :param nodes:
        :return:
        """
        triangles_lst = list()
        for tri in triangles:
            tri_ = str(sorted(tri))
            triangles_lst.append(tri_)
        if CreateMesh.DEV:
            if len(triangles) != len(triangles_lst):
                print("Duplicate triangles found!!!")
            else:
                print("No duplicate triangles found")

    @timing_decorator
    @staticmethod
    def check_for_duplicate_nodes_struct(nodes):
        """

        :param nodes:
        :return:
        """
        check_list = list()
        for p in nodes:
            xs = struct.pack('f', p[0])
            ys = struct.pack('f', p[1])
            ps = f"{xs}{ys}"
            check_list.append(ps)
        if CreateMesh.DEV:
            if len(nodes) != len(set(check_list)):
                print("Duplicates found!")

    @timing_decorator
    @staticmethod
    def plot_polygon_points(points, regions_pos_, regions_neg_, param=None):
        regions_pos = copy.deepcopy(regions_pos_)  # otherwise self.region_parameters will be appended!!!!
        regions_neg = copy.deepcopy(regions_neg_)  # otherwise self.region_parameters will be appended!!!!
        if regions_pos:
            for polygon in regions_pos:
                if polygon[0] != polygon[1]:
                    polygon.append(polygon[0])
                x_coords_polygon, y_coords_polygon = zip(*polygon)
                plt.fill(x_coords_polygon, y_coords_polygon, 'r-', alpha=0.6)  # Polygon fill
                plt.plot(x_coords_polygon, y_coords_polygon, 'r-')  # Polygon outline

        if regions_neg:
            for polygon in regions_neg:
                if polygon[0] != polygon[1]:
                    polygon.append(polygon[0])
                x_coords_polygon, y_coords_polygon = zip(*polygon)
                plt.fill(x_coords_polygon, y_coords_polygon, 'b-', alpha=0.6)  # Polygon fill
                plt.plot(x_coords_polygon, y_coords_polygon, 'b-')  # Polygon outline


        x_coords_points, y_coords_points = zip(*points)

        plt.scatter(x_coords_points, y_coords_points, color='red', marker='.')
        for nbr, p in enumerate(points):
            plt.text(p[0], p[1], str(nbr), fontsize=8, ha='center', va='bottom')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Polygon and Points')
        plt.show()

    @timing_decorator
    @staticmethod
    def plot_triangles(points, triangles, regions_pos_, regions_neg_, param=None):
        regions_pos = copy.deepcopy(regions_pos_)  # otherwise self.region_parameters will be appended!!!!
        regions_neg = copy.deepcopy(regions_neg_)  # otherwise self.region_parameters will be appended!!!!
        if regions_pos:
            for polygon in regions_pos:
                if polygon[0] != polygon[1]:
                    polygon.append(polygon[0])
                x_coords_polygon, y_coords_polygon = zip(*polygon)
                plt.fill(x_coords_polygon, y_coords_polygon, 'r-', alpha=0.6)  # Polygon fill
                plt.plot(x_coords_polygon, y_coords_polygon, 'r-')  # Polygon outline

        if regions_neg:
            for polygon in regions_neg:
                if polygon[0] != polygon[1]:
                    polygon.append(polygon[0])
                x_coords_polygon, y_coords_polygon = zip(*polygon)
                plt.fill(x_coords_polygon, y_coords_polygon, 'b-', alpha=0.6)  # Polygon fill
                plt.plot(x_coords_polygon, y_coords_polygon, 'b-')  # Polygon outline


        plt.triplot(points[:, 0], points[:, 1], triangles, c='gray', label='Mesh')
        plt.scatter(points[:, 0], points[:, 1], c='b', marker='.', label='Seed Points')


        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Triangulation')
        plt.show()

    @timing_decorator
    def normalize_density(self):
        """
        density ist dict mit stufen: 1: sehr grob ... 5: sehr fein
        1: 3 node pro Einheitsunit (Einheitsunit = distance 1.0 in x, y Richtung)
        2: 8 nodes pro Einheitsunit
        3: 15 nodes pro Einheitsunit
        4: 30 nodes pro Einheitsunit
        5: 80 nodes pro Einheitsunit
        :return:
        """
        density_dict = {1: 1/2, 2: 1/4, 3: 1/10, 4: 1/30, 5: 1/80}
        self.density = density_dict[self.calculation_parameters['mesh_density']]

    @timing_decorator
    def get_min_max_values(self, region):
        """
        ...
        """
        region = np.array(region)
        x_values = region[:, 0]
        y_values = region[:, 1]
        min_x, max_x = np.min(x_values), np.max(x_values)
        min_y, max_y = np.min(y_values), np.max(y_values)

        return min_x, min_y, max_x, max_y

    @timing_decorator
    def get_negative_areas(self):
        """
        initializes negative areas
        :return:
        """
        self.negative_areas = list()
        for reg in self.region_parameters.values():
            area_neg_pos = reg['area_neg_pos']
            if area_neg_pos == 'Negative':
                self.negative_areas.append(reg)

    @timing_decorator
    def seed_region(self, region, region_nbr):
        """
        Creates seed points for region
        :return:
        """
        factor_dict = {1: 1,
                       0.5: 1,
                       0.25: 2,
                       0.1: 3,
                       0: 3
                       }
        factor_x = self.region_size_dict[region_nbr]['factor_x']
        factor_y = self.region_size_dict[region_nbr]['factor_y']
        factor_x_adj = sorted([val for val in factor_dict.keys() if val <= factor_x])[-1]
        factor_x_adj = factor_dict[factor_x_adj]
        factor_y_adj = sorted([val for val in factor_dict.keys() if val <= factor_y])[-1]
        factor_y_adj = factor_dict[factor_y_adj]
        factor_keep = max([factor_x_adj, factor_y_adj])


        if region['area_neg_pos'] == 'Positive':
            region_nodes = np.array(region['coordinates'])
            min_x, min_y, max_x, max_y = self.get_min_max_values(region_nodes)
            rect_size_x = np.linalg.norm(max_x - min_x)
            rect_size_y = np.linalg.norm(max_y - min_y)
            nbr_points_x = math.floor(factor_x_adj * rect_size_x / self.density) + 1
            nbr_points_y = math.floor(factor_y_adj * rect_size_y / self.density) + 1
            x_points = np.linspace(min_x, max_x, nbr_points_x)
            y_points = np.linspace(min_y, max_y, nbr_points_y)
            x_grid, y_grid = np.meshgrid(x_points, y_points)
            rect_seed_points = np.column_stack((x_grid.ravel(), y_grid.ravel()))


            keep_points = []
            for idn, point in enumerate(rect_seed_points):  # point is np.array
                point_in_any_negative_area = False

                for negative_area in self.negative_areas:
                    negative_area_coords = np.array(negative_area['coordinates'])
                    if CreateMesh.check_vertice_in_polygon_area(point, negative_area_coords) \
                            or CreateMesh.check_vertice_in_polygon_outline(point, negative_area_coords,
                                                                           tolerance=self.density / (4 * factor_keep)):
                        point_in_any_negative_area = True
                point_in_polygon_area = CreateMesh.check_vertice_in_polygon_area(point, region_nodes)
                point_in_polygon_outline = CreateMesh.check_vertice_in_polygon_outline(point, region_nodes,
                                                                                       tolerance=self.density / (4 * factor_keep))
                if point_in_polygon_area and not point_in_polygon_outline and not point_in_any_negative_area:
                    keep_points.append(idn)
            filtered_seed_points = rect_seed_points[keep_points]

            return filtered_seed_points

    @timing_decorator
    def create_line_vertices(self, line: np.array, region_nbr) -> np.array:
        """
        Creates points on a line specified by line. The number of points is given by density which specifies the average
        distance between 2 points (floored!)
        :param line: np.array([x_coord0, y_coord0], [x_coord1, y_coord1])
        :return: np.array
        """

        start_point = line[0]
        end_point = line[1]
        distance = np.linalg.norm(start_point - end_point)
        num_subdivisions = math.floor(distance / self.density) + 2
        subdivision_points = np.linspace(start_point, end_point, num_subdivisions)

        return subdivision_points

    @timing_decorator
    def seed_boundary(self, region, region_nbr):
        """

        :param region:
        :return:
        """

        region_nodes = np.array(region['coordinates'])
        if not np.array_equal(region_nodes[0], region_nodes[-1]):
            region_nodes = np.append(region_nodes, region_nodes[0].reshape(1, -1), axis=0)

        outline_vertices = None
        for nv, start_point in enumerate(region_nodes[:-1]):
            end_point = region_nodes[nv + 1]
            line = np.array([start_point, end_point])
            if nv == 0:
                interpolation = self.create_line_vertices(line, region_nbr)
                outline_vertices = interpolation[:-1]
                self.boundary_nodes.append(interpolation)
            else:
                interpolation = self.create_line_vertices(line, region_nbr)
                outline_vertices = np.append(outline_vertices, interpolation[:-1], axis=0)
                self.boundary_nodes.append(interpolation)

        return outline_vertices

    @timing_decorator
    def triangulate_region(self, region, region_nbr):
        """
        Creates seed points for all regions
        :return:
        """


        seed_points_area = self.seed_region(region, region_nbr)
        #CreateMesh.plot_polygon_points(seed_points_area, self.positive_regions, self.negative_regions)  # dev
        seed_points_boundary = self.seed_boundary(region, region_nbr)
        #CreateMesh.plot_polygon_points(seed_points_boundary, self.positive_regions, self.negative_regions)  # dev
        seed_points = np.append(seed_points_area, seed_points_boundary, axis=0)

        # check if negative area inside:
        for reg in self.negative_areas:
            #print("QWE - TODO: NEGATIVE AREAS -> seed_points_boundary = self.seed_boundary(reg, 0) 0 sollte region_nbr sein...", reg)
            neg_inside = True
            reg_nodes = reg['coordinates']
            for node in reg_nodes:
                if not CreateMesh.check_vertice_in_polygon_area(node, region['coordinates']):
                    neg_inside = False
                    break
            if neg_inside:
                seed_points_boundary = self.seed_boundary(reg, 0)
                seed_points = np.append(seed_points, seed_points_boundary, axis=0)
                #CreateMesh.plot_polygon_points(seed_points_boundary, self.positive_regions, self.negative_regions)  # dev

        # add user defined points
        boundary_nodes = list()
        for nb in self.boundary_parameters.values():
            p1 = nb['coordinates'][0]
            p2 = nb['coordinates'][1]
            boundary_nodes.append(p1)
            boundary_nodes.append(p2)

        for node in self.node_parameters.values():
            # check if node in boundary_parameters, if not -> user defined -> if in region and not yet seedpoint-> add
            if node['coordinates'] not in boundary_nodes \
                    and CreateMesh.check_vertice_in_polygon_area(node['coordinates'], region['coordinates']) \
                    and not CreateMesh.point_in_list(node['coordinates'], seed_points):
                seed_points = np.append(seed_points, np.array(node['coordinates']).reshape(1, -1), axis=0)

        #seed_points = np.unique(seed_points, axis=0) # this should not be necessary if done right!

        # triangulation
        triangulation = Delaunay(seed_points)
        triangles = triangulation.simplices
        # Remove triangulation outside of polygon and inside of negative area
        keep_triangles = []
        for idt, triangle in enumerate(triangles):
            triangle_in_region = False
            triangle_in_negative_region = False
            triangle_points = np.array([[seed_points[triangle[0]][0], seed_points[triangle[0]][1]],
                                        [seed_points[triangle[1]][0], seed_points[triangle[1]][1]],
                                        [seed_points[triangle[2]][0], seed_points[triangle[2]][1]]])
            center_point = np.mean(triangle_points, axis=0)
            # check if triangle in region
            if CreateMesh.check_vertice_in_polygon_area(center_point, region['coordinates']):
                triangle_in_region = True
            # check if triangle in negative region
            for reg in self.negative_areas:
                negative_reg_nodes = reg['coordinates']
                if CreateMesh.check_vertice_in_polygon_area(center_point, negative_reg_nodes):
                    triangle_in_negative_region = True

            if triangle_in_region and not triangle_in_negative_region:
                keep_triangles.append(idt)
        triangles_filtered = triangles[keep_triangles]

        ############
        # develop
        # check if nodes in region contains duplicates
        # CreateMesh.plot_triangles(seed_points, triangles_filtered, self.positive_regions, self.negative_regions)
        CreateMesh.check_for_duplicate_nodes_np(seed_points)
        #CreateMesh.plot_polygon_points(seed_points, self.positive_regions, self.negative_regions)  # dev
        ###########

        return seed_points, triangles_filtered

    @timing_decorator
    @staticmethod
    def combine_regions(nodes_previous, nodes_this, triangles_this):
        """
        combines regions with adjacent boundaries
        todo: sehr schlechter und langsamer algorithmus...
        :return:
        """
        node_renumbering = dict()
        triangles_new = copy.deepcopy(triangles_this)
        nodes_previous_complex = [node[0] + 1j * node[1] for node in nodes_previous]
        nodes_this_complex = [node[0] + 1j * node[1] for node in nodes_this]
        node_pos_to_keep_this = np.where(~np.isin(nodes_this_complex, nodes_previous_complex))[
            0]  # knoten die behalten werden, aber umnummeriert werden für triagnles
        keep_nodes_this = nodes_this[node_pos_to_keep_this]

        for node in nodes_this_complex:
            pos_node = np.where(np.isin(nodes_this_complex, node))[0]
            pos_node_previous = np.where(np.isin(nodes_previous_complex, node))[0]
            if len(pos_node_previous) == 1:
                node_renumbering[pos_node[0]] = pos_node_previous[0]

        c = 0
        for pos in node_pos_to_keep_this:
            node_renumbering[pos] = len(nodes_previous) + c
            c += 1

        for nb_triangle, triangle in enumerate(triangles_new):
            for nb_pos, pos in enumerate(triangle):
                triangles_new[nb_triangle, nb_pos] = node_renumbering[pos]

        return keep_nodes_this, triangles_new

    @timing_decorator
    def triangulate_regions(self):
        """

        :return:
        """

        self.positive_regions = [region['coordinates'] for region
                            in self.region_parameters.values() if region['area_neg_pos'] == 'Positive']  # for dev
        self.negative_regions = [region['coordinates'] for region
                            in self.region_parameters.values() if region['area_neg_pos'] == 'Negative']  # for dev

        nodes_all = np.empty((0, 2))
        triangles_all = np.empty((0, 3))

        triangle_counter = 0
        triangle_region_dict = dict()
        c_pos = True
        print('Triangulation of regions...')
        for region_nbr, region in self.region_parameters.items():
            print(f"Region {region_nbr} / {len(self.region_parameters.items())}", end='\r')  # This does not show in pycharm, only via cmd / .exe
            if region['area_neg_pos'] == 'Positive':
                nodes_region, triangles_region = self.triangulate_region(region, region_nbr)  # todo besserer algo für boundaries
                if c_pos:
                    nodes_all = np.append(nodes_all, nodes_region, axis=0)
                    triangles_all = np.append(triangles_all, triangles_region, axis=0)
                    triangle_region_dict[region_nbr] = range(0, len(triangles_region))
                    triangle_counter += len(triangles_region)
                    c_pos = False
                else:
                    keep_nodes_region, triangles_region_new = CreateMesh.combine_regions(nodes_all, nodes_region, triangles_region)
                    nodes_all = np.append(nodes_all, keep_nodes_region, axis=0)
                    triangles_all = np.append(triangles_all, triangles_region_new, axis=0)
                    triangle_region_dict[region_nbr] = range(triangle_counter, triangle_counter + len(triangles_region))
                    triangle_counter += len(triangles_region)

        CreateMesh.check_for_duplicate_nodes_np(nodes_all)
        CreateMesh.check_for_duplicate_triangles(triangles_all)
        # dev
        # CreateMesh.plot_polygon_points(nodes_all, self.positive_regions, self.negative_regions)
        # CreateMesh.plot_triangles(nodes_all, triangles_all, self.positive_regions, self.negative_regions)

        self.nodes = nodes_all
        self.triangulation = triangles_all
        self.triangulation_region_dict = triangle_region_dict

    @timing_decorator
    def get_single_nodes_pos(self):
        """
        position of single nodes defined in self.node_parameters
        TODO: very inefficient...
        :return:
        """
        node_dict = dict()
        all_nodes_complex = [node[0] + 1j * node[1] for node in self.nodes]
        for node_nbr, values in self.node_parameters.items():
            node_complex = values['coordinates'][0] + 1j *values['coordinates'][1]
            pos_node = np.where(np.isin(all_nodes_complex, node_complex))[0]
            node_dict[node_nbr] = pos_node[0]
        self.single_nodes_dict = node_dict

    @timing_decorator
    def get_boundary_nodes_pos(self):

        all_nodes_complex = [node[0] + 1j * node[1] for node in self.nodes]

        boundary_number_dict =dict()  # dict key=nbr aus self.boundary_parameters values=zugehörige Knotenkoords
        boundary_pos_val_dict = dict()
        all_boundary_nodes = self.boundary_nodes

        # new
        for n, boundary in enumerate(all_boundary_nodes):
            fn_c = boundary[0][0] + 1j * boundary[0][1]
            ln_c = boundary[-1][0] + 1j * boundary[-1][1]
            for nbr, boundary_param in self.boundary_parameters.items():
                nodes = np.array(boundary_param['coordinates'])
                nodes_c = [node[0] + 1j * node[1] for node in nodes]
                f_eq = np.isin(fn_c, nodes_c)
                l_eq = np.isin(ln_c, nodes_c)
                if f_eq and l_eq:
                    if nbr not in boundary_number_dict.keys():
                        boundary_number_dict[nbr] = boundary

        for nbr, bnodes in boundary_number_dict.items():
            for b_node in bnodes:
                b_node_complex = b_node[0] + 1j * b_node[1]
                pos_in_all_nodes = np.where(all_nodes_complex == b_node_complex)[0]
                try:
                    boundary_pos_val_dict[nbr].append([pos_in_all_nodes[0], b_node])
                except KeyError:
                    boundary_pos_val_dict[nbr] = [[pos_in_all_nodes[0], b_node]]

        self.boundary_nodes_dict = boundary_pos_val_dict

    def develop(self):
        """
        loads data for development
        :return:
        """
        with open(self.file_path_dev, 'r') as f:
            content = f.read()
        exec(content)


if __name__ == '__main__':
    matplotlib.use('TkAgg')
    region_parameters1 = {'0': {'coordinates': [(0.0, 0.0), (2.0, 0.0), (0.0, 2.0)], 'area_neg_pos': 'Positive', 'material': {'k': 1.0, 'c': 340, 'rho': 1.21}}, '1': {'coordinates': [(0.5, 0.5), (1.0, 0.5), (0.5, 1.0)], 'area_neg_pos': 'Negative', 'material': {'k': 1.0, 'c': 340, 'rho': 1.21}}}
    boundary_parameters1 = {'0': {'coordinates': [(0.0, 0.0), (2.0, 0.0)], 'bc': {'type': None, 'value': None}}, '1': {'coordinates': [(2.0, 0.0), (0.0, 2.0)], 'bc': {'type': None, 'value': None}}, '2': {'coordinates': [(0.0, 2.0), (0.0, 0.0)], 'bc': {'type': None, 'value': None}}, '3': {'coordinates': [(0.5, 0.5), (1.0, 0.5)], 'bc': {'type': None, 'value': None}}, '4': {'coordinates': [(1.0, 0.5), (0.5, 1.0)], 'bc': {'type': None, 'value': None}}, '5': {'coordinates': [(0.5, 1.0), (0.5, 0.5)], 'bc': {'type': None, 'value': None}}}
    node_parameters1 = {'0': {'coordinates': (0.0, 0.0), 'bc': {'type': None, 'value': None}}, '1': {'coordinates': (2.0, 0.0), 'bc': {'type': None, 'value': None}}, '2': {'coordinates': (0.0, 2.0), 'bc': {'type': None, 'value': None}}, '3': {'coordinates': (0.5, 0.5), 'bc': {'type': None, 'value': None}}, '4': {'coordinates': (1.0, 0.5), 'bc': {'type': None, 'value': None}}, '5': {'coordinates': (0.5, 1.0), 'bc': {'type': None, 'value': None}}}
    calculation_parameters1 = {'mesh_density': 3, 'freq': None}
    # Obenstehende Werte werden durch createmesh.develop() überschrieben durch content in file self.file_path_dev
    params1 = (region_parameters1, boundary_parameters1, node_parameters1, calculation_parameters1)
    createmesh = CreateMesh(*params1)  # Todo - Develop: For testing mesh
    createmesh.develop()
    nodes, single_nodes_dict, boundary_nodes_dict, triangulation, triangulation_region_dict = createmesh.create_mesh()
    CreateMesh.plot_polygon_points(nodes, createmesh.positive_regions, createmesh.negative_regions)
    # for bnd, vals in boundary_nodes_dict.items():
    #     print(bnd, vals)
    # params
    print(f"\n\n"
          f"Number of nodes:     {len(nodes)}")
    print(f"Number of triangles: {len(triangulation)}")

    # timing for dev:
    print(f"\nTotal execution time          : {time_it_dict['create_mesh']:.4f}")

    print(f"\nTiming of functions: ")
    time_it_dict = dict(sorted(time_it_dict.items(), key=lambda x: x[1]))
    for func, exectime in time_it_dict.items():
        print(f"{str(func)[:29].ljust(30)}: {exectime:.4f}")

