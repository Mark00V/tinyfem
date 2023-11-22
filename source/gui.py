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
Main file for starting GUI
#######################################################################
"""

import math
import random
import threading
import time
import tkinter as tk
from source.calcfem import CalcFEM
from source.definebcs import CreateBCParams
from source.geometry import Geometry
from source.guistatics import GUIStatics, Tooltip
from source.meshgen import CreateMesh
from source.showsolution import ShowSolution
from PIL import ImageTk
import numpy as np

#################################################
# Other
AUTHOR = 'Elias Perras, Marius Mellmann'
VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 0
#################################################


class GUI(tk.Tk):
    """
    main class for calling other classes geometry, mesh creation, calculation and output
    """

    def __init__(self):
        """
        Constructor, inherits from tkinter
        """
        # output variable for geometry
        self.geometry_input = None  # output of geometry creation, callback variable for reformating geometry via class CreateBCParams
        # Definitions after formatting from CreateBCParams
        self.regions = None
        self.boundaries = None
        self.nodes = None
        # definitions for setting BCs, Mats etc. init in init_parameters() when geometry was created
        self.equation = None  # HE for heat equation, HH for helmholtz equation
        self.region_parameters = None  # saves materials, area_neg_pos, nodes, number for regions
        self.boundary_parameters = None  # saves dirichlet/neumann/robin values and setting, nodes, number for boundaries
        self.node_parameters = None  # saves node number, coords, neumann value for nodes
        self.calculation_parameters = None  # save calculation parameters, mesh density etc
        # output from CreateMesh after clicking button Create Mesh
        self.nodes_mesh_gen = None
        self.single_nodes_dict = None
        self.boundary_nodes_dict = None
        self.triangulation = None
        self.triangulation_region_dict = None

        # some output for user
        self.text_information_str = ''
        ##################################################
        # for development
        self.DEV = False  # set to True for DEV mode
        if self.DEV:
            self.regions = {'0': {'coordinates' : [(-4.0, -3.0), (1.0, -2.5), (2.5, 1.0), (-2.5, 1.0), (-4.2, -1.5)],
                                  'area_neg_pos': 'Positive'},
                            '1': {'coordinates': [(2.5, 1.0), (0.0, 3.0), (-2.5, 1.0)], 'area_neg_pos': 'Positive'},
                            '2': {'coordinates' : [(-1.0, 0.0), (0.0, 0.0), (0.0, 0.75), (-1.0, 0.5)],
                                  'area_neg_pos': 'Negative'}}
            self.boundaries = {'0' : ((-4.0, -3.0), (1.0, -2.5)), '1': ((1.0, -2.5), (2.5, 1.0)),
                               '2' : ((2.5, 1.0), (-2.5, 1.0)), '3': ((-2.5, 1.0), (-4.2, -1.5)),
                               '4' : ((-4.2, -1.5), (-4.0, -3.0)), '5': ((2.5, 1.0), (0.0, 3.0)),
                               '6' : ((0.0, 3.0), (-2.5, 1.0)), '7': ((-1.0, 0.0), (0.0, 0.0)),
                               '8' : ((0.0, 0.0), (0.0, 0.75)), '9': ((0.0, 0.75), (-1.0, 0.5)),
                               '10': ((-1.0, 0.5), (-1.0, 0.0))}
            self.nodes = {'0' : (-3.0, -2.0), '1': (0.0, 1.5), '2': (1.0, -1.0), '3': (-4.0, -3.0), '4': (1.0, -2.5),
                          '5' : (2.5, 1.0), '6': (-2.5, 1.0), '7': (-4.2, -1.5), '8': (0.0, 3.0), '9': (-1.0, 0.0),
                          '10': (0.0, 0.0), '11': (0.0, 0.75), '12': (-1.0, 0.5)}
        # for development
        ##################################################
        super().__init__()
        self.set_icon(self)
        # Start Main Window
        self.main_window()

    def set_icon(self, root):
        """
        Creates Icon from raw byte data to not need external files for creating .exe
        :return:
        """
        icon_image = ImageTk.PhotoImage(data=GUIStatics.return_icon_bytestring())
        root.tk.call('wm', 'iconphoto', root._w, icon_image)

    def main_window(self):
        """
        Defines Main Window
        :return:
        """


        print("Starting...Please wait.")  # Console output when running as .exe

        self.title('TinyFEM - MAIN WINDOW')
        self.geometry(f"{GUIStatics.MAIN_WINDOW_SIZE_X}x{GUIStatics.MAIN_WINDOW_SIZE_Y}")
        self.resizable(False, False)
        ##################################################
        # Position of elements
        # canvas
        border = 0.025
        canvas_x = 1 - GUIStatics.CANVAS_SIZE_X / GUIStatics.GEOM_WINDOW_SIZE_X - border
        canvas_y = 1 - GUIStatics.CANVAS_SIZE_Y / GUIStatics.GEOM_WINDOW_SIZE_Y - border

        # buttons and text on left side
        widgets_x_start = 0.01
        ##################################################

        ##################################################
        # Add canvas for visualization of geometry, boundaries, mesh...
        self.animation = True  # Start Main window canvas with animation cause ppl like animations :)

        def animate():
            """
            Starting screen animation j4f
            people like animations :)
            """

            if self.animation:
                all_canvas_elements = self.canvas.find_all()
                if len(all_canvas_elements) > 60:
                    for elem in all_canvas_elements[:6]:
                        self.canvas.delete(elem)
                    GUIStatics.add_canvas_border(self.canvas)
                pos_x = math.floor(random.random() * GUIStatics.CANVAS_SIZE_X)
                pos_y = math.floor(random.random() * GUIStatics.CANVAS_SIZE_Y)
                size_x = math.floor(random.random() * 300)
                size_y = math.floor(random.random() * 220)
                if size_x < 30:
                    size_x = 30
                if size_y < 20:
                    size_y = 20
                width = random.choice(['1', '2', '3', '4'])
                color = random.choice(
                        ['#383334', '#584043', '#8D565B', '#D5B7BA', '#A14750', '#582026', '#402628', '#870C18'])
                self.canvas.create_rectangle(pos_x - size_x, pos_y - size_y, pos_x + size_x, pos_y + size_y,
                                             fill="", outline=color, width=width, dash=(6, 1), activefill=color)
                self.canvas.create_text(175, GUIStatics.CANVAS_SIZE_Y - 75, text='ENTER GEOMETRY\n     TO START... :)',
                                        fill='Gray', font=("Helvetica", 22))
                self.canvas.after(150, animate)
            else:
                return None

        self.canvas = tk.Canvas(self, width=GUIStatics.CANVAS_SIZE_X, height=GUIStatics.CANVAS_SIZE_Y,
                                bg=GUIStatics.CANVAS_BG)
        self.canvas.place(relx=canvas_x + 0.0075, rely=canvas_y)
        GUIStatics.add_canvas_border(self.canvas)
        self.canvas.create_rectangle(10, 10, 50, 50, fill="", outline="gray")
        animate()

        ##################################################
        self.equation = 'HE'  # Initialized value for equation
        ##################################################
        # Buttons
        def assign_BCs():
            """
            Button action, calls window to assign Boundary conditions
            :return:
            """
            self.window_assign_boundary_conditions()

        def assign_materials():
            """
            Button action, calls window to assign Materials
            :return:
            """
            self.window_assign_region_conditions()

        def assign_calc_params():
            """
            Button action, calls window to assign Calculation Parameters
            :return:
            """
            self.window_assign_calculation_params()

        def create_mesh():
            """
            Button action, creates mesh. Calls window during wait time via thread
            :return:
            """

            def thread_create_mesh():
                """
                Helper function for thread
                :return:
                """
                try:
                    mesh = CreateMesh(self.region_parameters, self.boundary_parameters,
                                      self.node_parameters, self.calculation_parameters)
                    mesh_generator_output = mesh.create_mesh()
                    self.nodes_mesh_gen = mesh_generator_output[0]
                    self.single_nodes_dict = mesh_generator_output[1]
                    self.boundary_nodes_dict = mesh_generator_output[2]
                    self.triangulation = mesh_generator_output[3]
                    self.triangulation_region_dict = mesh_generator_output[4]
                except IndexError:
                    GUIStatics.window_error(self, '        MESHING ERROR         \n'
                                                               'Mesh could not be generated! \n'
                                                               'Check geometry!              \n')

            window_create_mesh_wait = tk.Toplevel(self)
            window_create_mesh_wait.title('CREATING MESH')
            window_create_mesh_wait.geometry(f"{200}x{150}")
            window_create_mesh_wait.resizable(False, False)
            icon_image = ImageTk.PhotoImage(data=GUIStatics.return_icon_bytestring())
            window_create_mesh_wait.tk.call('wm', 'iconphoto', window_create_mesh_wait._w, icon_image)
            tk.Label(window_create_mesh_wait, text="Creating Mesh...\nPlease Wait",
                     font=GUIStatics.STANDARD_FONT_MID_BOLD).place(relx=0.15, rely=0.1)
            window_create_mesh_wait_label = tk.Label(window_create_mesh_wait, text="",
                                                     font=GUIStatics.STANDARD_FONT_MID_BOLD)
            window_create_mesh_wait_label.place(relx=0.35, rely=0.6)
            thread_mesh = threading.Thread(target=thread_create_mesh)
            thread_mesh.start()

            self.button_solve_system.config(state="normal")

            def update_wait_label():
                """
                Helper function to update text in window appearing when mesh is calculated
                :return:
                """
                wait_text = ''
                while thread_mesh.is_alive():
                    if wait_text == '.....':
                        wait_text = ''
                    wait_text += '.'
                    window_create_mesh_wait_label.config(text=wait_text)
                    time.sleep(0.5)
                window_create_mesh_wait.destroy()

            update_thread = threading.Thread(target=update_wait_label)
            update_thread.start()
            button_show_mesh.config(state='normal')

        def show_mesh():
            """
            Button action to show mesh (not automatically shown since threading too slow)
            :return:
            """
            self.draw_mesh_from_mesh_output()

        def show_geometry():
            """
            Button action to show geometry and boundaries instead of mesh in GUI mainwindow
            :return:
            """
            self.draw_geometry_from_definebcs()

        def solve_system():
            """
            Button action to start FEM calculation and show window for displaying solution
            TODO: threading during waittime
            :return:
            """

            def thread_solve_system():
                """
                Helper function for thread
                :return:
                """
                if self.calculation_parameters['equation'] == 'HH' and not self.calculation_parameters['freq']:
                    GUIStatics.window_error(self, 'Please set frequency first!')
                    return
                params_mesh = (
                self.nodes_mesh_gen, self.single_nodes_dict, self.boundary_nodes_dict, self.triangulation,
                self.triangulation_region_dict)
                params_boundaries_materials = (
                        self.region_parameters, self.boundary_parameters, self.node_parameters,
                        self.calculation_parameters)
                try:
                    calcfem = CalcFEM(params_mesh, params_boundaries_materials)
                    self.solution = calcfem.calc_fem()
                except np.linalg.LinAlgError:
                    err_message = ('Singular Matrix encountered!\n'
                                   'Check Boundary Conditions \n'
                                   'and/or \n'
                                   'try lower/higher mesh density.')
                    GUIStatics.window_error(self, err_message)
                    return None
                except np.core._exceptions._ArrayMemoryError:
                    err_message = ('Mesh too large!\n'
                                   '(Sparse matrix calculation WIP)\n'
                                   'Try lower mesh density.')
                    GUIStatics.window_error(self, err_message)
                    return None

                ShowSolution(self.solution, self.nodes_mesh_gen, self.triangulation,
                             self.calculation_parameters)  # opens window for solution

            window_solve_system_wait = tk.Toplevel(self)
            window_solve_system_wait.title('SOLVING')
            window_solve_system_wait.geometry(f"{200}x{150}")
            window_solve_system_wait.resizable(False, False)
            icon_image = ImageTk.PhotoImage(data=GUIStatics.return_icon_bytestring())
            window_solve_system_wait.tk.call('wm', 'iconphoto', window_solve_system_wait._w, icon_image)
            tk.Label(window_solve_system_wait, text="Solving System...\nPlease Wait",
                     font=GUIStatics.STANDARD_FONT_MID_BOLD).place(relx=0.15, rely=0.1)
            window_solve_system_wait_label = tk.Label(window_solve_system_wait, text="",
                                                     font=GUIStatics.STANDARD_FONT_MID_BOLD)
            window_solve_system_wait_label.place(relx=0.35, rely=0.6)
            thread_mesh = threading.Thread(target=thread_solve_system)
            thread_mesh.start()

            def update_wait_label():
                """
                Helper function to update text in window appearing when mesh is calculated
                :return:
                """
                wait_text = ''
                while thread_mesh.is_alive():
                    if wait_text == '.....':
                        wait_text = ''
                    wait_text += '.'
                    window_solve_system_wait_label.config(text=wait_text)
                    time.sleep(0.5)
                window_solve_system_wait.destroy()

            update_thread = threading.Thread(target=update_wait_label)
            update_thread.start()

        # Button define Geometry
        tk.Frame(self, height=2, width=230, bg=GUIStatics.CANVAS_BORDER_COLOR) \
            .place(relx=widgets_x_start, rely=0.08)
        button_define_geometry = tk.Button(self, text="GEOMETRY", command=self.define_geometry, width=12,
                                           font=GUIStatics.STANDARD_FONT_BUTTON_BIG_BOLD, height=1)
        button_define_geometry.place(relx=widgets_x_start, rely=0.1)

        def show_help():
            """
            Button action to show help window for GUI
            :return:
            """
            window_help = tk.Toplevel(self)
            window_help.title('HELP - MAIN')
            window_help.geometry(f"{800}x{600}")
            window_help.resizable(False, False)
            self.set_icon(window_help)

            help_txt_t = f"Welcome to TinyFEM"
            help_txt_author_version = (f"Authors: {AUTHOR}\n"
                                       f"Version: {VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}")
            help_txt_inst = (f"1) Click Button GEOMETRY to define geometry in GEOMETRY EDITOR\n\n"
                             f"2) After defining geometry select equation to solve\n"
                             f"   Heat Equation: Solves the stationary coupled heat equation -> T = d^2(T)/d(T^2)\n"
                             f"   Helmholtz Equation: Solves the coupled Helmholtz equation -> d^2(P)/d(P^2) = -k^2 P\n\n"
                             f"3) Select Boundary by clicking Button BOUNDARY CONDITIONS\n"
                             f"   Select Boundary and Boundary Condition -> Dirichlet: Static values on Boundary\n"
                             f"                               -> Neumann:   Flux on Boundary (WIP, not implemented yet)\n"
                             f"   Input value and click SET VALUE\n"
                             f"   Click ACCEPT BCs when finished\n\n"
                             f"4) Select Material Parameters by clicking Button MATERIAL PARAMETERS\n"
                             f"   Select region, input value and click SET VALUE\n"
                             f"   Click ACCEPT REGIONs when finished\n\n"
                             f"5) Set Calculation Parameters by clicking Button CALCULATION PARAMETERS\n"
                             f"   Select Mesh Density (1: very coarse, 2: coarse, 3: medium, 4: fine, 5: very fine\n"
                             f"   If Helmholtz Equation is selected, set frequency\n"
                             f"   Click ACCEPT CALCULATION PARAMETERS when finished\n\n"
                             f"6) Click CREATE MESH\n"
                             f"   Click SHOW MESH to display mesh\n\n"
                             f"7) Click SOLVE to start FEM-Solver and open solution window\n")

            tk.Label(window_help, text=help_txt_t, font=GUIStatics.STANDARD_FONT_BIGGER_BOLD, anchor="center",
                     justify="center") \
                .place(relx=0.1, rely=0.025)
            tk.Label(window_help, text=help_txt_author_version, font=GUIStatics.STANDARD_FONT_MID, anchor="center",
                     justify="left") \
                .place(relx=0.1, rely=0.08)
            tk.Label(window_help, text='Instructions', font=GUIStatics.STANDARD_FONT_BIG_BOLD, anchor="w",
                     justify="left") \
                .place(relx=0.1, rely=0.155)
            tk.Label(window_help, text=help_txt_inst, font=GUIStatics.STANDARD_FONT_MID, anchor="w", justify="left") \
                .place(relx=0.1, rely=0.21)
            lic_text = ("TinyFEM is licensed under the GNU GENERAL PUBLIC LICENSE Version 3\n"
                        "No warranty of any kind is given for accuracy and correctness of the results.\n"
                        "Any use is solely at the user's discretion. Commercial use is not recommended.")

            tk.Label(window_help, text=lic_text, font=GUIStatics.STANDARD_FONT_SMALL, anchor="w", justify="left") \
                .place(relx=0.1, rely=0.85)

        # not necessary
        def show_license():
            """
            Button action to show help window for GUI
            :return:
            """
            window_lic = tk.Toplevel(self)
            window_lic.title('LICENSE INFORMATION')
            window_lic.geometry(f"{800}x{600}")
            window_lic.resizable(False, False)
            self.set_icon(window_lic)

            lic_info_str = ('LICENSE INFORMATION - TinyFEM and included libraries\n\n'
                            'TinyFEM uses the following external libraries:\n'
                            'PIL, NUMPY, ZLIB, MATPLOTLIB, SCIPY\n'
                            'License information is included below (please scroll down)\n\n')
            lics = GUIStatics.return_license_info()
            lic_info_str += lics

            lic_info = tk.Text(window_lic, height=38, width=108, wrap=tk.WORD,
                                            font=GUIStatics.STANDARD_FONT_SMALL, bg='light gray', fg='black')
            lic_info.place(relx=0.025, rely=0.05)
            lic_info.insert(tk.END, lic_info_str)
            lic_info.config(state='disabled')


        # Help Button
        tk.Button(self, text="HELP", command=show_help, width=7,
                  font=GUIStatics.STANDARD_FONT_BUTTON_SMALL, height=1).place(relx=0.92, rely=0.025)

        # License Button, not necessary
        # tk.Button(self, text="LICENSE", command=show_license, width=7,
        #           font=GUIStatics.STANDARD_FONT_BUTTON_SMALL, height=1).place(relx=0.85, rely=0.025)

        # Button show Mesh and show Geometry
        button_show_mesh = tk.Button(self, text="SHOW MESH", command=show_mesh, width=12,
                                     font=GUIStatics.STANDARD_FONT_BUTTON_MID, height=1, state='disabled')
        button_show_mesh.place(relx=0.23, rely=0.035)
        self.button_show_geom = tk.Button(self, text="SHOW GEOMETRY", command=show_geometry, width=12,
                                          font=GUIStatics.STANDARD_FONT_BUTTON_MID, height=1, state='disabled')
        self.button_show_geom.place(relx=0.34, rely=0.035)

        # FEM Parameters
        GUIStatics.create_divider(self, widgets_x_start, 0.17, 230)
        tk.Label(self, text="FEM PARAMETERS", font=GUIStatics.STANDARD_FONT_MID_BOLD) \
            .place(relx=widgets_x_start, rely=0.175)

        # Dropdown select equation
        def trace_equation(*args):
            """
            Tracer function for equation selector
            :param args:
            :return:
            """
            equation_selected = var_equations.get()
            equation_dict = {'Heat Equation': 'HE', 'Helmholtz Equation': 'HH'}
            self.equation = equation_dict[equation_selected]

        tk.Label(self, text="Equation: ", font=GUIStatics.STANDARD_FONT_MID) \
            .place(relx=widgets_x_start, rely=0.22)
        equations = ['Heat Equation', 'Helmholtz Equation']
        var_equations = tk.StringVar()
        var_equations.set(equations[0])  # default value m
        dropdown_equation_select = tk.OptionMenu(self, var_equations, *equations)
        dropdown_equation_select.config(font=GUIStatics.STANDARD_FONT_SMALL, width=15, height=1)
        dropdown_equation_select.place(relx=widgets_x_start + 0.065, rely=0.215)
        var_equations.trace('w', trace_equation)
        tooltip_text_dropdown_equation_select = 'None'
        if self.equation == 'HE':
            tooltip_text_dropdown_equation_select = (f" Solves the stationary Heat Equation ")
        elif self.equation == 'HH':
            tooltip_text_dropdown_equation_select = (f" Solves the Helmholtz Equation ")
        Tooltip(dropdown_equation_select, tooltip_text_dropdown_equation_select)


        # Button Assign Boundary Conditions /Material Parameters / Calculation Parameters
        self.button_define_bcs = tk.Button(self, text="BOUNDARY CONDITIONS", command=assign_BCs, width=25,
                                           font=GUIStatics.STANDARD_FONT_BUTTON_MID, height=1)
        self.button_define_bcs.place(relx=widgets_x_start, rely=0.27)
        self.button_define_materials = tk.Button(self, text="MATERIAL PARAMETERS", command=assign_materials, width=25,
                                                 font=GUIStatics.STANDARD_FONT_BUTTON_MID, height=1)
        self.button_define_materials.place(relx=widgets_x_start, rely=0.27 + 0.045)
        self.button_define_calc_params = tk.Button(self, text="CALCULATION PARAMETERS", command=assign_calc_params,
                                                   width=25,
                                                   font=GUIStatics.STANDARD_FONT_BUTTON_MID, height=1)
        self.button_define_calc_params.place(relx=widgets_x_start, rely=0.27 + 0.09)
        self.button_define_bcs.config(state="disabled")
        self.button_define_materials.config(state="disabled")
        self.button_define_calc_params.config(state="disabled")

        # buttons create mesh, solve system
        GUIStatics.create_divider(self, widgets_x_start, 0.41, 230)
        self.button_create_mesh = tk.Button(self, text="CREATE\nMESH", command=create_mesh, width=10,
                                            font=GUIStatics.STANDARD_FONT_BUTTON_MID_BOLD, height=2)
        self.button_create_mesh.place(relx=widgets_x_start, rely=0.41 + 0.012)
        self.button_solve_system = tk.Button(self, text="SOLVE", command=solve_system, width=10,
                                             font=GUIStatics.STANDARD_FONT_BUTTON_MID_BOLD, height=2)
        self.button_solve_system.place(relx=widgets_x_start + 0.1075, rely=0.41 + 0.012)
        self.button_create_mesh.config(state="disabled")
        self.button_solve_system.config(state="disabled")

        # info field
        def show_info():
            """
            Shows more information in separate window
            :return:
            """
            window_info= tk.Toplevel(self)
            window_info.title('INFO')
            window_info.geometry(f"{800}x{600}")
            window_info.resizable(False, False)
            self.set_icon(window_info)

            region_parameters = self.region_parameters
            boundary_parameters = self.boundary_parameters
            node_parameters = self.node_parameters
            calculation_parameters = self.calculation_parameters
            region_parameters_str = 'REGIONS:'
            if region_parameters:
                for k, v in region_parameters.items():
                    coordinates = v['coordinates']
                    area_neg_pos = v['area_neg_pos']
                    mat_k = v['material']['k']
                    mat_c = v['material']['c']
                    mat_rho = v['material']['rho']
                    mats = f"k = {mat_k} W/mK" if calculation_parameters['equation'] == 'HH' else f"c = {mat_c} m/s     rho = {mat_rho} kg/m³"
                    region_parameters_str += f"\nRegion R-{k}: {area_neg_pos}\n"
                    if area_neg_pos == 'Positive':
                        region_parameters_str += f"Materials: {mats}\n"
                    region_parameters_str += 'Nodes:'
                    for nc, coord in enumerate(coordinates):
                        region_parameters_str += f"N[{nc}] = {coord}     "
                        if nc in {4, 8, 12, 16, 20}:
                            region_parameters_str += '\n'

            calculation_parameters_str = 'CALCULATION PARAMETERS:'
            if calculation_parameters:
                eq = {'HH': 'Helmholtz Equation',
                      'HE': 'Heat Equation'}
                freq_st = ''
                if calculation_parameters['equation'] == 'HH':
                    freq_st = f"\nFrequency: {calculation_parameters['freq']} Hz"
                calculation_parameters_str += (f"\nEquation: {eq[calculation_parameters['equation']]}\n"
                                               f"Mesh Density: {calculation_parameters['mesh_density']}{freq_st}")
            if self.triangulation is not None:
                calculation_parameters_str += f"\nMesh created with {len(self.triangulation)} elements."

            boundary_parameters_str = 'BOUNDARIES:'
            try:
                if boundary_parameters:
                    for k, v in boundary_parameters.items():
                        coordinates = v['coordinates']
                        bc = v['bc']
                        bc_str = ''
                        if self.equation == 'HE':
                            if bc['type'] == 'Dirichlet':
                                bc_str = f"{bc['type']}, T = {bc['value']} K"
                            elif bc['type'] == 'Neumann':
                                bc_str = f"{bc['type']}, q = {bc['value']} W/m²"
                            elif bc['type'] == 'Robin':
                                bc_str = f"{bc['type']}, T_ext = {bc['value'][0]} K, h = {bc['value'][1]} W/m²K"
                            else:
                                bc_str = f"No BC specified"
                        elif self.equation == 'HH':
                            if bc['type'] == 'Dirichlet':
                                bc_str = f"{bc['type']}, T = {bc['value']} Pa"
                            elif bc['type'] == 'Neumann':
                                bc_str = f"{bc['type']}, T = {bc['value']} Pas/m"
                            elif bc['type'] == 'Robin':
                                bc_str = f"No BC specified"
                            else:
                                bc_str = f"No BC specified"
                        boundary_parameters_str += f"\nB-{k}: N[0] = {coordinates[0]}   N[1] = {coordinates[1]}     {bc_str}"

            except KeyError:
                ...
            except IndexError:
                ...

            node_parameters_str = 'NODES:'
            if node_parameters:
                for k, v in node_parameters.items():
                    coordinates = v['coordinates']
                    bc = v['bc']['value']
                    bc_str = ''
                    if bc:
                        bc_str = f"Sound source, P = {bc} W/m"

                    node_parameters_str += f"\nN-{k}: N = {coordinates}     {bc_str}"

            info_string_detailed = (f"CURRENT INPUT:\n"
                                    f"{'_' * 107}"
                                    f"{calculation_parameters_str}\n\n"
                                    f"{'_' * 107}"
                                    f"{region_parameters_str}\n\n"
                                    f"{'_' * 107}"
                                    f"{boundary_parameters_str}\n\n"
                                    f"{'_' * 107}"
                                    f"{node_parameters_str}\n\n"
                                    f"{'_' * 107}")

            info_field = tk.Text(window_info, height=36, width=108, wrap=tk.WORD,
                                            font=GUIStatics.STANDARD_FONT_SMALL, bg='light gray', fg='black')
            info_field.place(relx=0.025, rely=0.05)
            info_field.insert(tk.END, info_string_detailed)
            info_field.config(state='disabled')

        def write_info():
            """
            Writes info to file, e.g. for testing modules
            :return:
            """
            self.debug()

        self.text_information_str = 'None'
        GUIStatics.create_divider(self, widgets_x_start, 0.5, 230)
        tk.Label(self, text="Information: ", font=GUIStatics.STANDARD_FONT_MID_BOLD) \
            .place(relx=widgets_x_start, rely=0.505)
        self.text_information = tk.Text(self, height=24, width=44, wrap=tk.WORD,
                                        font=GUIStatics.STANDARD_FONT_SMALLEST, bg='light gray', fg='black')
        self.text_information.place(relx=widgets_x_start + 0.005, rely=0.54)
        self.text_information.insert(tk.END, self.text_information_str)
        self.text_information.config(state='disabled')
        tk.Button(self, text="SHOW INFO", command=show_info, width=12, font=GUIStatics.STANDARD_FONT_BUTTON_MID, height=1).place(relx=widgets_x_start, rely=0.925)
        tk.Button(self, text="WRITE INFO", command=write_info, width=12, font=GUIStatics.STANDARD_FONT_BUTTON_MID, height=1).place(relx=widgets_x_start + 0.1, rely=0.925)

        # Debug
        # Reformat Boundaryconditions via CreateBCParams, only needed for development
        # button_create_bc = tk.Button(self, text="FORM BCS", command=self.create_BC_params, width=10,
        #                              height=1, font=('Arial', 6))
        # button_create_bc.place(relx=0.01, rely=0.01)
        button_debug = tk.Button(self, text="DEBUG", command=self.debug, width=10,
                                 height=1, font=('Arial', 6))
        button_debug.place(relx=0.07, rely=0.01)

        ##################################################
        # Developing
        # placeholder for text FOR DEVELOPING
        # self.text_label = tk.Label(self, text="Init")
        # self.text_label.place(relx=0.02, rely=0.965)

        # Developing -> uncomment self.regions etc. in init!
        if self.DEV:
            self.animation = False  # todo delete this
            self.init_parameters()  # todo delete this
            self.draw_geometry_from_definebcs()  # todo delete this
        # Developing
        ##################################################

    def window_assign_calculation_params(self):
        """
        opens top window to assign calculation parameters
        """

        def set_freq():
            """
            Button action for setting frequency if HH eqution is selected
            :return:
            """
            if self.equation == 'HH':
                self.calculation_parameters['freq'] = entry_freq_var.get()

        window_calc_params = tk.Toplevel(self)
        window_calc_params.title('ASSIGN CALCULATION PARAMETERS')
        window_calc_params.geometry(f"{350}x{500}")
        window_calc_params.resizable(False, False)
        self.set_icon(window_calc_params)

        widgets_x_start = 0.01
        GUIStatics.create_divider(window_calc_params, widgets_x_start, 0.05, 335)
        tk.Label(window_calc_params, text="Calculation Parameters", font=GUIStatics.STANDARD_FONT_MID_BOLD) \
            .place(relx=widgets_x_start, rely=0.075)

        tk.Label(window_calc_params, text="Mesh Density:", font=GUIStatics.STANDARD_FONT_SMALL) \
            .place(relx=widgets_x_start + 0.025, rely=0.16)

        density_slider = tk.Scale(window_calc_params, from_=1, to=5, orient=tk.HORIZONTAL,
                                  label="", font=GUIStatics.STANDARD_FONT_SMALL)
        density_slider.place(relx=widgets_x_start + 0.325, rely=0.125)

        if self.equation == 'HH':
            GUIStatics.create_divider(window_calc_params, widgets_x_start, 0.3, 335)
            tk.Label(window_calc_params, text="Frequency:", font=GUIStatics.STANDARD_FONT_SMALL) \
                .place(relx=widgets_x_start + 0.025, rely=0.325)
            entry_freq_var = tk.StringVar()
            entry_freq_var.set('0')
            entry_freq_field = tk.Entry(window_calc_params, textvariable=entry_freq_var,
                                        font=GUIStatics.STANDARD_FONT_SMALL, width=8)
            entry_freq_field.place(relx=widgets_x_start + 0.025 + 0.3, rely=0.325)
            button_freq_set = tk.Button(window_calc_params, text="SET VALUE", command=set_freq,
                                        width=12, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALL)
            button_freq_set.place(relx=widgets_x_start + 0.6, rely=0.325)

        def accept_calcparams():
            """
            Button action for setting calculation parameters
            :return:
            """
            self.calculation_parameters['mesh_density'] = density_slider.get()
            self.init_information_text_field()
            self.text_information_str += '\n\nCalculation Parameters:\n'
            self.text_information_str += f"Mesh Density: {self.calculation_parameters['mesh_density']}\n"
            if self.equation == 'HH':
                self.text_information_str += f"Frequency: {self.calculation_parameters['freq']}\n"
            GUIStatics.update_text_field(self.text_information, self.text_information_str)
            window_calc_params.destroy()  # closes top window
            self.button_create_mesh.config(state="normal")
            self.calculation_parameters['equation'] = self.equation

        button_accept = tk.Button(window_calc_params, text="ACCEPT PARAMETERs", command=accept_calcparams,
                                  width=19, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_MID_BOLD)
        button_accept.place(relx=widgets_x_start + 0.05, rely=0.895)

    def window_assign_region_conditions(self):
        """
        opens top window to assign region parameters (materials) to regions
        """

        def trace_region(*args):
            """
            trace variable dropdown_region_select_var
            :param args:
            :return:
            """
            region_nbr = dropdown_region_select_var.get().split('R-')[-1]
            entry_materials_values_button.config(state='normal')
            if self.equation == 'HE':
                value_set_k = self.region_parameters[region_nbr]['material']['k']
                entry_material_k_value.set(str(value_set_k))
            elif self.equation == 'HH':
                value_set_c = self.region_parameters[region_nbr]['material']['c']
                value_set_rho = self.region_parameters[region_nbr]['material']['rho']
                entry_material_c_value.set(str(value_set_c))
                entry_material_rho_value.set(str(value_set_rho))

        def set_region_values():
            """
            sets the values for the regions for relevant materials
            :return:
            """
            region_nbr = dropdown_region_select_var.get().split('R-')[-1]
            if self.equation == 'HE':
                entry_k = entry_material_k_value.get()
                try:
                    entry_k = float(entry_k)
                except ValueError:
                    entry_k = 1.0
                self.region_parameters[region_nbr]['material']['k'] = entry_k
            elif self.equation == 'HH':
                entry_c = entry_material_c_value.get()
                entry_rho = entry_material_rho_value.get()
                try:
                    entry_c = float(entry_c)
                except ValueError:
                    entry_c = 1.0
                try:
                    entry_rho = float(entry_rho)
                except ValueError:
                    entry_rho = 1.0
                self.region_parameters[region_nbr]['material']['c'] = entry_c
                self.region_parameters[region_nbr]['material']['rho'] = entry_rho

        window_bcs = tk.Toplevel(self)
        window_bcs.title('ASSIGN MATERIALS PARAMETERS')
        window_bcs.geometry(f"{350}x{500}")
        window_bcs.resizable(False, False)
        self.set_icon(window_bcs)

        widgets_x_start = 0.01
        GUIStatics.create_divider(window_bcs, widgets_x_start, 0.05, 335)
        tk.Label(window_bcs, text="Materials", font=GUIStatics.STANDARD_FONT_MID_BOLD) \
            .place(relx=widgets_x_start, rely=0.075)
        tk.Label(window_bcs, text="Select Region", font=GUIStatics.STANDARD_FONT_MID) \
            .place(relx=widgets_x_start + 0.025, rely=0.125)

        regions = [f"R-{nbr}" for nbr in self.region_parameters.keys()]
        dropdown_region_select_var = tk.StringVar()
        dropdown_region_select_var.set('None')
        dropdown_region_select = tk.OptionMenu(window_bcs, dropdown_region_select_var, *regions)
        dropdown_region_select.config(font=GUIStatics.STANDARD_FONT_SMALL, width=8, height=1)
        dropdown_region_select.place(relx=widgets_x_start + 0.025, rely=0.18)
        dropdown_region_select_var.trace('w', trace_region)

        tk.Label(window_bcs, text="Material Parameters:", font=GUIStatics.STANDARD_FONT_SMALL) \
            .place(relx=widgets_x_start + 0.025, rely=0.27)

        if self.equation == 'HE':
            tk.Label(window_bcs, text="Heat conductivity k [W/mK]:", font=GUIStatics.STANDARD_FONT_SMALL) \
                .place(relx=widgets_x_start + 0.025, rely=0.33)
            entry_material_k_value = tk.StringVar()
            entry_material_k_value.set('0')
            entry_material_k_value_field = tk.Entry(window_bcs, textvariable=entry_material_k_value,
                                                    font=GUIStatics.STANDARD_FONT_SMALL, width=8)
            entry_material_k_value_field.place(relx=widgets_x_start + 0.025 + 0.5, rely=0.33)
            pos_y_set_button = 0.33

        elif self.equation == 'HH':
            tk.Label(window_bcs, text="Speed of sound [m/s]:", font=GUIStatics.STANDARD_FONT_SMALL) \
                .place(relx=widgets_x_start + 0.025, rely=0.33)
            entry_material_c_value = tk.StringVar()
            entry_material_c_value.set('0')
            entry_material_c_value_field = tk.Entry(window_bcs, textvariable=entry_material_c_value,
                                                    font=GUIStatics.STANDARD_FONT_SMALL, width=8)
            entry_material_c_value_field.place(relx=widgets_x_start + 0.025 + 0.5, rely=0.33)

            tk.Label(window_bcs, text="Density [kg/m³]:", font=GUIStatics.STANDARD_FONT_SMALL) \
                .place(relx=widgets_x_start + 0.025, rely=0.38)
            entry_material_rho_value = tk.StringVar()
            entry_material_rho_value.set('0')
            entry_material_rho_value_field = tk.Entry(window_bcs, textvariable=entry_material_rho_value,
                                                      font=GUIStatics.STANDARD_FONT_SMALL, width=8)
            entry_material_rho_value_field.place(relx=widgets_x_start + 0.025 + 0.5, rely=0.38)
            pos_y_set_button = 0.38

        entry_materials_values_button = tk.Button(window_bcs, text="SET VALUE", command=set_region_values,
                                                 width=12, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALL)
        entry_materials_values_button.place(relx=widgets_x_start + 0.025, rely=pos_y_set_button + 0.075)
        entry_materials_values_button.config(state='disabled')

        def accept_regions():
            """
            Button action for setting region parameters (Materials)
            :return:
            """

            self.init_information_text_field()
            self.text_information_str += '\n\nRegion Parameters:\n'
            for region_nbr in self.region_parameters.keys():
                region_k = self.region_parameters[region_nbr]['material']['k']
                region_c = self.region_parameters[region_nbr]['material']['c']
                region_rho = self.region_parameters[region_nbr]['material']['rho']
                if self.equation == 'HE':
                    self.text_information_str += f"R-{region_nbr}: k={region_k}"
                elif self.equation == 'HH':
                    self.text_information_str += f"R-{region_nbr}: c={region_c}, rho={region_rho}; | "

            GUIStatics.update_text_field(self.text_information, self.text_information_str)
            window_bcs.destroy()  # closes top window

        button_accept = tk.Button(window_bcs, text="ACCEPT REGIONs", command=accept_regions,
                                  width=14, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_MID_BOLD)
        button_accept.place(relx=widgets_x_start + 0.05, rely=0.895)

    def window_assign_boundary_conditions(self):
        """
        Opens top window to assign boundary conditions
        """

        def set_boundary_value():
            """
            Button action to set boundary values and type
            :return:
            """
            boundary_nbr = dropdown_boundary_select_var.get().split('B-')[-1]
            boundary_type = dropdown_boundary_type_var.get()
            if boundary_type == 'None' or boundary_nbr == 'None':
                return None
            try:
                value = float(entry_boundary_value.get())
                value_B = None
                if boundary_type == 'Robin':
                    value_B = float(entry_boundary_value_B.get())
            except ValueError:
                value = 0.0
            self.boundary_parameters[boundary_nbr]['bc']['type'] = boundary_type
            if boundary_type == 'Robin':
                self.boundary_parameters[boundary_nbr]['bc']['value'] = [value, value_B]
            else:
                self.boundary_parameters[boundary_nbr]['bc']['value'] = value

        def set_node_value():
            """
            Button action to set value for boundary condition for nodes (eg acoustic source values)
            :return:
            """
            node_number = dropdown_node_select_var.get().split('N-')[-1]
            try:
                value = entry_node_value.get()
            except ValueError:
                value = 0.0
            self.node_parameters[node_number]['bc']['value'] = value

        def trace_boundary(*args):
            """
            tracer function for highlighting boundarys in set boundary window
            :param args:
            :return:
            """

            last_highlight_element = self.canvas.find_withtag('highlight_element')
            if last_highlight_element:
                self.canvas.delete(last_highlight_element)
            boundary_nbr = dropdown_boundary_select_var.get().split('B-')[-1]
            button_boundary_value_set.config(state='normal')
            value_set = self.boundary_parameters[boundary_nbr]['bc']['value']
            type_set = self.boundary_parameters[boundary_nbr]['bc']['type']

            if type_set in ['Neumann', 'Dirichlet']:
                entry_boundary_value.set(str(value_set))
                entry_boundary_value_B.set('None')
            elif type_set == 'Robin':
                entry_boundary_value.set(str(value_set[0]))
                entry_boundary_value_B.set(str(value_set[1]))
            if type_set:
                dropdown_boundary_type_var.set(type_set)
            else:
                entry_boundary_value.set('None')
                entry_boundary_value_B.set('None')
            nodes = self.boundary_parameters[boundary_nbr]['coordinates']
            self.highlight_element = self.canvas.create_line(GUIStatics.transform_node_to_canvas(nodes[0]),
                                                             GUIStatics.transform_node_to_canvas(nodes[1]),
                                                             width=6, fill=GUIStatics.CANVAS_HIGHLIGHT_ELEMENT,
                                                             dash=(1, 1), tags='highlight_element')

        def trace_boundary_type(*args):
            """
            Traces boundary type selected and changes field states for values and labels accordingly
            :param args:
            :return:
            """
            boundary_type_selected = dropdown_boundary_type_var.get()
            equation_selected = self.equation
            if equation_selected == 'HE':
                if boundary_type_selected == 'Dirichlet':
                    entry_label_a.config(text='Temp T:')
                    entry_label_b.config(text='NONE')
                    entry_label_a_note.config(text='[K]')
                    entry_label_b_note.config(text='[-]')
                    entry_boundary_value_field.config(state='normal')
                    entry_boundary_value_B_field.config(state='disabled')
                elif boundary_type_selected == 'Neumann':
                    entry_label_a.config(text='Flux q:')
                    entry_label_b.config(text='NONE')
                    entry_label_a_note.config(text='[W/m²]')
                    entry_label_b_note.config(text='[-]')
                    entry_boundary_value_field.config(state='normal')
                    entry_boundary_value_B_field.config(state='disabled')
                elif boundary_type_selected == 'Robin':
                    entry_label_a.config(text='Fluid Temp T:')
                    entry_label_b.config(text='Heat TC h:')
                    entry_label_a_note.config(text='[K]')
                    entry_label_b_note.config(text='[W/(m²K)]')
                    entry_boundary_value_field.config(state='normal')
                    entry_boundary_value_B_field.config(state='normal')

            elif equation_selected == 'HH':
                if boundary_type_selected == 'Dirichlet':
                    entry_label_a.config(text='Pressure P:')
                    entry_label_b.config(text='NONE')
                    entry_label_a_note.config(text='[Pa]')
                    entry_label_b_note.config(text='[-]')
                    entry_boundary_value_field.config(state='normal')
                    entry_boundary_value_B_field.config(state='disabled')
                elif boundary_type_selected == 'Neumann':
                    entry_label_a.config(text='Impedance Z:')
                    entry_label_b.config(text='NONE')
                    entry_label_a_note.config(text='[Pa s/m]')
                    entry_label_b_note.config(text='[-]')
                    entry_boundary_value_field.config(state='normal')
                    entry_boundary_value_B_field.config(state='disabled')
                elif boundary_type_selected == 'Robin':
                    entry_label_a.config(text='NONE')
                    entry_label_b.config(text='NONE')
                    entry_label_a_note.config(text='[-]')
                    entry_label_b_note.config(text='[-]')
                    entry_boundary_value_field.config(state='disabled')
                    entry_boundary_value_B_field.config(state='disabled')

        def trace_node(*args):
            """
            tracer function for highlighting nodes in set boundary window
            :param args:
            :return:
            """
            last_highlight_element = self.canvas.find_withtag('highlight_element')
            if last_highlight_element:
                self.canvas.delete(last_highlight_element)
            node_number = dropdown_node_select_var.get().split('N-')[-1]
            node = self.node_parameters[node_number]['coordinates']
            node = GUIStatics.transform_node_to_canvas(node)
            self.highlight_element = self.canvas.create_oval(node[0] - 10, node[1] - 10, node[0] + 10, node[1] + 10,
                                                             width=3, outline=GUIStatics.CANVAS_HIGHLIGHT_ELEMENT,
                                                             dash=(2, 1), fill='', tags='highlight_element')

        equation_set = self.equation

        window_bcs = tk.Toplevel(self)
        window_bcs.title('ASSIGN SYSTEM PARAMETERS')
        window_bcs.geometry(f"{350}x{500}")
        window_bcs.resizable(False, False)
        self.set_icon(window_bcs)

        widgets_x_start = 0.01
        GUIStatics.create_divider(window_bcs, widgets_x_start, 0.05, 335)
        tk.Label(window_bcs, text="Boundary Conditions", font=GUIStatics.STANDARD_FONT_MID_BOLD) \
            .place(relx=widgets_x_start, rely=0.075)
        tk.Label(window_bcs, text=f"{'Select Boundary' + 15 * ' ' + 'Select Boundary Type'}",
                 font=GUIStatics.STANDARD_FONT_MID) \
            .place(relx=widgets_x_start + 0.025, rely=0.125)

        boundaries = [f"B-{nbr}" for nbr in self.boundary_parameters.keys()]
        dropdown_boundary_select_var = tk.StringVar()
        dropdown_boundary_select_var.set('None')
        dropdown_boundary_select = tk.OptionMenu(window_bcs, dropdown_boundary_select_var, *boundaries)
        dropdown_boundary_select.config(font=GUIStatics.STANDARD_FONT_SMALL, width=8, height=1)
        dropdown_boundary_select.place(relx=widgets_x_start + 0.025, rely=0.18)
        dropdown_boundary_select_var.trace('w', trace_boundary)

        boundary_types = ['Dirichlet', 'Neumann', 'Robin']
        dropdown_boundary_type_var = tk.StringVar()
        dropdown_boundary_type_var.set(boundary_types[0])
        dropdown_boundary_type = tk.OptionMenu(window_bcs, dropdown_boundary_type_var, *boundary_types)
        dropdown_boundary_type.config(font=GUIStatics.STANDARD_FONT_SMALL, width=8, height=1)
        dropdown_boundary_type.place(relx=widgets_x_start + 0.48, rely=0.18)
        dropdown_boundary_type_var.trace('w', trace_boundary_type)
        tooltip_text_dropdown_boundary_type = 'None'
        if self.equation == 'HE':
            tooltip_text_dropdown_boundary_type = (f" Dirichlet: Constant Temperature \n"
                                                   f" Neumann: Heat Flux              \n"
                                                   f" Robin: Convective Heat Flux     ")
        elif self.equation == 'HH':
            tooltip_text_dropdown_boundary_type = (f" Dirichlet: Constant Pressure          \n"
                                                   f" Neumann: Impedance Boundary Condition \n"
                                                   f" Robin: Not implemented                ")
        Tooltip(dropdown_boundary_type, tooltip_text_dropdown_boundary_type)

        init_value_A = 'None'
        entry_label_a_note_text = 'None'
        if self.equation == 'HE':
            init_value_A = 'Temp T:'
            entry_label_a_note_text = '[K]'
        elif self.equation == 'HH':
            init_value_A = 'Pressure P:'
            entry_label_a_note_text = '[Pa]'

        tooltip_text_field_A = 'Enter Value - Placeholder...'
        entry_label_a = tk.Label(window_bcs, text=init_value_A, font=GUIStatics.STANDARD_FONT_SMALL)
        entry_label_a.place(relx=widgets_x_start + 0.025, rely=0.27)
        entry_label_a_note = tk.Label(window_bcs, text=entry_label_a_note_text,
                                      font=GUIStatics.STANDARD_FONT_SMALLER)
        entry_label_a_note.place(relx=widgets_x_start + 0.455, rely=0.27)
        entry_boundary_value = tk.StringVar()
        entry_boundary_value.set('None')
        entry_boundary_value_field = tk.Entry(window_bcs, textvariable=entry_boundary_value,
                                              font=GUIStatics.STANDARD_FONT_SMALL, width=8)
        entry_boundary_value_field.place(relx=widgets_x_start + 0.025 + 0.25, rely=0.27)


        entry_label_b = tk.Label(window_bcs, text="NONE", font=GUIStatics.STANDARD_FONT_SMALL)
        entry_label_b.place(relx=widgets_x_start + 0.025, rely=0.33)
        entry_label_b_note = tk.Label(window_bcs, text="[-]", font=GUIStatics.STANDARD_FONT_SMALLER)
        entry_label_b_note.place(relx=widgets_x_start + 0.455, rely=0.33)
        entry_boundary_value_B = tk.StringVar()
        entry_boundary_value_B.set('None')
        entry_boundary_value_B_field = tk.Entry(window_bcs, textvariable=entry_boundary_value_B,
                                                font=GUIStatics.STANDARD_FONT_SMALL, width=8, state='disabled')
        entry_boundary_value_B_field.place(relx=widgets_x_start + 0.025 + 0.25, rely=0.33)

        button_boundary_value_set = tk.Button(window_bcs, text="SET VALUE", command=set_boundary_value,
                                              width=12, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALL)
        button_boundary_value_set.place(relx=widgets_x_start + 0.6, rely=0.29)
        button_boundary_value_set.config(state='disabled')

        if equation_set == 'HH':
            GUIStatics.create_divider(window_bcs, widgets_x_start, 0.42, 335)
            tk.Label(window_bcs, text="Point Sources", font=GUIStatics.STANDARD_FONT_MID_BOLD) \
                .place(relx=widgets_x_start, rely=0.44)
            tk.Label(window_bcs, text=f"{'Select Node'}",
                     font=GUIStatics.STANDARD_FONT_MID) \
                .place(relx=widgets_x_start + 0.025, rely=0.49)

            points = [f"N-{nbr}" for nbr in self.nodes.keys()]
            dropdown_node_select_var = tk.StringVar()
            dropdown_node_select_var.set('None')
            dropdown_node_select = tk.OptionMenu(window_bcs, dropdown_node_select_var, *points)
            dropdown_node_select.config(font=GUIStatics.STANDARD_FONT_SMALL, width=8, height=1)
            dropdown_node_select.place(relx=widgets_x_start + 0.025, rely=0.545)
            dropdown_node_select_var.trace('w', trace_node)

            tk.Label(window_bcs, text="Sound Source:", font=GUIStatics.STANDARD_FONT_SMALL) \
                .place(relx=widgets_x_start + 0.025, rely=0.635)
            tk.Label(window_bcs, text="[W/m]", font=GUIStatics.STANDARD_FONT_SMALLER).place(relx=widgets_x_start + 0.455, rely=0.635)
            entry_node_value = tk.StringVar()
            entry_node_value.set('None')
            entry_node_value_field = tk.Entry(window_bcs, textvariable=entry_node_value,
                                              font=GUIStatics.STANDARD_FONT_SMALL, width=8)
            entry_node_value_field.place(relx=widgets_x_start + 0.025 + 0.25, rely=0.635)
            entry_node_value_set = tk.Button(window_bcs, text="SET VALUE", command=set_node_value,
                                             width=12, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALL)
            entry_node_value_set.place(relx=widgets_x_start + 0.6, rely=0.63)

        def accept_bcs():
            """
            Button action to set boundary conditions
            :return:
            """
            last_highlight_element = self.canvas.find_withtag('highlight_element')
            if last_highlight_element:
                self.canvas.delete(last_highlight_element)

            self.init_information_text_field()
            self.text_information_str += '\n\nBoundary Conditions:\n'
            for boundary_nbr in self.boundary_parameters.keys():
                boundary_value = self.boundary_parameters[boundary_nbr]['bc']['value']
                boundary_type = self.boundary_parameters[boundary_nbr]['bc']['type']
                boundary_type_dict = {'Dirichlet': 'DC', 'Neumann': 'NM', 'Robin': 'RB'}
                if boundary_type:
                    self.text_information_str += f"B-{boundary_nbr}: {boundary_value},{boundary_type_dict[boundary_type]}; | "

            for node_nbr in self.node_parameters.keys():
                node_value = self.node_parameters[node_nbr]['bc']['value']
                node_type = self.node_parameters[node_nbr]['bc']['type']

                if node_value:
                    self.text_information_str += f"N-{node_nbr}: {node_value}; | "

            GUIStatics.update_text_field(self.text_information, self.text_information_str)
            window_bcs.destroy()  # closes top window

        button_accept = tk.Button(window_bcs, text="ACCEPT BCs", command=accept_bcs,
                                  width=12, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_MID_BOLD)
        button_accept.place(relx=widgets_x_start + 0.05, rely=0.895)

    def create_BC_params(self):
        """
        reformats the geometry for boundary and material parameters assignment via class CreateBCParams
        Only for Development, otherwise done in receive_geometry()
        :return:
        """
        if self.geometry_input:
            create_params = CreateBCParams(self.geometry_input)
            regions, boundaries, nodes = create_params.main()

    def define_geometry(self):
        """
        callback method, Executed when button "DEFINE GEOMETRY" pressed, creates callback for Class Geometry
        :return:
        """

        self.animation = False
        all_canvas_elements = self.canvas.find_all()
        for elem in all_canvas_elements:
            self.canvas.delete(elem)
        GUIStatics.add_canvas_border(self.canvas)
        self.canvas.create_text(GUIStatics.CANVAS_SIZE_X / 2, GUIStatics.CANVAS_SIZE_Y / 2,
                                text='CREATE GEOMETRY', fill='Gray', font=("Helvetica", 16))
        return_geometry = Geometry(self.receive_geometry, self.geometry_input)

    def receive_geometry(self, geometry):
        """
        callback method, Gets geometry input from class Geometry
        :param geometry:
        :return:
        """

        self.geometry_input = geometry
        geometry_input_str = str(geometry)
        # self.text_label.config(text=geometry_input_str, font=("Helvetica", 6))  # for testing

        format_for_params = CreateBCParams(self.geometry_input)
        self.regions, self.boundaries, self.nodes = format_for_params.main()
        self.init_parameters()
        self.button_show_geom.config(state='normal')

    def init_parameters(self):
        """
        Initializes parameters after geometry was defined
        :return:
        """
        self.draw_geometry_from_definebcs()

        # enable disabled buttons for bcs, materials, calc parametsr
        self.button_define_bcs.config(state="normal")
        self.button_define_materials.config(state="normal")
        self.button_define_calc_params.config(state="normal")

        # update information field
        self.init_information_text_field()
        GUIStatics.update_text_field(self.text_information, self.text_information_str)

        # initializes boundary parameters, materials and calculation
        region_parameters = dict()
        boundary_parameters = dict()
        node_parameters = dict()
        calculation_parameters = dict()
        for region_nbr, values in self.regions.items():
            coordinates = values['coordinates']
            area_neg_pos = values['area_neg_pos']
            region_parameters[region_nbr] = {'coordinates' : coordinates,
                                             'area_neg_pos': area_neg_pos,
                                             'material'    : {'k': 1.0, 'c': 340, 'rho': 1.21}}
        for boundary_nbr, nodes in self.boundaries.items():
            coordinates = [nodes[0], nodes[1]]
            boundary_parameters[boundary_nbr] = {'coordinates': coordinates, 'bc': {'type': None, 'value': None}}
        for node_nbr, node in self.nodes.items():
            coordinates = node
            node_parameters[node_nbr] = {'coordinates': coordinates, 'bc': {'type': None, 'value': None}}
        try:
            calculation_parameters = {'mesh_density': None, 'freq': None, 'equation': 'HE',
                                      'units'       : self.geometry_input['units']}
        except TypeError:
            calculation_parameters = {'mesh_density': None, 'freq': None, 'equation': 'HE',
                                      'units'       : 'm'}
        self.region_parameters = region_parameters
        self.boundary_parameters = boundary_parameters
        self.node_parameters = node_parameters
        self.calculation_parameters = calculation_parameters

    def init_information_text_field(self):
        """
        Initializes the information text field with the geometry provided
        :return:
        """
        text_regions = [
                f"{region_nbr}: {values['coordinates']}, ({'+' if values['area_neg_pos'] == 'Positive' else '-'})\n"
                for region_nbr, values in self.regions.items()]
        text_boundaries = [f"{bound_nbr}: {values} | " for bound_nbr, values in self.boundaries.items()]
        text_nodes = [f"{node_nbr}: {values} | " for node_nbr, values in self.nodes.items()]
        self.text_information_str = f"Regions:\n" + ''.join(text_regions) \
                                    + '\nBoundaries:\n' + ''.join(text_boundaries) \
                                    + '\n\nNodes:\n' + ''.join(text_nodes)

    def draw_geometry_from_definebcs(self):
        """
        draws the formated geometry (boundaries, vertices, regions from class  CreateBCParams
        :return:
        """

        all_canvas_elements = self.canvas.find_all()
        for elem in all_canvas_elements:
            self.canvas.delete(elem)
        GUIStatics.add_canvas_static_elements(self.canvas)

        # draw legend and stats
        nbr_of_nodes = len(self.nodes.keys())
        nbr_of_boundaries = len(self.boundaries.keys())
        nbr_of_regions = len(self.regions.keys())
        stat_text = f"Regions -R-    : {nbr_of_regions}\n" \
                    f"Boundaries -B- : {nbr_of_boundaries}\n" \
                    f"Nodes -N-      : {nbr_of_nodes}"
        self.canvas.create_text(80, 30, text=stat_text, fill='#21090B',
                                font=('Courier New', 8))

        # draw regions two times so negative areas are above positives
        color_code_plus = '#B88585'
        color_code_minus = '#8AC1C6'
        for region_nbr, params in self.regions.items():
            nodes = params['coordinates']
            area_neg_pos = params['area_neg_pos']
            if area_neg_pos == 'Negative':
                continue
            color_code = color_code_plus if area_neg_pos == 'Positive' else color_code_minus
            nodes = [GUIStatics.transform_node_to_canvas(node) for node in nodes]
            self.canvas.create_polygon(nodes, fill=color_code, outline='', width=2)
        for region_nbr, params in self.regions.items():
            nodes = params['coordinates']
            area_neg_pos = params['area_neg_pos']
            if area_neg_pos == 'Positive':
                continue
            color_code = color_code_plus if area_neg_pos == 'Positive' else color_code_minus
            nodes = [GUIStatics.transform_node_to_canvas(node) for node in nodes]
            self.canvas.create_polygon(nodes, fill=color_code, outline='', width=2)

        # text for regions
        for region_nbr, params in self.regions.items():
            nodes = params['coordinates']
            nodes = [GUIStatics.transform_node_to_canvas(node) for node in nodes]
            center_x, center_y = GUIStatics.get_polygon_center(nodes)
            area_neg_pos = params['area_neg_pos']
            text = f'R:{region_nbr}({"+" if area_neg_pos == "Positive" else "-"})'
            self.canvas.create_text(center_x, center_y, text=text, fill='white', font=GUIStatics.STANDARD_FONT_SMALLER)

        # draw boundaries
        for boundary_nbr, nodes in self.boundaries.items():
            nodes = [GUIStatics.transform_node_to_canvas(node) for node in nodes]
            sector_start_node = nodes[0]
            sector_end_node = nodes[1]
            center_x, center_y = GUIStatics.get_polygon_center(nodes)
            text = f'B:{boundary_nbr}'
            self.canvas.create_line(sector_start_node, sector_end_node, fill='#2F1417', width=2, dash=(1, 1),
                                    arrow='both', arrowshape=(8, 10, 3))
            self.canvas.create_text(center_x, center_y, text=text, fill='#420382', font=GUIStatics.STANDARD_FONT_SMALL)

        # draw points
        for node_nbr, node in self.nodes.items():
            node = GUIStatics.transform_node_to_canvas(node)
            text = f'N:{node_nbr}'
            self.canvas.create_oval(node[0] - 4, node[1] - 4, node[0] + 4, node[1] + 4, fill='#5F0F0F',
                                    outline='#1F1F1F', width=2, dash=(1, 1))
            self.canvas.create_text(node[0] - 10, node[1] - 10, text=text, fill='#14380A',
                                    font=GUIStatics.STANDARD_FONT_SMALL)

    def draw_mesh_from_mesh_output(self):
        """
        Called when Button for show mesh pressed
        Draws mesh in canvas
        :return:
        """
        all_canvas_elements = self.canvas.find_all()
        for elem in all_canvas_elements:
            self.canvas.delete(elem)
        GUIStatics.add_canvas_static_elements(self.canvas)

        # draw regions two times so negative areas are above positives
        color_code_plus = '#B8A8A8'
        color_code_minus = '#A8B3B8'
        color_code_outline_plus = '#261D1D'
        color_code_outline_minus = '#272634'
        for region_nbr, params in self.regions.items():
            nodes = params['coordinates']
            area_neg_pos = params['area_neg_pos']
            if area_neg_pos == 'Negative':
                continue
            color_code = color_code_plus if area_neg_pos == 'Positive' else color_code_minus
            nodes = [GUIStatics.transform_node_to_canvas(node) for node in nodes]
            self.canvas.create_polygon(nodes, fill=color_code, outline=color_code_outline_plus, width=2)
        for region_nbr, params in self.regions.items():
            nodes = params['coordinates']
            area_neg_pos = params['area_neg_pos']
            if area_neg_pos == 'Positive':
                continue
            color_code = color_code_plus if area_neg_pos == 'Positive' else color_code_minus
            nodes = [GUIStatics.transform_node_to_canvas(node) for node in nodes]
            self.canvas.create_polygon(nodes, fill=color_code, outline=color_code_outline_minus, width=2)

        # draw nodes
        if len(self.nodes_mesh_gen) < 1000:
            for node in self.nodes_mesh_gen:
                node_transformed = GUIStatics.transform_node_to_canvas(node)
                nx, ny = node_transformed[0], node_transformed[1]
                self.canvas.create_oval(nx - 2, ny - 2, nx + 2, ny + 2, fill="gray")

        # draw elements
        for triangle in self.triangulation:
            p0 = int(triangle[0])
            p1 = int(triangle[1])
            p2 = int(triangle[2])

            n0 = GUIStatics.transform_node_to_canvas(self.nodes_mesh_gen[p0])
            n1 = GUIStatics.transform_node_to_canvas(self.nodes_mesh_gen[p1])
            n2 = GUIStatics.transform_node_to_canvas(self.nodes_mesh_gen[p2])
            self.canvas.create_line(n0, n1, fill="#380303")
            self.canvas.create_line(n1, n2, fill="#380303")
            self.canvas.create_line(n2, n0, fill="#380303")

        # draw legend and stats
        stat_text = f"Nodes    : {len(self.nodes_mesh_gen)}\n" \
                    f"Elements : {len(self.triangulation)}\n"
        self.canvas.create_text(80, 30, text=stat_text, fill='#21090B',
                                font=('Courier New', 8))

    def debug(self):
        """
        for debugging
        :return:
        """

        write_output = (f"self.region_parameters = {self.region_parameters}\n"
                        f"self.boundary_parameters = {self.boundary_parameters}\n"
                        f"self.node_parameters = {self.node_parameters}\n"
                        f"self.calculation_parameters = {self.calculation_parameters}\n"
                        f"self.nodes_mesh_gen = np.array({list(self.nodes_mesh_gen) if self.nodes_mesh_gen is not None else 'None'})\n"
                        f"self.single_nodes_dict = {self.single_nodes_dict}\n"
                        f"self.boundary_nodes_dict = {self.boundary_nodes_dict}\n"
                        f"self.triangulation = np.array({list(self.triangulation) if self.triangulation is not None else 'None'})\n"
                        f"self.triangulation_region_dict = {self.triangulation_region_dict}\n")
        write_output = write_output.replace('array', 'np.array')
        write_output = write_output.replace('np.np.', 'np.')
        with open('output.txt', 'w') as f:
            f.write(write_output)


if __name__ == '__main__':
    gui = GUI()
    gui.mainloop()