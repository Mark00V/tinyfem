import numpy as np
import matplotlib.path as mpath
from typing import Union

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
        normal_vector = np.array([-direction_vector[1], direction_vector[0]])  # todo: manchmal hier runtime warning...
        normal_vector_ = normal_vector / np.linalg.norm(normal_vector)

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
        is_on_line = check_vertice_in_polygon_area(point, check_polygon)
        if is_on_line:
            point_on_line = True
            break

    return point_on_line

def point_in_list(point, node_list):
    point_is_in_list_q = np.all(node_list == point, axis=1)

    return True if np.any(point_is_in_list_q) else False

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