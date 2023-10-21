import tkinter as tk
import math
from typing import Callable, Any

#################################################
# Other
AUTHOR = 'Itsame Mario'
VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 0


#################################################


class GUIStatics:
    """
    Define constants and static methods
    """

    # FONTS
    # STANDARD_FONT_1_BOLD = tkFont.Font(family="Arial", size=12, weight='bold')
    # Main Window
    MAIN_WINDOW_SIZE_X = 1200
    MAIN_WINDOW_SIZE_Y = 800

    # Geometry Window
    GEOM_WINDOW_SIZE_X = 1200
    GEOM_WINDOW_SIZE_Y = 800

    # Standard Canvas Size
    CANVAS_SIZE_X = 920  # Needs to be even!
    CANVAS_SIZE_Y = 720  # Needs to be even!
    GRID_SPACE = 10  # Needs to be divisor of GUIStatics.CANVAS_SIZE_X and GUIStatics.CANVAS_SIZE_Y
    CANVAS_SCALE_FACTOR = 100

    # colors
    CANVAS_BORDER_COLOR = '#5F1010'  # Rosewood
    CANVAS_BG = '#D2D2D2'  # Light gray
    CANVAS_COORD_COLOR = '#262626'  # Dark gray

    # Fonts
    STANDARD_FONT_BUTTON_SMALLER = ('Consolas', 8)
    STANDARD_FONT_BUTTON_SMALL = ('Consolas', 9)
    STANDARD_FONT_BUTTON_MID = ('Consolas', 10)
    STANDARD_FONT_BUTTON_BIG = ('Consolas', 11)
    STANDARD_FONT_BUTTON_BIG_BOLD = ('Arial Black', 11)
    STANDARD_FONT_MID = ('Arial', 10)
    STANDARD_FONT_MID_BOLD = ('Arial Black', 10)
    STANDARD_FONT_SMALL = ('Arial', 9)
    STANDARD_FONT_SMALLER = ('Arial', 8)
    STANDARD_FONT_SMALL_BOLD = ('Arial Black', 9)
    SAVELOAD_FONT = ('Verdana', 10)

    @staticmethod
    def resort_keys(some_dict: dict) -> dict:
        """
        resort the dict (keys: str), if key is missing, assign following keys to it
        e.g {'1': 1, '3': 3, '4': 4, '5': 5} -> {'1': 1, '2': 3, '3': 4, '4': 5}

        :param some_dict: {'1': 1, '3': 3, '4': 4, '5': 5}
        :return:
        """

        # get missing key
        keys = some_dict.keys()
        mi_ma = set(range(int(min(keys)), int(max(keys)) + 1))
        missing_key = list(mi_ma - mi_ma.intersection(set([int(key) for key in keys])))
        # sort again
        if not missing_key and min(keys) != '1':
            return dict(sorted(some_dict.items()))
        else:
            missing_key = '0' if min(keys) == '1' else missing_key[0]
            next_key, last_key = int(missing_key) + 1, max([int(key) for key in keys])
            for key in range(next_key, last_key + 1):
                some_dict[str(key - 1)] = some_dict[str(key)]
            del some_dict[str(key)]

            return dict(sorted(some_dict.items()))

    @staticmethod
    def transform_node_to_canvas(node: list):
        """
        Transforms the coordinates of node from natural coord system to canvas coord system
        e.g. [1.0, 2.0] -> [300, 200]
        :param node: [x, y] in natural coordinates
        :return:
        """

        scale_factor = GUIStatics.CANVAS_SCALE_FACTOR
        node_x = node[0]
        node_y = node[1]
        node_new_x = node_x * scale_factor + GUIStatics.CANVAS_SIZE_X / 2
        node_new_y = -node_y * scale_factor + GUIStatics.CANVAS_SIZE_Y / 2

        return node_new_x, node_new_y

    # shared method
    @staticmethod
    def add_canvas_static_elements(canvas: tk.Canvas):
        """
        Adds coordsystem and grid to a canvas
        :param canvas:
        :return:
        """

        width = GUIStatics.CANVAS_SIZE_X
        height = GUIStatics.CANVAS_SIZE_Y

        # grid
        for x in range(GUIStatics.GRID_SPACE, width + GUIStatics.GRID_SPACE, GUIStatics.GRID_SPACE):
            canvas.create_line(x, 0, x, height, fill="dark gray", width=1)
        for y in range(GUIStatics.GRID_SPACE, height, GUIStatics.GRID_SPACE):
            canvas.create_line(0, y, width, y, fill="dark gray", width=1)
        canvas.create_line(1, 1, width, 1, fill=GUIStatics.CANVAS_BORDER_COLOR, width=4)
        canvas.create_line(1, 0, 1, height, fill=GUIStatics.CANVAS_BORDER_COLOR, width=6)
        canvas.create_line(0, height + 1, width, height + 1,
                           fill=GUIStatics.CANVAS_BORDER_COLOR, width=2)
        canvas.create_line(width + 1, 0, width + 1, height,
                           fill=GUIStatics.CANVAS_BORDER_COLOR, width=2)

        # coordinatesystem
        canvas.create_line(width / 2, 0, width / 2, height,
                           fill=GUIStatics.CANVAS_COORD_COLOR, width=1)
        canvas.create_line(0, height / 2, width, height / 2,
                           fill=GUIStatics.CANVAS_COORD_COLOR, width=1)

        # text_values
        text_color = '#575757'
        div_color = '#404040'
        x_it = 0
        for x in range(int(width / 2), width, GUIStatics.GRID_SPACE * 2):
            x_text = x_it / GUIStatics.CANVAS_SCALE_FACTOR
            x_it += GUIStatics.GRID_SPACE * 2
            if x_text == 0:
                x_text = 0
            canvas.create_text(x + 4, height / 2 + 10, text=x_text, fill=text_color, font=("Helvetica", 6))
            canvas.create_line(x, height / 2 + 3, x, height / 2 - 3, fill=div_color, width=1)

        x_it = 0
        for x in range(int(width / 2), 0, -GUIStatics.GRID_SPACE * 2):
            x_text = x_it / GUIStatics.CANVAS_SCALE_FACTOR
            x_it += GUIStatics.GRID_SPACE * 2
            x_text = '-' + str(x_text)
            if x_text == '-0.0':
                x_text = ''
            canvas.create_text(x + 4, height / 2 + 10, text=x_text, fill=text_color, font=("Helvetica", 6))
            canvas.create_line(x, height / 2 + 3, x, height / 2 - 3, fill=div_color, width=1)

        y_it = 0
        for y in range(int(height / 2), height, GUIStatics.GRID_SPACE * 2):
            y_text = y_it / GUIStatics.CANVAS_SCALE_FACTOR
            y_it += GUIStatics.GRID_SPACE * 2
            y_text = '-' + str(y_text)
            if y_text == '-0.0':
                y_text = ''
            canvas.create_text(width / 2 + 10, y, text=y_text, fill=text_color, font=("Helvetica", 6))
            canvas.create_line(width / 2 - 3, y, width / 2 + 3, y, fill=div_color, width=1)

        y_it = 0
        for y in range(int(height / 2), 0, -GUIStatics.GRID_SPACE * 2):
            y_text = y_it / GUIStatics.CANVAS_SCALE_FACTOR
            y_it += GUIStatics.GRID_SPACE * 2
            y_text = str(y_text)
            if y_text == '0.0':
                y_text = ''
            canvas.create_text(width / 2 + 10, y, text=y_text, fill=text_color, font=("Helvetica", 6))
            canvas.create_line(width / 2 - 3, y, width / 2 + 3, y, fill=div_color, width=1)


class GUI(tk.Tk):
    """
    main class for calling other classes geometry, mesh creation, calculation and output
    """

    def __init__(self):
        """
        Constructor, inherits from tkinter
        """

        super().__init__()

        # Start Main Window
        self.main_window()
        self.resizable(False, False)
        # main input and output variables
        self.geometry_input = None

    def main_window(self):
        """
        Defines Main Window
        :return:
        """

        self.title('TinyFEM - MAIN WINDOW')
        self.geometry(f"{GUIStatics.MAIN_WINDOW_SIZE_X}x{GUIStatics.MAIN_WINDOW_SIZE_Y}")

        # Button define Geometry
        button_define_geometry = tk.Button(self, text="DEFINE GEOMETRY", command=self.define_geometry, width=20,
                                           height=1)
        button_define_geometry.place(relx=0.025, rely=0.05)

        # placeholder for text
        self.text_label = tk.Label(self, text="Init")
        self.text_label.place(relx=0.4, rely=0.4)

    def define_geometry(self):
        """
        Executed when button "DEFINE GEOMETRY" pressed, creates callback for Class Geometry
        :return:
        """
        return_geometry = Geometry(self.receive_geometry)

    def receive_geometry(self, geometry):
        """
        Gets geometry input from class Geometry
        :param geometry:
        :return:
        """
        self.geometry_input = str(geometry)
        self.text_label.config(text=self.geometry_input)


class Geometry(tk.Toplevel):
    """
    Define Geometry Window
    """

    def __init__(self, callback_geometry: Callable[[dict], Any]):
        """
        Constructor, inherits from tk toplevel
        :param callback_geometry: callback method from class GUI
        """

        # Callback geometry to return geometry values to guimain
        self.callback_geometry = callback_geometry
        self.geometry_input = None
        self.polygons = {'0': {'coordinates': [], 'area_neg_pos': 'Positive'}}  # init value
        self.polygons = {'0': {'coordinates': [[0, 0], [1, 0.5], [1.5, 1.5], [0.75, 2.0]], 'area_neg_pos': 'Positive'},
                         '1': {'coordinates': [[-1, -1], [-2, -1], [-3, -3], [-2, -3]], 'area_neg_pos': 'Positive'},
                         '2': {'coordinates': [[1, -0.5], [3, -1], [3, -3.5], [2, -2.5], [0.5, -4]],
                               'area_neg_pos': 'Negative'}}  # TEST TODO
        self.polygon_nodes = [0]  # needed for update for select polygon dropdown (numbers for polygons in list)
        self.points = {}  # init value
        #self.points = {'0': [0, 1], '1': [2, 3], '2': [-2, 3]}  # testing todo
        super().__init__()
        self.main_window()

    def main_window(self):
        """
        Creates main window for class Geometry
        :return:
        """

        self.title('TinyFEM - DEFINE GEOMETRY')
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

        ##################################################
        # save and load buttons
        # save geometry button
        button_save_geo = tk.Button(self, text="SAVE", command=self.save_geometry,
                                    font=GUIStatics.SAVELOAD_FONT, width=10, height=1)
        button_save_geo.place(relx=widgets_x_start, rely=0.02)

        # load geometry button
        button_load_geo = tk.Button(self, text="LOAD", command=self.load_geometry,
                                    font=GUIStatics.SAVELOAD_FONT, width=10, height=1)
        button_load_geo.place(relx=0.1, rely=0.02)

        ##################################################

        ##################################################
        # unit selector
        def update_unit_text(*args):
            """
            Updates label text when unit is selected from dropdown menu
            :param args:
            :return:
            """
            unit_selected = unit_var.get()
            units_dict = {'m': 'meter', 'mm': 'milimeter', 'km': 'kilometer', 'hm': 'hektometer', 'dam': 'dekameter',
                          'dm': 'dezimeter', 'cm': 'centimeter'}
            self.unit_selected.config(text=units_dict[unit_selected])

        unit_select_label = tk.Label(self, text="Unit:", font=GUIStatics.STANDARD_FONT_SMALL_BOLD)
        unit_select_label.place(relx=0.835, rely=0.04)
        units = ['m', 'mm', 'km', 'hm', 'dam', 'dm', 'cm']
        unit_var = tk.StringVar()
        unit_var.set(units[0])  # default value m
        dropdown_unit_select = tk.OptionMenu(self, unit_var, *units)
        dropdown_unit_select.config(font=GUIStatics.STANDARD_FONT_SMALL, width=2, height=1)
        dropdown_unit_select.place(relx=0.865, rely=0.034)
        self.unit_selected = tk.Label(self, text='meter', font=GUIStatics.STANDARD_FONT_SMALL)
        self.unit_selected.place(relx=0.92, rely=0.04)
        unit_var.trace('w', update_unit_text)

        ##################################################

        ##################################################
        # Polygon definition

        def update_dropdown_polygon_node_select_poly_info(*args):
            """
            updates the dropdown_polygon_node_select optionMenu for the nodes set in the polygon set
            in dropdown_polygon_select  optionMenu
            Also updates the instance variable self.polygon_nodes
            :param args:
            :return:
            """
            # updates the polygon selection menu
            polygons_numbered = range(0, len(self.polygons)) if self.polygons else ['None']
            dropdown_polygon_select["menu"].delete(0, "end")
            for option in polygons_numbered:
                dropdown_polygon_select["menu"].add_command(label=option,
                                                                 command=tk._setit(polygon_select_var, option))
            # updates the polygon nodes dropdown menu and the info field for nodes
            active_polygon = self.polygons.get(polygon_select_var.get(), None)
            if active_polygon == 'None':
                dropdown_polygon_node_select["state"] = "disabled"
            else:
                dropdown_polygon_node_select["state"] = "normal"
            if self.polygons:
                self.polygon_nodes = range(0, len(active_polygon['coordinates']))
                dropdown_polygon_node_select["menu"].delete(0, "end")
                for option in self.polygon_nodes:
                    dropdown_polygon_node_select["menu"].add_command(label=option,
                                                                     command=tk._setit(polygon_node_var, option))
                area_neg_pos_var.set(active_polygon['area_neg_pos'])
                update_polygon_nodes_info()
            else:
                polygon_nodes_text.config(state='normal')
                polygon_nodes_text.delete('0.0', 'end')
                polygon_nodes_text.insert('end', 'None')
                polygon_nodes_text.config(state='disabled')

        def update_polygon_nodes_info():
            """
            updates the info field for polygon nodes
            :return:
            """
            active_polygon = self.polygons.get(polygon_select_var.get(), None)
            print(active_polygon)
            polygon_nodes_text.config(state='normal')
            polygon_nodes_text.delete('0.0', 'end')
            polygon_nodes_text.insert('end', str(active_polygon['coordinates']))
            polygon_nodes_text.config(state='disabled')

        def update_x_y_entry_polygon_node(*args):
            """
            Updates the x and y values for the selected polygon and node
            :param args:
            :return:
            """
            active_polygon = self.polygons.get(polygon_select_var.get(), None)
            if active_polygon == 'None':
                return None
            polygon_nodes = active_polygon['coordinates']
            active_polygon_node = int(polygon_node_var.get())
            node_coords = polygon_nodes[active_polygon_node]
            add_node_x_entry.delete(0, 'end')
            add_node_x_entry.insert('end', str(node_coords[0]))
            add_node_y_entry.delete(0, 'end')
            add_node_y_entry.insert('end', str(node_coords[1]))

        def new_polygon():
            """
            create new polygon on click button NEW
            :return:
            """
            if not self.polygons:
                self.polygons = {'0': {'coordinates': [], 'area_neg_pos': 'Positive'}}
                dropdown_polygon_select["state"] = "normal"
                polygon_select_var.set('0')
                update_polygon_nodes_info()
                update_dropdown_polygon_node_select_poly_info()
            else:
                new_index = str(1 + int(max(self.polygons.keys())))
                self.polygons[new_index] = {'coordinates': [], 'area_neg_pos': 'Positive'}
                update_dropdown_polygon_node_select_poly_info()
                polygon_select_var.set(new_index)





        polygon_def_label = tk.Label(self, text="Define Polygon", font=GUIStatics.STANDARD_FONT_MID_BOLD)
        polygon_def_label.place(relx=widgets_x_start, rely=0.1)

        polygon_select_label = tk.Label(self, text="Select Polygon:", font=GUIStatics.STANDARD_FONT_SMALL)
        polygon_select_label.place(relx=widgets_x_start, rely=0.135)
        self.polygon_selection = [elem for elem in self.polygons.keys()]
        polygon_select_var = tk.StringVar()
        polygon_select_var.set('None')
        dropdown_polygon_select = tk.OptionMenu(self, polygon_select_var, *self.polygon_selection)
        dropdown_polygon_select.config(font=GUIStatics.STANDARD_FONT_SMALL, width=4, height=1)
        dropdown_polygon_select.place(relx=widgets_x_start + 0.075, rely=0.13)
        polygon_select_var.trace('w', update_dropdown_polygon_node_select_poly_info)

        new_poly_button = tk.Button(self, text="NEW", command=new_polygon,
                                    width=7, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALL)
        new_poly_button.place(relx=widgets_x_start + 0.145, rely=0.133)

        polygon_node_select_label = tk.Label(self, text="Select Node:", font=GUIStatics.STANDARD_FONT_SMALL)
        polygon_node_select_label.place(relx=widgets_x_start, rely=0.185)
        polygon_node_var = tk.StringVar()
        polygon_node_var.set('None')
        dropdown_polygon_node_select = tk.OptionMenu(self, polygon_node_var, *self.polygon_nodes)
        dropdown_polygon_node_select.config(font=GUIStatics.STANDARD_FONT_SMALL, width=4, height=1)
        dropdown_polygon_node_select.place(relx=widgets_x_start + 0.075, rely=0.18)
        dropdown_polygon_node_select["state"] = "disabled"
        polygon_node_var.trace('w', update_x_y_entry_polygon_node)

        add_poly_select_label = tk.Label(self, text="Add/Update Node:", font=GUIStatics.STANDARD_FONT_SMALL)
        add_poly_select_label.place(relx=widgets_x_start, rely=0.225)

        add_node_x_label = tk.Label(self, text="X:", font=GUIStatics.STANDARD_FONT_SMALL)
        add_node_x_label.place(relx=widgets_x_start, rely=0.26)
        add_node_x_entry_val = tk.StringVar()
        add_node_x_entry_val.set('0')
        add_node_x_entry = tk.Entry(self, textvariable=add_node_x_entry_val,
                                    font=GUIStatics.STANDARD_FONT_SMALL, width=6)
        add_node_x_entry.place(relx=widgets_x_start + 0.02, rely=0.262)

        add_node_y_label = tk.Label(self, text="Y:", font=GUIStatics.STANDARD_FONT_SMALL)
        add_node_y_label.place(relx=widgets_x_start + 0.06, rely=0.26)
        add_node_y_entry_val = tk.StringVar()
        add_node_y_entry_val.set('0')
        add_node_y_entry = tk.Entry(self, textvariable=add_node_y_entry_val,
                                    font=GUIStatics.STANDARD_FONT_SMALL, width=6)
        add_node_y_entry.place(relx=widgets_x_start + 0.08, rely=0.262)

        def delete_poly_node():
            active_polygon = polygon_select_var.get()
            if active_polygon == 'None':
                return None
            selected_node = polygon_node_var.get()
            if selected_node == 'None':
                return None
            else:
                selected_node = int(polygon_node_var.get())
            del self.polygons[active_polygon]['coordinates'][selected_node]
            update_polygon_nodes_info()
            update_dropdown_polygon_node_select_poly_info()
            self.update_graphics()


        def add_poly_node():
            """
            When button ADD for polygon is pressed
            :return:
            """

            this_polygon = polygon_select_var.get()
            if this_polygon == 'None':
                return None
            dropdown_polygon_node_select["state"] = "normal"
            polygon_nodes = self.polygons[this_polygon]['coordinates']
            x_entry = float(add_node_x_entry_val.get())
            y_entry = float(add_node_y_entry_val.get())
            polygon_nodes.append([x_entry, y_entry])
            self.polygons[this_polygon]['coordinates'] = polygon_nodes
            update_dropdown_polygon_node_select_poly_info()
            update_polygon_nodes_info()
            self.update_graphics()

        def update_poly_node():
            """
            When button UPDATE for polygon is pressed
            :return:
            """
            this_polygon = polygon_select_var.get()
            if this_polygon == 'None':
                return None
            selected_node = polygon_node_var.get()
            if selected_node == 'None':
                return None
            else:
                selected_node = int(polygon_node_var.get())
            print(this_polygon, selected_node)
            x_value = float(add_node_x_entry.get())
            y_value = float(add_node_y_entry.get())
            area_value = area_neg_pos_var.get()
            self.polygons[this_polygon]['coordinates'][selected_node] = [x_value, y_value]
            self.polygons[this_polygon]['area_neg_pos'] = area_value
            update_polygon_nodes_info()
            self.update_graphics()

        add_poly_node_button = tk.Button(self, text="ADD", command=add_poly_node,
                                         width=11, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALLER)
        add_poly_node_button.place(relx=widgets_x_start + 0.125, rely=0.258)
        update_poly_node_button = tk.Button(self, text="UPDATE", command=update_poly_node,
                                            width=11, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALLER)
        update_poly_node_button.place(relx=widgets_x_start + 0.125, rely=0.289)
        delete_polygon_node_button = tk.Button(self, text="DELETE", command=delete_poly_node,
                                     width=11, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALLER)
        delete_polygon_node_button.place(relx=widgets_x_start + 0.125, rely=0.228)

        polygon_nodes_label = tk.Label(self, text="Polygon Nodes:", font=GUIStatics.STANDARD_FONT_SMALL)
        polygon_nodes_label.place(relx=widgets_x_start, rely=0.30)
        polygon_nodes_text = tk.Text(self, height=4, width=35, wrap=tk.WORD,
                                     font=GUIStatics.STANDARD_FONT_SMALLER, bg='light gray', fg='black')
        polygon_nodes_text.place(relx=widgets_x_start + 0.005, rely=0.33)
        polygon_nodes_text.insert(tk.END, 'None')
        polygon_nodes_text.config(state='disabled')

        area_neg_pos_label = tk.Label(self, text="Area:", font=GUIStatics.STANDARD_FONT_SMALL)
        area_neg_pos_label.place(relx=widgets_x_start, rely=0.42)
        area_neg_pos = ['Positive', 'Negative']
        area_neg_pos_var = tk.StringVar()
        area_neg_pos_var.set(area_neg_pos[0])
        area_neg_pos_select = tk.OptionMenu(self, area_neg_pos_var, *area_neg_pos)
        area_neg_pos_select.config(font=GUIStatics.STANDARD_FONT_SMALL, width=6, height=1)
        area_neg_pos_select.place(relx=widgets_x_start + 0.04, rely=0.415)

        def delete_polygon():
            """
            When button DELETE POLYGON for polygons is pressed
            :return:
            """
            active_polygon = polygon_select_var.get()
            if active_polygon != 'None':
                if len(self.polygons) > 1:
                    del self.polygons[active_polygon]
                    self.polygons = GUIStatics.resort_keys(self.polygons)
                    polygon_select_var.set('0')
                    update_dropdown_polygon_node_select_poly_info()
                    self.update_graphics()
                else:
                    del self.polygons[active_polygon]
                    polygon_select_var.set('None')
                    dropdown_polygon_node_select["state"] = "disabled"
                    dropdown_polygon_select["state"] = "disabled"
                    self.update_graphics()


        delete_polygon_button = tk.Button(self, text="DELETE POLYGON", command=delete_polygon,
                                          width=16, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALL)
        delete_polygon_button.place(relx=widgets_x_start, rely=0.465)

        ##################################################

        ##################################################
        # Single Point definition
        def new_point():
            """
            When button NEW for single point definition is pressed
            :return:
            """
            dropdown_single_point_select["state"] = "normal"
            # check if points already in self.points
            if not self.points or self.points == {'None'}:
                self.points = {'0': [0, 0]}
                selected_point = '0'
            else:
                selected_point = str(int(max(list(self.points.keys()))) + 1)
                self.points[selected_point] = [0, 0]
            update_point_select_dropdown()
            single_point_var.set(selected_point)
            self.update_graphics()

        def update_point_select_dropdown():
            """
            updates the select point dropdown menu
            :return:
            """
            points_numbered = range(0, len(self.points)) if self.points else ['None']
            dropdown_single_point_select["menu"].delete(0, "end")
            for option in points_numbered:
                dropdown_single_point_select["menu"].add_command(label=option,
                                                                 command=tk._setit(single_point_var, option))

        single_point_def_label = tk.Label(self, text="Define Point", font=GUIStatics.STANDARD_FONT_MID_BOLD)
        single_point_def_label.place(relx=widgets_x_start, rely=0.55)

        def update_x_y_select_point(*args):
            """
            Updates the x and y values for the selected polygon and node
            :param args:
            :return:
            """
            selected_point = single_point_var.get()
            if selected_point == 'None' or not self.points:
                node_coords = [0, 0]
            else:
                node_coords = self.points[selected_point]
            add_point_x_entry.delete(0, 'end')
            add_point_x_entry.insert('end', str(node_coords[0]))
            add_point_y_entry.delete(0, 'end')
            add_point_y_entry.insert('end', str(node_coords[1]))

        single_point_select_label = tk.Label(self, text="Select Point:", font=GUIStatics.STANDARD_FONT_SMALL)
        single_point_select_label.place(relx=widgets_x_start, rely=0.585)
        single_point_var = tk.StringVar()
        single_point_var.set('None')
        if not self.points:
            self.points = {'None'}
        dropdown_single_point_select = tk.OptionMenu(self, single_point_var, *self.points)
        dropdown_single_point_select.config(font=GUIStatics.STANDARD_FONT_SMALL, width=4, height=1)
        dropdown_single_point_select.place(relx=widgets_x_start + 0.075, rely=0.58)
        dropdown_single_point_select["state"] = "disabled"
        single_point_var.trace('w', update_x_y_select_point)

        new_point_button = tk.Button(self, text="NEW", command=new_point,
                                     width=7, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALL)
        new_point_button.place(relx=widgets_x_start + 0.145, rely=0.583)

        add_point_select_label = tk.Label(self, text="Update Point:", font=GUIStatics.STANDARD_FONT_SMALL)
        add_point_select_label.place(relx=widgets_x_start, rely=0.63)

        add_point_x_label = tk.Label(self, text="X:", font=GUIStatics.STANDARD_FONT_SMALL)
        add_point_x_label.place(relx=widgets_x_start, rely=0.665)
        add_point_x_entry_val = tk.StringVar()
        add_point_x_entry_val.set('0')
        add_point_x_entry = tk.Entry(self, textvariable=add_point_x_entry_val,
                                     font=GUIStatics.STANDARD_FONT_SMALL, width=6)
        add_point_x_entry.place(relx=widgets_x_start + 0.02, rely=0.667)

        add_point_y_label = tk.Label(self, text="Y:", font=GUIStatics.STANDARD_FONT_SMALL)
        add_point_y_label.place(relx=widgets_x_start + 0.06, rely=0.665)
        add_point_y_entry_val = tk.StringVar()
        add_point_y_entry_val.set('0')
        add_point_y_entry = tk.Entry(self, textvariable=add_point_y_entry_val,
                                     font=GUIStatics.STANDARD_FONT_SMALL, width=6)
        add_point_y_entry.place(relx=widgets_x_start + 0.08, rely=0.667)

        def update_point():
            """
            gets the selected point from dropdown and values from x and y field
            and updates the values for selected point
            :return:
            """
            if not self.points:
                return None
            selected_point = single_point_var.get()
            if selected_point == 'None':
                return None
            new_x = add_point_x_entry_val.get()
            new_y = add_point_y_entry_val.get()
            self.points[selected_point] = [float(new_x), float(new_y)]
            self.update_graphics()

        def delete_point():
            """
            deletes specified point in dropdown menu and resorts dict
            :return:
            """
            selected_point = single_point_var.get()

            if selected_point == 'None':
                return None
            del self.points[selected_point]
            if not self.points:
                single_point_var.set('None')
                dropdown_single_point_select["state"] = "disabled"
                self.update_graphics()
                return None
            self.points = GUIStatics.resort_keys(self.points)
            update_point_select_dropdown()
            single_point_var.set('0')
            self.update_graphics()

        add_point_button = tk.Button(self, text="UPDATE", command=update_point,
                                     width=11, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALLER)
        add_point_button.place(relx=widgets_x_start + 0.125, rely=0.663)

        delete_point_button = tk.Button(self, text="DELETE POINT", command=delete_point,
                                        width=14, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALL)
        delete_point_button.place(relx=widgets_x_start, rely=0.71)
        ##################################################

        ##################################################
        # Add canvas for system visualization - DYNAMIC
        self.canvas = tk.Canvas(self, width=GUIStatics.CANVAS_SIZE_X, height=GUIStatics.CANVAS_SIZE_Y,
                                bg=GUIStatics.CANVAS_BG)
        self.canvas.place(relx=canvas_x + 0.0075, rely=canvas_y)
        GUIStatics.add_canvas_static_elements(self.canvas)
        ##################################################

        ##################################################
        # Update graphics
        button_update_graphics = tk.Button(self, text="UPDATE GRAPHICS", command=self.update_graphics,
                                           width=22, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_MID)
        button_update_graphics.place(relx=0.025, rely=0.885)

        # Accept Geometry button - returns value for geometry input and destroys window
        button_accept = tk.Button(self, text="ACCEPT GEOMETRY", command=self.return_geometry,
                                  width=16, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_BIG_BOLD)
        button_accept.place(relx=0.025, rely=0.935)

        ##################################################

        ##################################################
        # For debugging
        def debug():
            """
            when button DEBUG is pressed
            :return:
            """
            print("\n\n")
            print(f"self.polygons: {self.polygons}")
            print(f"self.polygon_nodes: {self.polygon_nodes}")
            print(f"self.points: {self.points}")

        button_debug = tk.Button(self, text="DEBUG", command=debug,
                                 width=5, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALLER)
        button_debug.place(relx=0.95, rely=0.01)
        ##################################################

    def update_graphics(self):
        """
        Updates the canvas, draws static elements (coordsystem, grid) and draws defined polygons and single points
        :return:
        """

        # delete all
        all_canvas_elements = self.canvas.find_all()
        for elem in all_canvas_elements:
            self.canvas.delete(elem)

        # add grid etc
        GUIStatics.add_canvas_static_elements(self.canvas)

        # draw polygons
        for polygon_nbr, polygon_data in self.polygons.items():

            color_code_plus = '#7D4C4C'
            color_code_minus = '#222638'
            color_code_plus_node = '#5F0F0F'
            color_code_minus_node = '#3A4571'

            polygon_nodes = polygon_data['coordinates']
            if len(polygon_nodes) < 3:
                continue
            polygon_nodes_transformed = [GUIStatics.transform_node_to_canvas(node) for node in polygon_nodes]
            polygon_neg_pos = polygon_data['area_neg_pos']  # either 'Positive' or 'Negative'
            color_code = color_code_plus if polygon_neg_pos == 'Positive' else color_code_minus
            color_code_node = color_code_plus_node if polygon_neg_pos == 'Positive' else color_code_minus_node
            self.canvas.create_polygon(polygon_nodes_transformed, fill=color_code, outline='#341010', width=2)

            # add text to polygon, todo: position besser finden
            middle_node = math.floor(len(polygon_nodes_transformed) / 2)
            if middle_node == 0:
                middle_node = 1
            text = f'Polygon {polygon_nbr}'
            color_code_text = '#1F1F1F' if polygon_neg_pos == 'Positive' else '#B1C0C2'
            center_node_approx_x = math.floor(abs((polygon_nodes_transformed[middle_node][0] +
                                                   polygon_nodes_transformed[0][0]) / 2))
            center_node_approx_y = math.floor(abs((polygon_nodes_transformed[middle_node][1] +
                                                   polygon_nodes_transformed[0][1]) / 2))
            self.canvas.create_text(center_node_approx_x, center_node_approx_y, text=text, fill=color_code_text,
                                    font=("Helvetica", 7))

            # add nodes
            for node in polygon_nodes:
                node = GUIStatics.transform_node_to_canvas(node)
                self.canvas.create_oval(node[0] - 3, node[1] - 3, node[0] + 3, node[1] + 3, fill=color_code_node,
                                        outline='#1F1F1F', width=1)

        # draw points
        if self.points != {'None'} and self.points:
            for point_nbr, node in self.points.items():
                node = GUIStatics.transform_node_to_canvas(node)
                text = f'Point {point_nbr}'
                self.canvas.create_oval(node[0] - 4, node[1] - 4, node[0] + 4, node[1] + 4, fill='#2D0F0F',
                                        outline='#1F1F1F', width=1)
                self.canvas.create_text(node[0], node[1] - 10, text=text, fill='#1F1F1F', font=("Helvetica", 7))

    def save_geometry(self):
        ...

    def load_geometry(self):
        ...

    def return_geometry(self):
        """
        Callback method to return defined geometry to main class GUI
        :return:
        """
        # todo: check if geometry is valid e.g. polgones have to be connects,
        #  only one polygon can be subtracted, points have to be in valid area, etc.
        value = 999
        self.callback_geometry(value)
        self.destroy()  # closes top window


if __name__ == '__main__':
    # gui = GUI()  # Todo - Develop: For testing main gui
    gui = Geometry(lambda x: x)  # Todo - Develop: For testing Geometry gui, argument simulates callback
    gui.mainloop()
