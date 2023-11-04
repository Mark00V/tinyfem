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
        self.iconbitmap('tiny_fem_icon.ico')
        ##################################################
        # Position of elements
        # canvas
        border = 0.025
        canvas_x = 1 - GUIStatics.CANVAS_SIZE_X / GUIStatics.GEOM_WINDOW_SIZE_X - border
        canvas_y = 1 - GUIStatics.CANVAS_SIZE_Y / GUIStatics.GEOM_WINDOW_SIZE_Y - border

        # buttons and text on left side
        widgets_x_start = 0.01
        ##################################################

        # Create a Matplotlib figure
        fig, ax = self.create_mpl_fig()

        # canvas qith Matplotlib figure (canvas on top of canvas
        self.canvas_main = tk.Canvas(self, width=GUIStatics.CANVAS_SIZE_X, height=GUIStatics.CANVAS_SIZE_Y,
                                bg=GUIStatics.CANVAS_BG)
        self.canvas_main.place(relx=canvas_x + 0.0075, rely=canvas_y)
        GUIStatics.add_canvas_border(self.canvas_main)

        canvas_mpl = FigureCanvasTkAgg(fig, master=self)
        self.canvas_mpl_widget = canvas_mpl.get_tk_widget()
        self.canvas_mpl_widget.place(relx=canvas_x + 0.0075+0.003, rely=canvas_y+0.006)

        # buttons
        def export_solution_csv():
            export_string = self.convert_solution_to_string()
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt")],
                title="Save Input As",
            )
            if file_path:
                with open(file_path, "w") as file:
                    file.write(export_string)

        def export_image():
            file_path = "Output_solution.png"  # Specify the file path and format here
            fig.savefig(file_path, dpi=200)

        def get_min_value():
            GUIStatics.window_error(self, "Work In Progress...")

        def get_max_value():
            GUIStatics.window_error(self, "Work In Progress...")

        def show_help():
            window_help = tk.Toplevel(self)
            window_help.title('HELP - SOLUTION')
            window_help.geometry(f"{800}x{600}")
            window_help.resizable(False, False)
            window_help.iconbitmap('tiny_fem_icon.ico')



        # Help Button
        tk.Button(self, text="HELP", command=show_help, width=8,
                                           font=GUIStatics.STANDARD_FONT_BUTTON_SMALL, height=1).place(relx=0.9, rely=0.025)
        # export solution as csv file button
        tk.Button(self, text="EXPORT CSV FILE", command=export_solution_csv, width=20,
                                           font=GUIStatics.STANDARD_FONT_BUTTON_BIG_BOLD, height=1).place(relx=widgets_x_start, rely=0.1)

        # save image button
        tk.Button(self, text="EXPORT IMAGE FILE", command=export_image, width=20,
                                           font=GUIStatics.STANDARD_FONT_BUTTON_BIG_BOLD, height=1).place(relx=widgets_x_start, rely=0.15)

        # get min/max value buttons
        tk.Button(self, text="MIN VAL", command=get_min_value, width=8,
                                           font=GUIStatics.STANDARD_FONT_BUTTON_MID, height=1).place(relx=widgets_x_start, rely=0.23)
        tk.Button(self, text="MIN VAL", command=get_min_value, width=8,
                                           font=GUIStatics.STANDARD_FONT_BUTTON_MID, height=1).place(relx=widgets_x_start + 0.095, rely=0.23)

    def convert_solution_to_string(self):

        x_values = self.nodes[:, 0]
        y_values = self.nodes[:, 1]
        sol_values = self.solution

        export_string = f"{'X-POSITION'.ljust(15)}{'Y-POSITION'.ljust(15)}{'SOLUTION'.ljust(15)}\n"
        for x, y, s in zip(x_values, y_values, sol_values):
            x_s = f"{x:.4f};".ljust(15)
            y_s = f"{y:.4f};".ljust(15)
            s_s = f"{s:.4f}".ljust(15)
            add = f"{x_s}{y_s}{s_s}\n"
            export_string += add
        return export_string



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
