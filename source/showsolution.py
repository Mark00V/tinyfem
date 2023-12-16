"""
#######################################################################
LICENSE INFORMATION
This file is part of TinyFEM.

TinyFEM is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

TinyFEM is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with TinyFEM. If not, see <https://www.gnu.org/licenses/>.
#######################################################################

#######################################################################
Description:
Plotting of solution and transformation of solution
#######################################################################
"""

import tkinter as tk
import math
from typing import Callable, Any
from tkinter import filedialog
import json
from source.guistatics import GUIStatics
import numpy as np
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.tri as tri
from mpl_toolkits.axes_grid1 import make_axes_locatable
from PIL import ImageTk
import datetime

class ShowSolution(tk.Toplevel):
    """
    Define Solution Window
    """

    def __init__(self, solution, nodes, triangulation, calculation_parameters):
        """
        Constructor, inherits from tk toplevel
        :param
        """

        # solution values
        self.solution = solution
        self.nodes = nodes
        self.triangulation = triangulation
        self.calculation_parameters = calculation_parameters
        self.solution_orig = solution

        # graphics settings
        self.levels = 20  # number of contours
        self.show_min_value = None

        super().__init__()
        self.set_icon(self)
        self.main_window_solution()

    def set_icon(self, root):
        """
        Creates Icon from raw byte data to not need external files for creating .exe
        :return:
        """
        icon_image = ImageTk.PhotoImage(data=GUIStatics.return_icon_bytestring())
        root.tk.call('wm', 'iconphoto', root._w, icon_image)

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

        # Create a Matplotlib figure
        self.fig, ax = self.create_mpl_fig()

        # canvas qith Matplotlib figure (canvas on top of canvas
        self.canvas_main = tk.Canvas(self, width=GUIStatics.CANVAS_SIZE_X, height=GUIStatics.CANVAS_SIZE_Y,
                                bg=GUIStatics.CANVAS_BG)
        self.canvas_main.place(relx=canvas_x + 0.0075, rely=canvas_y)
        GUIStatics.add_canvas_border(self.canvas_main)

        canvas_mpl = FigureCanvasTkAgg(self.fig, master=self)
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
            now = datetime.datetime.now().strftime('%Y_%m_%d_%H%M%S')
            file_path = f"fig_solution_{now}.png"
            self.fig.savefig(file_path, dpi=200)

        def get_min_value():
            min_value = min(self.solution)
            min_value_pos = np.where(self.nodes == min_value)
            print(min_value, min_value_pos)

            if self.show_min_value is not None:
                ...
            elif self.show_min_value is None:
                ...
                #
                # self.show_min = self.canvas_main.create_oval(node[0] - 10, node[1] - 10, node[0] + 10, node[1] + 10,
                #                                                  width=3, outline=GUIStatics.CANVAS_HIGHLIGHT_ELEMENT,
                #                                                  dash=(2, 1), fill='', tags='highlight_element')
                #

        def get_max_value():
            ...

        def show_help():
            window_help = tk.Toplevel(self)
            window_help.title('HELP - SOLUTION')
            window_help.geometry(f"{800}x{600}")
            window_help.resizable(False, False)
            self.set_icon(window_help)

        def show_spl():
            """
            this is ugly
            :return:
            """
            self.calculate_spl()
            self.fig, ax = self.create_mpl_fig(spl_flag=True)
            canvas_mpl = FigureCanvasTkAgg(self.fig, master=self)
            self.canvas_mpl_widget = canvas_mpl.get_tk_widget()
            self.canvas_mpl_widget.place(relx=canvas_x + 0.0075 + 0.003, rely=canvas_y + 0.006)

        def show_pressure():
            """
            this is also ugly
            :return:
            """
            self.solution = self.solution_orig
            self.fig, ax = self.create_mpl_fig()
            canvas_mpl = FigureCanvasTkAgg(self.fig, master=self)
            self.canvas_mpl_widget = canvas_mpl.get_tk_widget()
            self.canvas_mpl_widget.place(relx=canvas_x + 0.0075 + 0.003, rely=canvas_y + 0.006)


        # Help Button WIP
        # tk.Button(self, text="HELP", command=show_help, width=8,
        #                                    font=GUIStatics.STANDARD_FONT_BUTTON_SMALL, height=1).place(relx=0.9, rely=0.025)

        GUIStatics.create_divider(self, widgets_x_start, 0.08, 230)
        # export solution as csv file button
        tk.Button(self, text="EXPORT CSV FILE", command=export_solution_csv, width=20,
                                           font=GUIStatics.STANDARD_FONT_BUTTON_BIG_BOLD, height=1).place(relx=widgets_x_start, rely=0.1)

        # save image button
        tk.Button(self, text="EXPORT IMAGE FILE", command=export_image, width=20,
                                           font=GUIStatics.STANDARD_FONT_BUTTON_BIG_BOLD, height=1).place(relx=widgets_x_start, rely=0.15)

        GUIStatics.create_divider(self, widgets_x_start, 0.21, 230)
        # get min/max value buttons TODO: WIP
        tk.Button(self, text="MIN VAL", command=get_min_value, width=8,
                                           font=GUIStatics.STANDARD_FONT_BUTTON_MID, height=1).place(relx=widgets_x_start, rely=0.23)
        tk.Button(self, text="MAX VAL", command=get_max_value, width=8,
                                           font=GUIStatics.STANDARD_FONT_BUTTON_MID, height=1).place(relx=widgets_x_start + 0.095, rely=0.23)

        if self.calculation_parameters['equation'] == 'HH':
            tk.Button(self, text="SOUND PRESSURE LEVEL", command=show_spl, width=24,
                                               font=GUIStatics.STANDARD_FONT_BUTTON_MID, height=1).place(relx=widgets_x_start, rely=0.32)
            tk.Button(self, text="PRESSURE", command=show_pressure, width=24,
                                               font=GUIStatics.STANDARD_FONT_BUTTON_MID, height=1).place(relx=widgets_x_start, rely=0.36)
        GUIStatics.create_divider(self, widgets_x_start, 0.40, 230)

        # Graphics Setting
        def redraw(*args):
            self.levels = int(density_var.get())
            self.fig, ax = self.create_mpl_fig()
            canvas_mpl = FigureCanvasTkAgg(self.fig, master=self)
            self.canvas_mpl_widget = canvas_mpl.get_tk_widget()
            self.canvas_mpl_widget.place(relx=canvas_x + 0.0075 + 0.003, rely=canvas_y + 0.006)

        tk.Label(self, text="Density:", font=GUIStatics.STANDARD_FONT_SMALL_BOLD).place(relx=widgets_x_start, rely=0.425)
        dens_selection = [5, 10, 20, 40, 100]
        density_var = tk.StringVar()
        density_var.set(20)
        dropdown_density_select = tk.OptionMenu(self, density_var, *dens_selection)
        dropdown_density_select.config(font=GUIStatics.STANDARD_FONT_SMALL, width=4, height=1)
        dropdown_density_select.place(relx=0.075, rely=0.42)
        density_var.trace('w', redraw)

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

    def calculate_spl(self):
        """
        Calculates sound pressure level
        :return:
        """
        solution = self.solution_orig
        pref = 20 * 10 ** (-6)
        solutionspl = abs(20 * np.log10(solution / pref))
        self.solution = solutionspl

    def create_mpl_fig(self, spl_flag=False):
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

        title_text = 'None'
        legend_text = 'None'
        cmap = 'viridis'
        if self.calculation_parameters['equation'] == 'HE':
            title_text = 'Temperature Field'
            legend_text = '\nTemperature [K]'
            cmap = 'jet'
        elif self.calculation_parameters['equation'] == 'HH':
            if spl_flag:
                title_text = f'Sound Pressure Distribution @ {self.calculation_parameters["freq"]} Hz'
                legend_text = '\nSPL [dB]'
                cmap = 'inferno'
            else:
                title_text = f'Pressure Field @ {self.calculation_parameters["freq"]} Hz'
                legend_text = '\nPressure [Pa]'
                cmap = 'cool'

        fig = Figure(figsize=(9.15, 7.15), dpi=100, facecolor='lightgray')
        ax = fig.add_subplot(111)
        label_font_title = {'fontsize': 14, 'fontfamily': 'sans-serif'}
        ax.set_title(title_text, **label_font_title)
        label_font_axes = {'fontsize': 12, 'fontfamily': 'sans-serif'}
        ax.set_xlabel(f'x [{self.calculation_parameters["units"]}]', **label_font_axes)
        ax.set_ylabel(f'y [{self.calculation_parameters["units"]}]', **label_font_axes)
        ax.set_aspect(aspectxy)

        contour = ax.tricontourf(triang_mpl, values, cmap=cmap, levels=self.levels)
        ax.set_facecolor('lightgray')  # backgroundcolor of contourmap
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.2)

        legend = fig.colorbar(contour, cax=cax)
        legend.set_label(legend_text)
        ax.scatter(all_points[:, 0], all_points[:, 1], c=values, cmap=cmap, marker='.', s=1)
        ax.triplot(triang_mpl, 'w-', linewidth=0.1)

        return fig, ax

if __name__ == '__main__':

    solution = np.array([1.5, 1.0, 1.0, 1.75, 2.0, 2.0])
    nodes = np.array([[0.0, 0.0], [0.5, 0.0], [1.0,  0.0], [1.0, 0.5], [1.0,  1.0], [0.5, 0.5]])
    triangles = np.array([[1., 5., 0.], [5., 3., 4.], [1., 3., 5.], [3., 1., 2.]])
    calculation_parameters = {'mesh_density': None, 'freq': 300, 'equation': 'HH', 'units': 'm'}
    show_solution = ShowSolution(solution, nodes, triangles, calculation_parameters)  # Develop
    show_solution.mainloop()
