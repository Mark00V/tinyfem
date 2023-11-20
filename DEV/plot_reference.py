"""
Plot reference data from other FEM framework
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib.patches import Polygon
from matplotlib.path import Path
import matplotlib

############################################################
FILENBR = 1
EQ = 'HH'  # either HE for Heat Equation or HH for Helmholtz
HH_M = 'SPL'  # Either P for Pressure or SPL for sound pressure levle
############################################################

DATA_PATH_WLG = os.path.join('../Verification', 'Verifikation WLG')
DATA_PATH_HH = os.path.join('../Verification', 'Verifikation_HH')
str_me = 'veri_wlg_' if EQ == 'HE' else 'veri_HH_'
DATA_FILE = str_me + str(FILENBR) + '_100Hz.txt'       # input file for verification
POLY_FILE = str_me + str(FILENBR) + '_geom.txt'  # for creating mesh in tinyfem
PATH_SOL = os.path.join(DATA_PATH_WLG, DATA_FILE) if EQ == 'HE' else os.path.join(DATA_PATH_HH, DATA_FILE)
PATH_POLY = os.path.join(DATA_PATH_WLG, POLY_FILE) if EQ == 'HE' else os.path.join(DATA_PATH_HH, POLY_FILE)

def open_file(path):
    """
    opens file and converts data to np.array
    :param path:
    :return:
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("File not found.")
    except IOError:
        print("Error reading the file.")

    content = content.split('\n')
    solution_cloud = list()
    for line in content:
        try:
            if line[0] == '%':
                continue
        except IndexError:
            ...
        line = line.split()
        try:
            val_x, val_y, val_sol = line[0], line[1], line[2]
        except IndexError:
            ...

        solution_cloud.append([float(val_x), float(val_y), float(val_sol)])
    solution_cloud = np.array(solution_cloud)

    return solution_cloud

def plot_solution(solution_cloud, polygon_merged):
    """
    plots solution via matplotlib
    polygon_merged is the mask: everything inside polygon_merged will be plotted, all else white
    :param solution_cloud:
    :return:
    """

    x = solution_cloud[:, 0]
    y = solution_cloud[:, 1]
    z = solution_cloud[:, 2]
    z = np.nan_to_num(z, nan=0)

    polygon = Polygon(polygon_merged, closed=True, facecolor='white', linewidth=0)
    plt.gca().add_patch(polygon)
    triangulation = tri.Triangulation(x, y)

    if EQ == 'HE':
        cmap = 'jet'
    else:
        if HH_M == 'P':
            cmap = 'cool'
        else:
            cmap = 'inferno'
    contour = plt.tripcolor(triangulation, z, cmap=cmap, vmin=90, vmax=115)
    plt.colorbar()
    contour.set_clip_path(polygon)
    plt.gca().set_aspect('equal')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Solution')

    plt.show()

def read_polygon(polyfile):
    """
    Reads the geometry and converts to single polygon for mask for plot
    polyfile must have lines with values 'w=1, h=0.3, x=0, y=0' and no \n at end or start
    Start of line: % -> Line describes rectangle
    Start of Line: ! -> Line describes polygon
    :param polyfile:
    :return:
    """
    try:
        with open(polyfile, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("File not found.")
    except IOError:
        print("Error reading the file.")

    content = content.split('\n')
    polygons = list()
    for line in content:
        if line[0] == '%':
            line = line.split(',')
            w = float(line[0].split('=')[-1])
            h = float(line[1].split('=')[-1])
            x = float(line[2].split('=')[-1])
            y = float(line[3].split('=')[-1])
            polynodes = [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]
            polynodes = polynodes + [polynodes[0]]  # include start point necessary for numpy merge polygons method
            polynodes = np.array(polynodes)
            polygons.append(polynodes)
        if line[0] == '!':
            polynodes = eval(line[1:])
            polynodes = polynodes + [polynodes[0]]
            polynodes = np.array(polynodes)
            if FILENBR == 2 and EQ == 'HE':
                polynodes *= 3
            polygons.append(polynodes)


    poly_tinyfem= dict()
    poly_tinyfem["polygons"] = {}
    poly_tinyfem["points"] = {}
    poly_tinyfem["units"] = "m"
    poly_tinyfem["other"] = "None"

    for nbr, poly in enumerate(polygons):
        dic = {"coordinates": list([list(node) for node in poly[:-1]]), "area_neg_pos": "Positive"}
        poly_tinyfem["polygons"][str(nbr)] = dic


    polygon_merged = polygons[0]
    for poly in polygons[1:]:
        polygon_merged = np.vstack((polygon_merged, poly))

    return polygon_merged, poly_tinyfem


def main():
    matplotlib.use('TkAgg')
    solution_cloud = open_file(PATH_SOL)
    polygon_merged, poly_tinyfem  = read_polygon(PATH_POLY)
    plot_solution(solution_cloud, polygon_merged)
    print(poly_tinyfem)

main()