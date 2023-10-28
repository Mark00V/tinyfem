import numpy as np
import matplotlib.path as mpath
import math
import random
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import struct  # for checking for duplicates since np.unique not very reliable
from typing import Union
import warnings
import copy


class CreateMesh:

    def __init__(self, region_parameters, boundary_parameters, node_parameters, calculation_parameters):
        # input parameters
        self.region_parameters = region_parameters
        self.boundary_parameters = boundary_parameters
        self.node_parameters = node_parameters
        self.calculation_parameters = calculation_parameters
        # mesh creation parameters
        self.density = None  # initialized by normalize_density()
        self.negative_areas = None  # initialized by get_negative_areas()
        self.nodes = np.empty((0, 2))
        #output parameters
        self.single_nodes = dict()

    def create_mesh(self):
        self.normalize_density()
        self.get_negative_areas()
        self.triangulate_regions()

    def normalize_density(self):
        """
        density ist dict mit stufen: 1: sehr grob ... 5: sehr fein
        1: 2 node pro Einheitsunit (Einheitsunit = distance 1.0 in x, y Richtung)
        2: 4 nodes pro Einheitsunit
        3: 10 nodes pro Einheitsunit
        4: 30 nodes pro Einheitsunit
        5: 80 nodes pro Einheitsunit
        :return:
        """
        density_dict = {1: 1/2, 2: 1/4, 3: 1/10, 4: 1/30, 5: 1/80}
        self.density = density_dict[self.calculation_parameters['mesh_density']]

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
                            #print(f"RuntimeWarning: {warning.message} for {normal_vector}, {start_point}, {end_point}, {polygon}")
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
            plt.text(p[0], p[1], str(nbr), fontsize=6, ha='center', va='bottom')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Polygon and Points')
        plt.show()

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

    def seed_region(self, region):
        """
        Creates seed points for region
        :return:
        """



        if region['area_neg_pos'] == 'Positive':
            region_nodes = np.array(region['coordinates'])
            min_x, min_y, max_x, max_y = self.get_min_max_values(region_nodes)
            rect_size_x = np.linalg.norm(max_x - min_x)
            rect_size_y = np.linalg.norm(max_y - min_y)
            nbr_points_x = math.floor(rect_size_x / self.density) + 1
            nbr_points_y = math.floor(rect_size_y / self.density) + 1

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
                                                                           tolerance=self.density / 4):
                        point_in_any_negative_area = True
                point_in_polygon_area = CreateMesh.check_vertice_in_polygon_area(point, region_nodes)
                point_in_polygon_outline = CreateMesh.check_vertice_in_polygon_outline(point, region_nodes,
                                                                                       tolerance=self.density / 4)
                if point_in_polygon_area and not point_in_polygon_outline and not point_in_any_negative_area:
                    keep_points.append(idn)
            filtered_seed_points = rect_seed_points[keep_points]

            return filtered_seed_points

    def create_line_vertices(self, line: np.array) -> np.array:
        """
        Creates points on a line specified by line. The number of points is given by density which specifies the average
        distance between 2 points (floored!)
        :param line: np.array([x_coord0, y_coord0], [x_coord1, y_coord1])
        :return: np.array
        """
        start_point = line[0]
        end_point = line[1]
        distance = np.linalg.norm(start_point - end_point)
        num_subdivisions = math.floor(distance / self.density) + 1
        subdivision_points = np.linspace(start_point, end_point, num_subdivisions)

        return subdivision_points

    def seed_boundary(self, region):
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
                outline_vertices = self.create_line_vertices(line)[:-1]
            else:
                outline_vertices = np.append(outline_vertices, self.create_line_vertices(line)[:-1], axis=0)

        return outline_vertices

    @staticmethod
    def point_in_list(point, node_list):
        point_is_in_list_q = np.all(node_list == point, axis=1)

        return True if np.any(point_is_in_list_q) else False


    def triangulate_region(self, region):
        """
        Creates seed points for all regions
        :return:
        """

        seed_points_area = self.seed_region(region)
        #CreateMesh.plot_polygon_points(seed_points_area, self.positive_regions, self.negative_regions)  # dev
        seed_points_boundary = self.seed_boundary(region)
        #CreateMesh.plot_polygon_points(seed_points_boundary, self.positive_regions, self.negative_regions)  # dev
        seed_points = np.append(seed_points_area, seed_points_boundary, axis=0)

        # check if negative area inside:
        for reg in self.negative_areas:
            neg_inside = True
            reg_nodes = reg['coordinates']
            for node in reg_nodes:
                if not CreateMesh.check_vertice_in_polygon_area(node, region['coordinates']):
                    neg_inside = False
                    break
            if neg_inside:
                seed_points_boundary = self.seed_boundary(reg)
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

        CreateMesh.plot_triangles(seed_points, triangles_filtered, self.positive_regions, self.negative_regions)

        ############
        # develop
        # check if nodes in region contains duplicates
        duplicate_check = CreateMesh.check_for_duplicate_nodes_np(seed_points)
        #CreateMesh.plot_polygon_points(seed_points, self.positive_regions, self.negative_regions)  # dev

        ###########


    @staticmethod
    def check_for_duplicate_nodes_np(nodes):
        """

        :param nodes:
        :return:
        """
        complex_coordinates = nodes[:, 0] + 1j * nodes[:, 1]
        unique_complex_coordinates, counts = np.unique(complex_coordinates, return_counts=True)
        duplicate_indices = np.where(counts > 1)[0]
        if len(unique_complex_coordinates) != len(nodes):
            print("Duplicate coordinates found at indices:", duplicate_indices)
            print("Duplicate coordinates:", nodes[duplicate_indices])
        else:
            print("No duplicates found!")

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

        if len(nodes) != len(set(check_list)):
            print("Duplicates found!")

    def triangulate_regions(self):
        """

        :return:
        """

        self.positive_regions = [region['coordinates'] for region
                            in self.region_parameters.values() if region['area_neg_pos'] == 'Positive']  # for dev
        self.negative_regions = [region['coordinates'] for region
                            in self.region_parameters.values() if region['area_neg_pos'] == 'Negative']  # for dev

        for region in self.region_parameters.values():
            print("\n\n\n", region)
            if region['area_neg_pos'] == 'Positive':
                triangulated_region = self.triangulate_region(region)

        # todo: knotenpunkte an angrenzenden boundaries übereinstimmend?
        # -> einmal löschen bzw dreiecke der einen region an die andere forcieren





if __name__ == '__main__':
    region_parameters1 = {'0': {'coordinates': [(-4.0, -3.0), (1.0, -2.5), (2.5, 1.0), (-2.5, 1.0), (-2.2, -1.5)],
                                    'area_neg_pos': 'Positive', 'material': {'k': 0, 'c': 0, 'rho': 0}},
                              '1': {'coordinates': [(2.5, 1.0), (0.0, 3.0), (-2.5, 1.0)], 'area_neg_pos': 'Positive',
                                    'material': {'k': 0, 'c': 0, 'rho': 0}},
                              '2': {'coordinates': [(-1.0, 0.0), (0.0, 0.0), (0.0, 0.75), (-1.0, 0.5)],
                                    'area_neg_pos': 'Negative', 'material': {'k': 0, 'c': 0, 'rho': 0}}}
    boundary_parameters1 = {'0': {'coordinates': [(-4.0, -3.0), (1.0, -2.5)], 'bc': {'type': None, 'value': None}},
                                '1': {'coordinates': [(1.0, -2.5), (2.5, 1.0)], 'bc': {'type': None, 'value': None}},
                                '2': {'coordinates': [(2.5, 1.0), (-2.5, 1.0)], 'bc': {'type': None, 'value': None}},
                                '3': {'coordinates': [(-2.5, 1.0), (-4.2, -1.5)], 'bc': {'type': None, 'value': None}},
                                '4': {'coordinates': [(-4.2, -1.5), (-4.0, -3.0)], 'bc': {'type': None, 'value': None}},
                                '5': {'coordinates': [(2.5, 1.0), (0.0, 3.0)], 'bc': {'type': None, 'value': None}},
                                '6': {'coordinates': [(0.0, 3.0), (-2.5, 1.0)], 'bc': {'type': None, 'value': None}},
                                '7': {'coordinates': [(-1.0, 0.0), (0.0, 0.0)], 'bc': {'type': None, 'value': None}},
                                '8': {'coordinates': [(0.0, 0.0), (0.0, 0.75)], 'bc': {'type': None, 'value': None}},
                                '9': {'coordinates': [(0.0, 0.75), (-1.0, 0.5)], 'bc': {'type': None, 'value': None}},
                                '10': {'coordinates': [(-1.0, 0.5), (-1.0, 0.0)], 'bc': {'type': None, 'value': None}}}
    node_parameters1 = {'0': {'coordinates': (-3.0, -2.0), 'bc': {'type': None, 'value': None}},
                            '1': {'coordinates': (0.0, 1.5), 'bc': {'type': None, 'value': None}},
                            '2': {'coordinates': (1.0, -1.0), 'bc': {'type': None, 'value': None}},
                            '3': {'coordinates': (-4.0, -3.0), 'bc': {'type': None, 'value': None}},
                            '4': {'coordinates': (1.0, -2.5), 'bc': {'type': None, 'value': None}},
                            '5': {'coordinates': (2.5, 1.0), 'bc': {'type': None, 'value': None}},
                            '6': {'coordinates': (-2.5, 1.0), 'bc': {'type': None, 'value': None}},
                            '7': {'coordinates': (-4.2, -1.5), 'bc': {'type': None, 'value': None}},
                            '8': {'coordinates': (0.0, 3.0), 'bc': {'type': None, 'value': None}},
                            '9': {'coordinates': (-1.0, 0.0), 'bc': {'type': None, 'value': None}},
                            '10': {'coordinates': (0.0, 0.0), 'bc': {'type': None, 'value': None}},
                            '11': {'coordinates': (0.0, 0.75), 'bc': {'type': None, 'value': None}},
                            '12': {'coordinates': (-1.0, 0.5), 'bc': {'type': None, 'value': None}}}
    calculation_parameters1 = {'mesh_density': 2, 'freq': None}
    params1 = (region_parameters1, boundary_parameters1, node_parameters1, calculation_parameters1)
    createmesh = CreateMesh(*params1)  # Todo - Develop: For testing mesh
    mesh = createmesh.create_mesh()
