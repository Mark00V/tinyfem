import tkinter as tk
import tkinter.font as tkFont

#################################################
# Other
AUTHOR = 'Itsame Mario'
VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 0


#################################################




class GUI(tk.Tk):
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
    GRID_SPACE = 10  # Needs to be divisor of CANVAS_SIZE_X and CANVAS_SIZE_Y

    # colors
    CANVAS_BORDER_COLOR = '#5F1010'  # Rosewood
    CANVAS_BG = '#D2D2D2'  # Light gray
    CANVAS_COORD_COLOR = '#262626'  # Dark gray

    # Fonts
    STANDARD_FONT_BUTTON_SMALLER = ('Arial', 8)
    STANDARD_FONT_BUTTON_SMALL = ('Arial', 9)
    STANDARD_FONT_BUTTON_MID = ('Arial', 10)
    STANDARD_FONT_BUTTON_BIG = ('Arial', 11)
    STANDARD_FONT_BUTTON_BIG_BOLD = ('Arial Black', 11)
    STANDARD_FONT_MID = ('Arial', 10)
    STANDARD_FONT_MID_BOLD = ('Arial Black', 10)
    STANDARD_FONT_SMALL = ('Arial', 9)
    STANDARD_FONT_SMALLER = ('Arial', 8)
    STANDARD_FONT_SMALL_BOLD = ('Arial Black', 9)

    def __init__(self):

        super().__init__()

        # Start Main Window
        self.main_window()
        self.resizable(False, False)
        # main input and output variables
        self.geometry_input = None


    def main_window(self):
        """

        :return:
        """
        self.title('TinyFEM - MAIN WINDOW')
        self.geometry(f"{self.MAIN_WINDOW_SIZE_X}x{self.MAIN_WINDOW_SIZE_Y}")

        button_define_geometry = tk.Button(self, text="DEFINE GEOMETRY", command=self.define_geometry, width=20,
                                           height=1)
        button_define_geometry.place(relx=0.025, rely=0.05)

        self.text_label = tk.Label(self, text="Init")
        self.text_label.place(relx=0.4, rely=0.4)

    def define_geometry(self):
        return_geometry = Geometry(self.receive_geometry)

    def receive_geometry(self, geometry):
        self.geometry_input = str(geometry)
        self.text_label.config(text=self.geometry_input)

    # shared method
    @staticmethod
    def add_canvas_static_elements(canvas: tk.Canvas):
        width = GUI.CANVAS_SIZE_X
        height = GUI.CANVAS_SIZE_Y

        # grid
        for x in range(GUI.GRID_SPACE, width + GUI.GRID_SPACE, GUI.GRID_SPACE):
            canvas.create_line(x, 0, x, height, fill="dark gray", width=1)
        for y in range(GUI.GRID_SPACE, height, GUI.GRID_SPACE):
            canvas.create_line(0, y, width, y, fill="dark gray", width=1)
        canvas.create_line(1, 1, width, 1, fill=GUI.CANVAS_BORDER_COLOR, width=4)
        canvas.create_line(1, 0, 1, height, fill=GUI.CANVAS_BORDER_COLOR, width=6)
        canvas.create_line(0, height + 1, width, height + 1,
                           fill=GUI.CANVAS_BORDER_COLOR, width=2)
        canvas.create_line(width + 1, 0, width + 1, height,
                           fill=GUI.CANVAS_BORDER_COLOR, width=2)

        # coordinatesystem
        canvas.create_line(width / 2, 0, width / 2, height,
                           fill=GUI.CANVAS_COORD_COLOR, width=1)
        canvas.create_line(0, height / 2, width, height / 2,
                           fill=GUI.CANVAS_COORD_COLOR, width=1)

        # text_values
        text_color = '#575757'
        div_color ='#404040'
        x_it = 0
        for x in range(int(width / 2), width, GUI.GRID_SPACE * 2):
            x_text = x_it/100
            x_it += GUI.GRID_SPACE * 2
            if x_text == 0:
                x_text = 0
            canvas.create_text(x + 4, height/ 2 + 10, text=x_text, fill=text_color, font=("Helvetica", 6))
            canvas.create_line(x, height/ 2 + 3, x, height/ 2 - 3, fill=div_color, width=1)

        x_it = 0
        for x in range(int(width / 2), 0, -GUI.GRID_SPACE * 2):
            x_text = x_it/100
            x_it += GUI.GRID_SPACE * 2
            x_text = '-' + str(x_text)
            if x_text == '-0.0':
                x_text = ''
            canvas.create_text(x + 4, height/ 2 + 10, text=x_text, fill=text_color, font=("Helvetica", 6))
            canvas.create_line(x, height/ 2 + 3, x, height/ 2 - 3, fill=div_color, width=1)

        y_it = 0
        for y in range(int(height / 2), height, GUI.GRID_SPACE * 2):
            y_text = y_it/100
            y_it += GUI.GRID_SPACE * 2
            y_text = '-' + str(y_text)
            if y_text == '-0.0':
                y_text = ''
            canvas.create_text(width / 2 + 10, y, text=y_text, fill=text_color, font=("Helvetica", 6))
            canvas.create_line(width / 2 -3, y, width / 2 +3, y, fill=div_color, width=1)

        y_it = 0
        for y in range(int(height / 2), 0, -GUI.GRID_SPACE * 2):
            y_text = y_it/100
            y_it += GUI.GRID_SPACE * 2
            y_text = str(y_text)
            if y_text == '0.0':
                y_text = ''
            canvas.create_text(width / 2 + 10, y, text=y_text, fill=text_color, font=("Helvetica", 6))
            canvas.create_line(width / 2 -3, y, width / 2 +3, y, fill=div_color, width=1)


class Geometry(GUI, tk.Toplevel):

    def __init__(self, callback_geometry):

        # Callback geometry to return geometry values to guimain
        self.callback_geometry = callback_geometry
        self.geometry_input = None
        self.polygons = {'0': {'coordinates': [[0, 0]], 'area_neg_pos': 'Positive'}} # init value
        self.polygons = {'0': {'coordinates': [[0, 0]], 'area_neg_pos': 'Positive'},
                         '1': {'coordinates': [[1, 1], [2, 1], [3, 3]], 'area_neg_pos': 'Positive'}} # TEST TODO
        self.polygon_nodes = [0]
        self.points = {'0': [0, 0]} # init value
        self.points = {'0': [0, 1], '1': [2, 3], '2': [2, 3]} # testing todo
        super().__init__()






    def main_window(self):
        """

        :return:
        """

        self.title('TinyFEM - DEFINE GEOMETRY')
        self.geometry(f"{GUI.GEOM_WINDOW_SIZE_X}x{GUI.GEOM_WINDOW_SIZE_Y}")

        ##################################################
        # Position of elements
        # canvas
        border = 0.025
        canvas_x = 1 - GUI.CANVAS_SIZE_X / GUI.GEOM_WINDOW_SIZE_X - border
        canvas_y = 1 - GUI.CANVAS_SIZE_Y / GUI.GEOM_WINDOW_SIZE_Y - border

        # buttons and text on left side
        widgets_x_start = 0.01
        ##################################################

        ##################################################
        # save and load buttons
        # save geometry button
        button_save_geo = tk.Button(self, text="SAVE", command=self.save_geometry,
                                    font=GUI.STANDARD_FONT_BUTTON_MID, width=10, height=1)
        button_save_geo.place(relx=widgets_x_start, rely=0.02)

        # load geometry button
        button_load_geo = tk.Button(self, text="LOAD", command=self.load_geometry,
                                    font=GUI.STANDARD_FONT_BUTTON_MID, width=10, height=1)
        button_load_geo.place(relx=0.1, rely=0.02)
        ##################################################

        ##################################################
        # unit selector
        def update_unit_text(*args):
            unit_selected = unit_var.get()
            units_dict = {'m': 'meter', 'mm': 'milimeter', 'km': 'kilometer', 'hm': 'hektometer', 'dam': 'dekameter',
                          'dm': 'dezimeter', 'cm': 'centimeter'}
            self.unit_selected.config(text=units_dict[unit_selected])

        unit_select_label = tk.Label(self, text="Unit:", font=GUI.STANDARD_FONT_SMALL_BOLD)
        unit_select_label.place(relx=0.835, rely=0.04)
        units = ['m', 'mm', 'km', 'hm', 'dam', 'dm', 'cm']
        unit_var = tk.StringVar()
        unit_var.set(units[0])  # default value m
        dropdown_unit_select = tk.OptionMenu(self, unit_var, *units)
        dropdown_unit_select.config(font=GUI.STANDARD_FONT_SMALL, width=2, height=1)
        dropdown_unit_select.place(relx=0.865, rely=0.034)
        self.unit_selected = tk.Label(self, text='meter', font=GUI.STANDARD_FONT_SMALL)
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
            active_polygon = self.polygons.get(polygon_select_var.get(), None)
            self.polygon_nodes = range(0, len(active_polygon['coordinates']))
            dropdown_polygon_node_select["menu"].delete(0, "end")
            for option in self.polygon_nodes:
                dropdown_polygon_node_select["menu"].add_command(label=option, command=tk._setit(polygon_node_var, option))
            polygon_nodes_text.config(state='normal')
            polygon_nodes_text.delete('0.0', 'end')  # todo: why the fuck here '0.0' and for add_node_x_entry 0
            polygon_nodes_text.insert('end', str(active_polygon['coordinates']))
            polygon_nodes_text.config(state='disabled')

        def update_x_y_entry_polygon_node(*args):
            """
            Updates the x and y values for the selected polygon and node
            :param args:
            :return:
            """
            active_polygon = self.polygons.get(polygon_select_var.get(), None)
            polygon_nodes = active_polygon['coordinates']
            active_polygon_node = int(polygon_node_var.get())
            node_coords = polygon_nodes[active_polygon_node]
            add_node_x_entry.delete(0, 'end')
            add_node_x_entry.insert('end', str(node_coords[0]))
            add_node_y_entry.delete(0, 'end')
            add_node_y_entry.insert('end', str(node_coords[1]))

        def new_polygon():
            ...

        polygon_def_label = tk.Label(self, text="Define Polygon", font=GUI.STANDARD_FONT_MID_BOLD)
        polygon_def_label.place(relx=widgets_x_start, rely=0.1)

        polygon_select_label = tk.Label(self, text="Select Polygon:", font=GUI.STANDARD_FONT_SMALL)
        polygon_select_label.place(relx=widgets_x_start, rely=0.135)
        self.polygon_selection = [elem for elem in self.polygons.keys()]
        polygon_select_var = tk.StringVar()
        polygon_select_var.set('None')
        dropdown_polygon_select = tk.OptionMenu(self, polygon_select_var, *self.polygon_selection)
        dropdown_polygon_select.config(font=GUI.STANDARD_FONT_SMALL, width=4, height=1)
        dropdown_polygon_select.place(relx=widgets_x_start + 0.075, rely=0.13)
        polygon_select_var.trace('w', update_dropdown_polygon_node_select_poly_info)

        new_poly_button = tk.Button(self, text="NEW", command=new_polygon,
                                 width=7, height=1, font=GUI.STANDARD_FONT_BUTTON_SMALL)
        new_poly_button.place(relx=widgets_x_start + 0.145, rely=0.133)

        polygon_node_select_label = tk.Label(self, text="Select Node:", font=GUI.STANDARD_FONT_SMALL)
        polygon_node_select_label.place(relx=widgets_x_start, rely=0.185)
        polygon_node_var = tk.StringVar()
        polygon_node_var.set('None')
        dropdown_polygon_node_select = tk.OptionMenu(self, polygon_node_var, *self.polygon_nodes)
        dropdown_polygon_node_select.config(font=GUI.STANDARD_FONT_SMALL, width=4, height=1)
        dropdown_polygon_node_select.place(relx=widgets_x_start + 0.075, rely=0.18)
        polygon_node_var.trace('w', update_x_y_entry_polygon_node)

        add_poly_select_label = tk.Label(self, text="Add/Adjust Node:", font=GUI.STANDARD_FONT_SMALL)
        add_poly_select_label.place(relx=widgets_x_start, rely=0.225)

        add_node_x_label = tk.Label(self, text="X:", font=GUI.STANDARD_FONT_SMALL)
        add_node_x_label.place(relx=widgets_x_start, rely=0.26)
        add_node_x_entry_val = tk.StringVar()
        add_node_x_entry_val.set('0')
        add_node_x_entry = tk.Entry(self, textvariable=add_node_x_entry_val, font=GUI.STANDARD_FONT_SMALL, width=6)
        add_node_x_entry.place(relx=widgets_x_start + 0.02, rely=0.262)

        add_node_y_label = tk.Label(self, text="Y:", font=GUI.STANDARD_FONT_SMALL)
        add_node_y_label.place(relx=widgets_x_start + 0.06, rely=0.26)
        add_node_y_entry_val = tk.StringVar()
        add_node_y_entry_val.set('0')
        add_node_y_entry = tk.Entry(self, textvariable=add_node_y_entry_val, font=GUI.STANDARD_FONT_SMALL, width=6)
        add_node_y_entry.place(relx=widgets_x_start + 0.08, rely=0.262)

        def add_poly_node():
            ...

        def update_poly_node():
            selected_poly = polygon_select_var.get()
            selected_node = polygon_node_var.get()
            x_value = add_node_x_entry.get()
            y_value = add_node_x_entry.get()
            area_value = area_neg_pos_var.get()

        add_poly_node_button = tk.Button(self, text="ADD", command=add_poly_node,
                                 width=11, height=1, font=GUI.STANDARD_FONT_BUTTON_SMALLER)
        add_poly_node_button.place(relx=widgets_x_start + 0.125, rely=0.258)
        update_poly_node_button = tk.Button(self, text="ADJUST", command=update_poly_node,
                                 width=11, height=1, font=GUI.STANDARD_FONT_BUTTON_SMALLER)
        update_poly_node_button.place(relx=widgets_x_start + 0.125, rely=0.289)

        polygon_nodes_label = tk.Label(self, text="Polygon Nodes:", font=GUI.STANDARD_FONT_SMALL)
        polygon_nodes_label.place(relx=widgets_x_start, rely=0.30)
        polygon_nodes_text = tk.Text(self, height=4, width=35, wrap=tk.WORD,
                                     font=GUI.STANDARD_FONT_SMALLER, bg='light gray', fg='black')
        polygon_nodes_text.place(relx=widgets_x_start + 0.005, rely=0.33)
        polygon_nodes_text.insert(tk.END, 'None')
        polygon_nodes_text.config(state='disabled')

        area_neg_pos_label = tk.Label(self, text="Area:", font=GUI.STANDARD_FONT_SMALL)
        area_neg_pos_label.place(relx=widgets_x_start, rely=0.42)
        area_neg_pos = ['Positive', 'Negative']
        area_neg_pos_var = tk.StringVar()
        area_neg_pos_var.set(area_neg_pos[0])
        area_neg_pos_select = tk.OptionMenu(self, area_neg_pos_var, *area_neg_pos)
        area_neg_pos_select.config(font=GUI.STANDARD_FONT_SMALL, width=6, height=1)
        area_neg_pos_select.place(relx=widgets_x_start + 0.04, rely=0.415)

        def delete_polygon():
            ...

        delete_polygon_button = tk.Button(self, text="DELETE POLY", command=delete_polygon,
                                 width=14, height=1, font=GUI.STANDARD_FONT_BUTTON_SMALL)
        delete_polygon_button.place(relx=widgets_x_start, rely=0.465)
        ##################################################

        ##################################################
        # Single Point definition
        def new_point():
            # check if points already in self.points
            if not self.points:
                self.points = {'0': [0, 0]}
                selected_point = '0'
            else:
                selected_point = str(int(max(list(self.points.keys()))) + 1)
                self.points[selected_point] = [0, 0]
            points_numbered = range(0, len(self.points))
            dropdown_single_point_select["menu"].delete(0, "end")
            for option in points_numbered:
                dropdown_single_point_select["menu"].add_command(label=option, command=tk._setit(single_point_var, option))
            single_point_var.set(selected_point)

        single_point_def_label = tk.Label(self, text="Define Point", font=GUI.STANDARD_FONT_MID_BOLD)
        single_point_def_label.place(relx=widgets_x_start, rely=0.55)

        def update_x_y_select_point(*args):
            """
            Updates the x and y values for the selected polygon and node
            :param args:
            :return:
            """
            selected_point = single_point_var.get()
            node_coords = self.points[selected_point]
            add_point_x_entry.delete(0, 'end')
            add_point_x_entry.insert('end', str(node_coords[0]))
            add_point_y_entry.delete(0, 'end')
            add_point_y_entry.insert('end', str(node_coords[1]))

        single_point_select_label = tk.Label(self, text="Select Point:", font=GUI.STANDARD_FONT_SMALL)
        single_point_select_label.place(relx=widgets_x_start, rely=0.585)
        single_point_var = tk.StringVar()
        single_point_var.set('None')
        dropdown_single_point_select = tk.OptionMenu(self, single_point_var, *self.points)
        dropdown_single_point_select.config(font=GUI.STANDARD_FONT_SMALL, width=4, height=1)
        dropdown_single_point_select.place(relx=widgets_x_start + 0.075, rely=0.58)
        single_point_var.trace('w', update_x_y_select_point)

        new_point_button = tk.Button(self, text="NEW", command=new_point,
                                 width=7, height=1, font=GUI.STANDARD_FONT_BUTTON_SMALL)
        new_point_button.place(relx=widgets_x_start + 0.145, rely=0.583)

        add_point_select_label = tk.Label(self, text="Adjust Point:", font=GUI.STANDARD_FONT_SMALL)
        add_point_select_label.place(relx=widgets_x_start, rely=0.63)

        add_point_x_label = tk.Label(self, text="X:", font=GUI.STANDARD_FONT_SMALL)
        add_point_x_label.place(relx=widgets_x_start, rely=0.665)
        add_point_x_entry_val = tk.StringVar()
        add_point_x_entry_val.set('0')
        add_point_x_entry = tk.Entry(self, textvariable=add_point_x_entry_val, font=GUI.STANDARD_FONT_SMALL, width=6)
        add_point_x_entry.place(relx=widgets_x_start + 0.02, rely=0.667)

        add_point_y_label = tk.Label(self, text="Y:", font=GUI.STANDARD_FONT_SMALL)
        add_point_y_label.place(relx=widgets_x_start + 0.06, rely=0.665)
        add_point_y_entry_val = tk.StringVar()
        add_point_y_entry_val.set('0')
        add_point_y_entry = tk.Entry(self, textvariable=add_point_y_entry_val, font=GUI.STANDARD_FONT_SMALL, width=6)
        add_point_y_entry.place(relx=widgets_x_start + 0.08, rely=0.667)

        def update_point():
            """
            gets the selected point from dropdown and values from x and y field
            and updates the values for selected point
            :return:
            """
            selected_point = single_point_var.get()
            new_x = add_point_x_entry_val.get()
            new_y = add_point_y_entry_val.get()
            self.points[selected_point] = [new_x, new_y]

        def delete_point():
            ...

        add_point_button = tk.Button(self, text="ADJUST", command=update_point,
                                 width=11, height=1, font=GUI.STANDARD_FONT_BUTTON_SMALLER)
        add_point_button.place(relx=widgets_x_start + 0.125, rely=0.663)

        delete_point_button = tk.Button(self, text="DELETE POINT", command=delete_point,
                                 width=14, height=1, font=GUI.STANDARD_FONT_BUTTON_SMALL)
        delete_point_button.place(relx=widgets_x_start, rely=0.83)
        ##################################################

        ##################################################
        # Add canvas for system visualization - DYNAMIC
        self.canvas = tk.Canvas(self, width=GUI.CANVAS_SIZE_X, height=GUI.CANVAS_SIZE_Y, bg=GUI.CANVAS_BG)
        self.canvas.place(relx=canvas_x + 0.0075, rely=canvas_y)
        GUI.add_canvas_static_elements(self.canvas)
        ##################################################

        ##################################################
        button_update_graphics = tk.Button(self, text="UPDATE GRAPHICS", command=self.update_graphics,
                                 width=22, height=1, font=GUI.STANDARD_FONT_BUTTON_MID)
        button_update_graphics.place(relx=0.025, rely=0.885)

        # Accept Geometry button - returns value for geometry input and destroys window
        button_accept = tk.Button(self, text="ACCEPT GEOMETRY", command=self.return_geometry,
                                 width=16, height=1, font=GUI.STANDARD_FONT_BUTTON_BIG_BOLD)
        button_accept.place(relx=0.025, rely=0.935)
        ##################################################

    def update_graphics(self):
        ...

    def save_geometry(self):
        ...

    def load_geometry(self):
        ...

    def return_geometry(self):
        # todo: check if geometry is valid e.g. polgones have to be connects,
        #  only one polygon can be subtracted, points have to be in valid area, etc.
        value = 999
        self.callback_geometry(value)
        self.destroy()  # closes top window


if __name__ == '__main__':
    #gui = GUI()  # Todo - Develop: For testing main gui
    gui = Geometry(lambda x: x)  # Todo - Develop: For testing Geometry gui, argument simulates callback
    gui.mainloop()
