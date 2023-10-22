import tkinter as tk
import math
from typing import Callable, Any
from tkinter import filedialog
import json
from guistatics import GUIStatics
from definebcs import CreateBCParams
from geometry import Geometry
import random

#################################################
# Other
AUTHOR = 'Itsame Mario'
VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 0


#################################################


# todo add window with small description for each module


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
        self.equation = 'HH'  # HE for heat equation, HH for hemlholtz equation
        self.region_parameters = None  # saves materials, area_neg_pos, nodes, number for regions
        self.boundary_parameters = None  # saves dirichlet/neumann/robin values and setting, nodes, number for boundaries
        self.node_parameters = None  # saves node number, coords, neumann value for nodes
        self.calculation_parameters = None  # save calculation parameters, mesh density etc
        # some output for user
        self.text_information_str = ''
        # for development
        self.regions = {'0': {'coordinates': [(-4.0, -3.0), (1.0, -2.5), (2.5, 1.0), (-2.5, 1.0), (-4.2, -1.5)],
                              'area_neg_pos': 'Positive'},
                        '1': {'coordinates': [(2.5, 1.0), (0.0, 3.0), (-2.5, 1.0)], 'area_neg_pos': 'Positive'},
                        '2': {'coordinates': [(-1.0, 0.0), (0.0, 0.0), (0.0, 0.75), (-1.0, 0.5)],
                              'area_neg_pos': 'Negative'}}
        self.boundaries = {'0': ((-4.0, -3.0), (1.0, -2.5)), '1': ((1.0, -2.5), (2.5, 1.0)),
                           '2': ((2.5, 1.0), (-2.5, 1.0)), '3': ((-2.5, 1.0), (-4.2, -1.5)),
                           '4': ((-4.2, -1.5), (-4.0, -3.0)), '5': ((2.5, 1.0), (0.0, 3.0)),
                           '6': ((0.0, 3.0), (-2.5, 1.0)), '7': ((-1.0, 0.0), (0.0, 0.0)),
                           '8': ((0.0, 0.0), (0.0, 0.75)), '9': ((0.0, 0.75), (-1.0, 0.5)),
                           '10': ((-1.0, 0.5), (-1.0, 0.0))}
        self.nodes = {'0': (-3.0, -2.0), '1': (0.0, 1.5), '2': (1.0, -1.0), '3': (-4.0, -3.0), '4': (1.0, -2.5),
                      '5': (2.5, 1.0), '6': (-2.5, 1.0), '7': (-4.2, -1.5), '8': (0.0, 3.0), '9': (-1.0, 0.0),
                      '10': (0.0, 0.0), '11': (0.0, 0.75), '12': (-1.0, 0.5)}

        super().__init__()
        # Start Main Window
        self.main_window()

    def main_window(self):
        """
        Defines Main Window
        :return:
        """

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
        self.animation = True

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

        width = GUIStatics.CANVAS_SIZE_X
        height = GUIStatics.CANVAS_SIZE_Y
        self.canvas = tk.Canvas(self, width=GUIStatics.CANVAS_SIZE_X, height=GUIStatics.CANVAS_SIZE_Y,
                                bg=GUIStatics.CANVAS_BG)
        self.canvas.place(relx=canvas_x + 0.0075, rely=canvas_y)
        GUIStatics.add_canvas_border(self.canvas)
        # GUIStatics.add_canvas_static_elements(self.canvas)
        rect = self.canvas.create_rectangle(10, 10, 50, 50, fill="", outline="gray")
        animate()

        ##################################################

        ##################################################
        # Buttons
        def assign_BCs():
            self.window_assign_boundary_conditions()

        def assign_materials():
            ...

        def assign_calc_params():
            ...

        def create_mesh():
            ...

        def solve_system():
            ...

        # Button define Geometry
        tk.Frame(self, height=2, width=230, bg=GUIStatics.CANVAS_BORDER_COLOR) \
            .place(relx=widgets_x_start, rely=0.08)
        button_define_geometry = tk.Button(self, text="GEOMETRY", command=self.define_geometry, width=12,
                                           font=GUIStatics.STANDARD_FONT_BUTTON_BIG_BOLD, height=1)
        button_define_geometry.place(relx=widgets_x_start, rely=0.1)

        # FEM Parameters
        GUIStatics.create_divider(self, widgets_x_start, 0.17, 230)
        tk.Label(self, text="FEM PARAMETERS", font=GUIStatics.STANDARD_FONT_MID_BOLD) \
            .place(relx=widgets_x_start, rely=0.175)

        # Dropdown select equation
        tk.Label(self, text="Equation: ", font=GUIStatics.STANDARD_FONT_MID) \
            .place(relx=widgets_x_start, rely=0.22)
        equations = ['Heat Equation', 'Helmholtz Equation']
        var_equations = tk.StringVar()
        var_equations.set(equations[0])  # default value m
        dropdown_equation_select = tk.OptionMenu(self, var_equations, *equations)
        dropdown_equation_select.config(font=GUIStatics.STANDARD_FONT_SMALL, width=15, height=1)
        dropdown_equation_select.place(relx=widgets_x_start + 0.065, rely=0.215)

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
        self.text_information_str = 'None'
        GUIStatics.create_divider(self, widgets_x_start, 0.5, 230)
        tk.Label(self, text="Information: ", font=GUIStatics.STANDARD_FONT_MID_BOLD) \
            .place(relx=widgets_x_start, rely=0.505)
        self.text_information = tk.Text(self, height=28, width=44, wrap=tk.WORD,
                                        font=GUIStatics.STANDARD_FONT_SMALLEST, bg='light gray', fg='black')
        self.text_information.place(relx=widgets_x_start + 0.005, rely=0.54)
        self.text_information.insert(tk.END, self.text_information_str)
        self.text_information.config(state='disabled')

        # Debug
        # Reformat Boundaryconditions via CreateBCParams todo: THIS IS ONLY NEEDED FOR DEVELOPMENT
        button_create_bc = tk.Button(self, text="FORM BCS", command=self.create_BC_params, width=10,
                                           height=1, font=('Arial', 6))
        button_create_bc.place(relx=0.01, rely=0.01)
        button_debug = tk.Button(self, text="DEBUG", command=self.debug, width=10,
                                           height=1, font=('Arial', 6))
        button_debug.place(relx=0.07, rely=0.01)

        # placeholder for text FOR DEVELOPING
        #self.text_label = tk.Label(self, text="Init")
        #self.text_label.place(relx=0.02, rely=0.965)

        # Developing
        self.animation = False  # todo delete this
        self.init_parameters()  # todo delete this
        self.draw_geometry_from_definebcs()  # todo delete this
        ##################################################

    def window_assign_boundary_conditions(self):

        def set_boundary_value():
            boundary_nbr = dropdown_boundary_select_var.get().split('B-')[-1]
            boundary_type = dropdown_boundary_type_var.get()
            if boundary_type == 'None' or boundary_nbr == 'None':
                return None
            try:
                value = float(entry_boundary_value.get())
            except ValueError:
                value = 0.0
            self.boundary_parameters[boundary_nbr]['bc']['type'] = boundary_type
            self.boundary_parameters[boundary_nbr]['bc']['value'] = value

        def set_node_value():
            node_number = dropdown_node_select_var.get().split('N-')[-1]
            try:
                value = entry_node_value.get()
            except ValueError:
                value = 0.0
            self.node_parameters[node_number]['bc']['value'] = value

        def trace_boundary(*args):

            last_highlight_element = self.canvas.find_withtag('highlight_element')
            if last_highlight_element:
                self.canvas.delete(last_highlight_element)
            boundary_nbr = dropdown_boundary_select_var.get().split('B-')[-1]
            value_set = self.boundary_parameters[boundary_nbr]['bc']['value']
            type_set = self.boundary_parameters[boundary_nbr]['bc']['type']

            entry_boundary_value.set(str(value_set))
            if type_set:
                dropdown_boundary_type_var.set(type_set)
            nodes = self.boundary_parameters[boundary_nbr]['coordinates']
            self.highlight_element = self.canvas.create_line(GUIStatics.transform_node_to_canvas(nodes[0]),
                                                     GUIStatics.transform_node_to_canvas(nodes[1]),
                                                     width=6, fill=GUIStatics.CANVAS_HIGHLIGHT_ELEMENT, dash=(1, 1), tags='highlight_element')

        def trace_node(*args):
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

        widgets_x_start = 0.01
        GUIStatics.create_divider(window_bcs, widgets_x_start, 0.05, 335)
        tk.Label(window_bcs, text="Boundary Conditions", font=GUIStatics.STANDARD_FONT_MID_BOLD) \
            .place(relx=widgets_x_start, rely=0.075)
        tk.Label(window_bcs, text=f"{'Select Boundary' + 15 * ' ' + 'Select Boundary Type'}", font=GUIStatics.STANDARD_FONT_MID) \
            .place(relx=widgets_x_start + 0.025, rely=0.125)

        boundaries = [f"B-{nbr}" for nbr in self.boundary_parameters.keys()]
        dropdown_boundary_select_var = tk.StringVar()
        dropdown_boundary_select_var.set('None')
        dropdown_boundary_select = tk.OptionMenu(window_bcs, dropdown_boundary_select_var, *boundaries)
        dropdown_boundary_select.config(font=GUIStatics.STANDARD_FONT_SMALL, width=8, height=1)
        dropdown_boundary_select.place(relx=widgets_x_start + 0.025, rely=0.18)
        dropdown_boundary_select_var.trace('w', trace_boundary)

        boundary_types = ['Dirichlet', 'Neumann']
        dropdown_boundary_type_var = tk.StringVar()
        dropdown_boundary_type_var.set(boundary_types[0])
        dropdown_boundary_type = tk.OptionMenu(window_bcs, dropdown_boundary_type_var, *boundary_types)
        dropdown_boundary_type.config(font=GUIStatics.STANDARD_FONT_SMALL, width=8, height=1)
        dropdown_boundary_type.place(relx=widgets_x_start + 0.48, rely=0.18)

        tk.Label(window_bcs, text="Value:", font=GUIStatics.STANDARD_FONT_SMALL)\
            .place(relx=widgets_x_start + 0.025, rely=0.27)
        entry_boundary_value = tk.StringVar()
        entry_boundary_value.set('None')
        entry_boundary_value_field = tk.Entry(window_bcs, textvariable=entry_boundary_value,
                                              font=GUIStatics.STANDARD_FONT_SMALL, width=8)
        entry_boundary_value_field.place(relx=widgets_x_start + 0.025 + 0.15, rely=0.27)
        button_boundary_value_set = tk.Button(window_bcs, text="SET VALUE", command=set_boundary_value,
                                          width=12, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALL)
        button_boundary_value_set.place(relx=widgets_x_start + 0.38, rely=0.265)

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

            tk.Label(window_bcs, text="Value:", font=GUIStatics.STANDARD_FONT_SMALL) \
                .place(relx=widgets_x_start + 0.025, rely=0.635)
            entry_node_value = tk.StringVar()
            entry_node_value.set('None')
            entry_node_value_field = tk.Entry(window_bcs, textvariable=entry_node_value,
                                                  font=GUIStatics.STANDARD_FONT_SMALL, width=8)
            entry_node_value_field.place(relx=widgets_x_start + 0.025 + 0.15, rely=0.635)
            entry_node_value_set = tk.Button(window_bcs, text="SET VALUE", command=set_node_value,
                                                  width=12, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALL)
            entry_node_value_set.place(relx=widgets_x_start + 0.38, rely=0.63)

        def accept_bcs():
            """

            :return:
            """
            last_highlight_element = self.canvas.find_withtag('highlight_element')
            if last_highlight_element:
                self.canvas.delete(last_highlight_element)

            self.text_information_str += '\n\nBoundary Conditions:\n'
            for boundary_nbr in self.boundary_parameters.keys():
                boundary_value = self.boundary_parameters[boundary_nbr]['bc']['value']
                boundary_type = self.boundary_parameters[boundary_nbr]['bc']['type']
                boundary_type_dict = {'Dirichlet': 'DC', 'Neumann': 'NM'}
                if boundary_value:
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
        return_geometry = Geometry(self.receive_geometry)

    def receive_geometry(self, geometry):
        """
        callback method, Gets geometry input from class Geometry
        :param geometry:
        :return:
        """

        self.geometry_input = geometry

        geometry_input_str = str(geometry)  # todo, for testing
        #self.text_label.config(text=geometry_input_str, font=("Helvetica", 6))  # todo, for testing

        format_for_params = CreateBCParams(self.geometry_input)
        self.regions, self.boundaries, self.nodes = format_for_params.main()
        self.init_parameters()

    def init_parameters(self):
        self.draw_geometry_from_definebcs()

        # enable disabled buttons for bcs, materials, calc parametsr
        self.button_define_bcs.config(state="normal")
        self.button_define_materials.config(state="normal")
        self.button_define_calc_params.config(state="normal")

        # update information field
        text_regions = [
            f"{region_nbr}: {values['coordinates']}, ({'+' if values['area_neg_pos'] == 'Positive' else '-'})\n"
            for region_nbr, values in self.regions.items()]
        text_boundaries = [f"{bound_nbr}: {values} | " for bound_nbr, values in self.boundaries.items()]
        text_nodes = [f"{node_nbr}: {values} | " for node_nbr, values in self.nodes.items()]
        self.text_information_str = f"Regions:\n" + ''.join(text_regions) \
                                    + '\nBoundaries:\n' + ''.join(text_boundaries) \
                                    + '\n\nNodes:\n' + ''.join(text_nodes)
        GUIStatics.update_text_field(self.text_information, self.text_information_str)

        # initializes boundary parameters, materials and calculation
        region_parameters = dict()
        boundary_parameters = dict()
        node_parameters = dict()
        calculation_parameters = dict()
        for region_nbr, values in self.regions.items():
            coordinates = values['coordinates']
            area_neg_pos = values['area_neg_pos']
            region_parameters[region_nbr] = {'coordinates': coordinates,
                                             'area_neg_pos': area_neg_pos,
                                             'material': {'k': 0, 'c': 0, 'rho': 0}}
        for boundary_nbr, nodes in self.boundaries.items():
            coordinates = [nodes[0], nodes[1]]
            boundary_parameters[boundary_nbr] = {'coordinates': coordinates, 'bc': {'type': None, 'value': None}}
        for node_nbr, node in self.nodes.items():
            coordinates = node
            node_parameters[node_nbr] = {'coordinates': coordinates, 'bc': {'type': None, 'value': None}}
        calculation_parameters = {'mesh_density': None, 'freq': None}
        self.region_parameters = region_parameters
        self.boundary_parameters = boundary_parameters
        self.node_parameters = node_parameters
        self.calculation_parameters = calculation_parameters

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

    def debug(self):
        """
        for debugging
        :return:
        """
        print("\n\n\n------------------DEBUG--------------------")
        print(f"self.geometry_input: {self.geometry_input}")
        print(f"self.regions: {self.regions}")
        print(f"self.boundaries = {self.boundaries}")
        print(f"self.nodes = {self.nodes}")
        print(f"self.equation = {self.equation}")
        print(f"\nself.region_parameters = {self.region_parameters}")
        print(f"self.boundary_parameters = {self.boundary_parameters}")
        print(f"self.node_parameters = {self.node_parameters}")
        print(f"self.calculation_parameters = {self.calculation_parameters}")


if __name__ == '__main__':
    gui = GUI()  # Todo - Develop: For testing main gui
    # gui = Geometry(lambda x: x)  # Todo - Develop: For testing Geometry gui, argument simulates callback
    gui.mainloop()



# structure of boundary conditions variables
# self.region_parameters = {'0': {'coordinates': [(-4.0, -3.0), (1.0, -2.5), (2.5, 1.0), (-2.5, 1.0), (-4.2, -1.5)], 'area_neg_pos': 'Positive', 'material': {'k': 0, 'c': 0, 'rho': 0}}, '1': {'coordinates': [(2.5, 1.0), (0.0, 3.0), (-2.5, 1.0)], 'area_neg_pos': 'Positive', 'material': {'k': 0, 'c': 0, 'rho': 0}}, '2': {'coordinates': [(-1.0, 0.0), (0.0, 0.0), (0.0, 0.75), (-1.0, 0.5)], 'area_neg_pos': 'Negative', 'material': {'k': 0, 'c': 0, 'rho': 0}}}
# self.boundary_parameters = {'0': {'coordinates': [(-4.0, -3.0), (1.0, -2.5)], 'bc': {'type': None, 'value': None}}, '1': {'coordinates': [(1.0, -2.5), (2.5, 1.0)], 'bc': {'type': None, 'value': None}}, '2': {'coordinates': [(2.5, 1.0), (-2.5, 1.0)], 'bc': {'type': None, 'value': None}}, '3': {'coordinates': [(-2.5, 1.0), (-4.2, -1.5)], 'bc': {'type': None, 'value': None}}, '4': {'coordinates': [(-4.2, -1.5), (-4.0, -3.0)], 'bc': {'type': None, 'value': None}}, '5': {'coordinates': [(2.5, 1.0), (0.0, 3.0)], 'bc': {'type': None, 'value': None}}, '6': {'coordinates': [(0.0, 3.0), (-2.5, 1.0)], 'bc': {'type': None, 'value': None}}, '7': {'coordinates': [(-1.0, 0.0), (0.0, 0.0)], 'bc': {'type': None, 'value': None}}, '8': {'coordinates': [(0.0, 0.0), (0.0, 0.75)], 'bc': {'type': None, 'value': None}}, '9': {'coordinates': [(0.0, 0.75), (-1.0, 0.5)], 'bc': {'type': None, 'value': None}}, '10': {'coordinates': [(-1.0, 0.5), (-1.0, 0.0)], 'bc': {'type': None, 'value': None}}}
# self.node_parameters = {'0': {'coordinates': (-3.0, -2.0), 'bc': {'type': None, 'value': None}}, '1': {'coordinates': (0.0, 1.5), 'bc': {'type': None, 'value': None}}, '2': {'coordinates': (1.0, -1.0), 'bc': {'type': None, 'value': None}}, '3': {'coordinates': (-4.0, -3.0), 'bc': {'type': None, 'value': None}}, '4': {'coordinates': (1.0, -2.5), 'bc': {'type': None, 'value': None}}, '5': {'coordinates': (2.5, 1.0), 'bc': {'type': None, 'value': None}}, '6': {'coordinates': (-2.5, 1.0), 'bc': {'type': None, 'value': None}}, '7': {'coordinates': (-4.2, -1.5), 'bc': {'type': None, 'value': None}}, '8': {'coordinates': (0.0, 3.0), 'bc': {'type': None, 'value': None}}, '9': {'coordinates': (-1.0, 0.0), 'bc': {'type': None, 'value': None}}, '10': {'coordinates': (0.0, 0.0), 'bc': {'type': None, 'value': None}}, '11': {'coordinates': (0.0, 0.75), 'bc': {'type': None, 'value': None}}, '12': {'coordinates': (-1.0, 0.5), 'bc': {'type': None, 'value': None}}}
# self.calculation_parameters = {'mesh_density': None, 'freq': None}