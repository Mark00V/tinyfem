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
        # for development
        self.regions = {'0': {'coordinates': [(0.1, -0.2), (1.5, -0.2), (1.5, 1.1), (0.0, 1.1)], 'area_neg_pos': 'Positive'},
         '1': {'coordinates': [(0.6, 0.5), (0.8, 0.8), (0.8, 0.2)], 'area_neg_pos': 'Negative'},
         '2': {'coordinates': [(1.5, -1.5), (2.5, 0.0), (2.5, 2.5), (1.5, 2.5), (1.5, 1.1), (1.5, -0.2)],
               'area_neg_pos': 'Positive'}}
        self.boundaries = {'0': ((0.1, -0.2), (1.5, -0.2)), '1': ((1.5, -0.2), (1.5, 1.1)), '2': ((1.5, 1.1), (0.0, 1.1)),
         '3': ((0.0, 1.1), (0.1, -0.2)), '4': ((0.6, 0.5), (0.8, 0.8)), '5': ((0.8, 0.8), (0.8, 0.2)),
         '6': ((0.8, 0.2), (0.6, 0.5)), '7': ((1.5, -1.5), (2.5, 0.0)), '8': ((2.5, 0.0), (2.5, 2.5)),
         '9': ((2.5, 2.5), (1.5, 2.5)), '10': ((1.5, 2.5), (1.5, 1.1)), '11': ((1.5, -0.2), (1.5, -1.5))}
        self.nodes = {'0': (0.5, 0.5), '1': (2.0, 0.2), '2': (0.1, -0.2), '3': (1.5, -0.2), '4': (1.5, 1.1), '5': (0.0, 1.1),
         '6': (0.6, 0.5), '7': (0.8, 0.8), '8': (0.8, 0.2), '9': (1.5, -1.5), '10': (2.5, 0.0), '11': (2.5, 2.5),
         '12': (1.5, 2.5)}

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
        # Button define Geometry
        button_define_geometry = tk.Button(self, text="GEOMETRY", command=self.define_geometry, width=12,
                                           font=GUIStatics.STANDARD_FONT_BUTTON_BIG_BOLD, height=1)
        button_define_geometry.place(relx=0.025, rely=0.05)

        # Reformat Boundaryconditions via CreateBCParams todo: THIS IS ONLY NEEDED FOR DEVELOPMENT
        button_define_geometry = tk.Button(self, text="Format BCs", command=self.create_BC_params, width=20,
                                           height=1)
        button_define_geometry.place(relx=0.025, rely=0.25)

        # placeholder for text FOR DEVELOPING
        self.text_label = tk.Label(self, text="Init")
        self.text_label.place(relx=0.02, rely=0.965)

        # Developing
        self.animation = False  # todo delete this
        self.draw_geometry_from_definebcs()  # todo delete this
        ##################################################

    def create_BC_params(self):
        """
        reformats the geometry for boundary and material parameters assignment via class CreateBCParams
        :return:
        """
        # todo
        create_params = CreateBCParams(self.geometry_input)
        regions, boundaries, nodes = create_params.main()
        print(regions)
        print(boundaries)
        print(nodes)

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

        # draw regions
        for region_nbr, params in self.regions.items():
            nodes = params['coordinates']
            area_neg_pos = params['area_neg_pos']
            
            nodes = [GUIStatics.transform_node_to_canvas(node) for node in nodes]
            self.canvas.create_polygon(nodes, fill='gray', outline='#341010', width=2)






if __name__ == '__main__':
    gui = GUI()  # Todo - Develop: For testing main gui
    #gui = Geometry(lambda x: x)  # Todo - Develop: For testing Geometry gui, argument simulates callback
    gui.mainloop()
