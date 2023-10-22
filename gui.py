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
        # definitions for setting BCs, Mats etc.
        self.equation = 'HE'  # HE for heat equation, HH for hemlholtz equation
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
                color = random.choice(['#383334', '#584043', '#8D565B', '#D5B7BA', '#A14750', '#582026', '#402628', '#870C18'])
                self.canvas.create_rectangle(pos_x - size_x, pos_y - size_y, pos_x + size_x, pos_y + size_y,
                                             fill="", outline=color, width=width, dash=(6, 1), activefill=color)
                self.canvas.create_text(175, GUIStatics.CANVAS_SIZE_Y - 75, text='ENTER GEOMETRY\n     TO START... :)', fill='Gray', font=("Helvetica", 22))
                self.canvas.after(150, animate)
            else:
                return None

        width = GUIStatics.CANVAS_SIZE_X
        height = GUIStatics.CANVAS_SIZE_Y
        self.canvas = tk.Canvas(self, width=GUIStatics.CANVAS_SIZE_X, height=GUIStatics.CANVAS_SIZE_Y,
                                bg=GUIStatics.CANVAS_BG)
        self.canvas.place(relx=canvas_x + 0.0075, rely=canvas_y)
        GUIStatics.add_canvas_border(self.canvas)
        #GUIStatics.add_canvas_static_elements(self.canvas)
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
        tk.Frame(self, height=2, width=230, bg=GUIStatics.CANVAS_BORDER_COLOR)\
            .place(relx=widgets_x_start, rely=0.08)
        button_define_geometry = tk.Button(self, text="GEOMETRY", command=self.define_geometry, width=12,
                                           font=GUIStatics.STANDARD_FONT_BUTTON_BIG_BOLD, height=1)
        button_define_geometry.place(relx=widgets_x_start, rely=0.1)


        # FEM Parameters
        GUIStatics.create_divider(self, widgets_x_start, 0.17, 230)
        tk.Label(self, text="FEM PARAMETERS", font=GUIStatics.STANDARD_FONT_MID_BOLD)\
            .place(relx=widgets_x_start, rely=0.175)

        # Dropdown select equation
        tk.Label(self, text="Equation: ", font=GUIStatics.STANDARD_FONT_MID)\
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
        self.button_define_calc_params = tk.Button(self, text="CALCULATION PARAMETERS", command=assign_calc_params, width=25,
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
        tk.Label(self, text="Information: ", font=GUIStatics.STANDARD_FONT_MID_BOLD)\
            .place(relx=widgets_x_start, rely=0.505)
        self.text_information = tk.Text(self, height=28, width=44, wrap=tk.WORD,
                                     font=GUIStatics.STANDARD_FONT_SMALLEST, bg='light gray', fg='black')
        self.text_information.place(relx=widgets_x_start + 0.005, rely=0.54)
        self.text_information.insert(tk.END, self.text_information_str)
        self.text_information.config(state='disabled')

        # Debug
        # Reformat Boundaryconditions via CreateBCParams todo: THIS IS ONLY NEEDED FOR DEVELOPMENT
        button_define_geometry = tk.Button(self, text="FORM BCS", command=self.create_BC_params, width=10,
                                           height=1, font=('Arial', 6))
        button_define_geometry.place(relx=0.01, rely=0.01)
        button_define_geometry = tk.Button(self, text="DEBUG", command=self.debug, width=10,
                                           height=1, font=('Arial', 6))
        button_define_geometry.place(relx=0.07, rely=0.01)

        # placeholder for text FOR DEVELOPING
        self.text_label = tk.Label(self, text="Init")
        self.text_label.place(relx=0.02, rely=0.965)

        # Developing
        self.animation = False  # todo delete this
        self.draw_geometry_from_definebcs()  # todo delete this
        ##################################################

    def window_assign_boundary_conditions(self):
        window_bcs = tk.Toplevel(self)
        window_bcs.title('ASSIGN SYSTEM PARAMETERS')
        window_bcs.geometry(f"{350}x{500}")
        window_bcs.resizable(False, False)
        window_bcs.config(bg=GUIStatics.WINDOWS_SMALL_BG_COLOR)

        widgets_x_start = 0.01
        GUIStatics.create_divider(window_bcs, widgets_x_start, 0.05, 335)







    def create_BC_params(self):
        """
        reformats the geometry for boundary and material parameters assignment via class CreateBCParams
        :return:
        """

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
        self.text_label.config(text=geometry_input_str, font=("Helvetica", 6))  # todo, for testing

        format_for_params = CreateBCParams(self.geometry_input)
        self.regions, self.boundaries, self.nodes = format_for_params.main()
        self.draw_geometry_from_definebcs()


    def draw_geometry_from_definebcs(self):
        """
        draws the formated geometry (boundaries, vertices, regions from class  CreateBCParams
        :return:
        """
        print(self.regions)
        print(self.boundaries)
        print(self.nodes)
        all_canvas_elements = self.canvas.find_all()
        for elem in all_canvas_elements:
            self.canvas.delete(elem)
        GUIStatics.add_canvas_static_elements(self.canvas)

        # enable disabled buttons for bcs, materials, calc parametsr
        self.button_define_bcs.config(state="normal")
        self.button_define_materials.config(state="normal")
        self.button_define_calc_params.config(state="normal")

        # update information field
        text_regions = [f"{region_nbr}: {values['coordinates']}, ({'+' if values['area_neg_pos'] == 'Positive' else '-'})\n"
                   for region_nbr, values in self.regions.items()]
        text_boundaries = [f"{bound_nbr}: {values} | " for bound_nbr, values in self.boundaries.items()]
        text_nodes = [f"{node_nbr}: {values} | " for node_nbr, values in self.nodes.items()]
        self.text_information_str = f"Regions:\n" + ''.join(text_regions) \
                                    + '\nBoundaries:\n' + ''.join(text_boundaries) \
                                    + '\n\nNodes:\n' + ''.join(text_nodes)
        GUIStatics.update_text_field(self.text_information, self.text_information_str)

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
            self.canvas.create_line(sector_start_node, sector_end_node, fill='#2F1417', width=2, dash=(1, 1), arrow='both', arrowshape=(8, 10, 3))
            self.canvas.create_text(center_x, center_y, text=text, fill='#420382', font=GUIStatics.STANDARD_FONT_SMALL)

        # draw points
        for node_nbr, node in self.nodes.items():
            node = GUIStatics.transform_node_to_canvas(node)
            text = f'N:{node_nbr}'
            self.canvas.create_oval(node[0] - 4, node[1] - 4, node[0] + 4, node[1] + 4, fill='#5F0F0F',
                                    outline='#1F1F1F', width=2, dash=(1, 1))
            self.canvas.create_text(node[0] - 10, node[1] - 10, text=text, fill='#14380A', font=GUIStatics.STANDARD_FONT_SMALL)

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




if __name__ == '__main__':
    gui = GUI()  # Todo - Develop: For testing main gui
    #gui = Geometry(lambda x: x)  # Todo - Develop: For testing Geometry gui, argument simulates callback
    gui.mainloop()
