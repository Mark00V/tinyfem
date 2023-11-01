import tkinter as tk
import math
from typing import Callable, Any
from tkinter import filedialog
import json
from guistatics import GUIStatics
import numpy as np
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.tri as tri
from mpl_toolkits.axes_grid1 import make_axes_locatable

class ShowSolution(tk.Toplevel):
    """
    Define Solution Window
    """

    def __init__(self, solution, nodes, triangulation):
        """
        Constructor, inherits from tk toplevel
        :param
        """

        # solution values
        self.solution = solution
        self.nodes = nodes
        self.triangulation = triangulation

        super().__init__()
        self.main_window_solution()

    def main_window_solution(self):
        """
        Creates main window for class Geometry
        :return:
        """
        self.resizable(False, False)
        self.title('TinyFEM - SOLUTION')
        self.geometry(f"{GUIStatics.GEOM_WINDOW_SIZE_X}x{GUIStatics.GEOM_WINDOW_SIZE_Y}")
        ##################################################
        # Position of elements
        # canvas
        border = 0.025
        canvas_x = 1 - GUIStatics.CANVAS_SIZE_X / GUIStatics.GEOM_WINDOW_SIZE_X - border
        canvas_y = 1 - GUIStatics.CANVAS_SIZE_Y / GUIStatics.GEOM_WINDOW_SIZE_Y - border

        # buttons and text on left side
        widgets_x_start = 0.01
        ##################################################

        ##############
        # Create a Matplotlib figure
        fig, ax = self.create_mpl_fig()

        # Create a canvas widget to embed the Matplotlib figure
        self.canvas_main = tk.Canvas(self, width=GUIStatics.CANVAS_SIZE_X, height=GUIStatics.CANVAS_SIZE_Y,
                                bg=GUIStatics.CANVAS_BG)
        self.canvas_main.place(relx=canvas_x + 0.0075, rely=canvas_y)
        GUIStatics.add_canvas_border(self.canvas_main)

        canvas_mpl = FigureCanvasTkAgg(fig, master=self)
        canvas_mpl_widget = canvas_mpl.get_tk_widget()
        canvas_mpl_widget.place(relx=canvas_x + 0.0075+0.003, rely=canvas_y+0.006)

    def create_mpl_fig(self):
        """

        :return:
        """
        all_points = self.nodes
        solution = self.solution
        triangles = self.triangulation

        dataz = np.real(solution)
        values = dataz
        aspectxy = 1
        triang_mpl = tri.Triangulation(all_points[:, 0], all_points[:, 1], triangles)

        fig = Figure(figsize=(9.15, 7.15), dpi=100, facecolor='lightgray')
        ax = fig.add_subplot(111)
        label_font_title = {'fontsize': 14, 'fontfamily': 'sans-serif'}
        ax.set_title("Solution", **label_font_title)
        label_font_axes = {'fontsize': 12, 'fontfamily': 'sans-serif'}
        ax.set_xlabel('x [m]', **label_font_axes)
        ax.set_ylabel('y [m]', **label_font_axes)
        ax.set_aspect(aspectxy)

        contour = ax.tricontourf(triang_mpl, values, cmap='viridis', levels=20)
        ax.set_facecolor('lightgray')  # backgroundcolor of contourmap
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.2)

        fig.colorbar(contour, cax=cax)
        ax.scatter(all_points[:, 0], all_points[:, 1], c=values, cmap='viridis', marker='.',
                             edgecolors='w', s=10)
        ax.triplot(triang_mpl, 'w-', linewidth=0.3)

        return fig, ax

if __name__ == '__main__':

    solution = np.array([1.5, 1.0, 1.0, 1.75, 2.0, 2.0])
    nodes = np.array([[0.0, 0.0], [0.5, 0.0], [1.0,  0.0], [1.0, 0.5], [1.0,  1.0], [0.5, 0.5]])
    triangles = np.array([[1., 5., 0.], [5., 3., 4.], [1., 3., 5.], [3., 1., 2.]])
    show_solution = ShowSolution(solution, nodes, triangles)  # Develop
    show_solution.mainloop()
