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


class Geometry(GUI, tk.Toplevel):

    def __init__(self, callback_geometry):


        # Callback geometry to return geometry values to guimain
        self.callback_geometry = callback_geometry
        self.geometry_input = None
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

        def update_unit_text(*args):
            unit_selected = unit_var.get()
            units_dict = {'m': 'meter', 'mm': 'milimeter', 'km': 'kilometer', 'hm': 'hektometer', 'dam': 'dekameter',
                          'dm': 'dezimeter', 'cm': 'centimeter'}
            self.unit_selected.config(text=units_dict[unit_selected])
        unit_var.trace('w', update_unit_text)
        ##################################################

        ##################################################
        # Polygon definition
        polygon_def_label = tk.Label(self, text="Define Polygon", font=GUI.STANDARD_FONT_MID_BOLD)
        polygon_def_label.place(relx=widgets_x_start, rely=0.1)

        polygon_select_label = tk.Label(self, text="Select Polygon:", font=GUI.STANDARD_FONT_SMALL)
        polygon_select_label.place(relx=widgets_x_start, rely=0.135)
        polygons = ['None']
        polygon_select_var = tk.StringVar()
        polygon_select_var.set('None')
        dropdown_polygon_select = tk.OptionMenu(self, polygon_select_var, *polygons)
        dropdown_polygon_select.config(font=GUI.STANDARD_FONT_SMALL, width=4, height=1)
        dropdown_polygon_select.place(relx=widgets_x_start + 0.075, rely=0.13)

        polygon_node_select_label = tk.Label(self, text="Select Node:", font=GUI.STANDARD_FONT_SMALL)
        polygon_node_select_label.place(relx=widgets_x_start, rely=0.185)
        polygon_nodes = ['None']
        polygon_node_var = tk.StringVar()
        polygon_node_var.set('None')
        dropdown_polygon_node_select = tk.OptionMenu(self, polygon_node_var, *polygon_nodes)
        dropdown_polygon_node_select.config(font=GUI.STANDARD_FONT_SMALL, width=4, height=1)
        dropdown_polygon_node_select.place(relx=widgets_x_start + 0.075, rely=0.18)

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
        add_poly_node_button = tk.Button(self, text="ADD/ADJUST", command=add_poly_node,
                                 width=11, height=1, font=GUI.STANDARD_FONT_BUTTON_SMALL)
        add_poly_node_button.place(relx=widgets_x_start + 0.125, rely=0.258)

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
        area_neg_pos_var.set(area_neg_pos[1])
        area_neg_pos_select = tk.OptionMenu(self, area_neg_pos_var, *area_neg_pos)
        area_neg_pos_select.config(font=GUI.STANDARD_FONT_SMALL, width=6, height=1)
        area_neg_pos_select.place(relx=widgets_x_start + 0.04, rely=0.415)
        ##################################################

        ##################################################
        # Single Point definition
        single_point_def_label = tk.Label(self, text="Define Point", font=GUI.STANDARD_FONT_MID_BOLD)
        single_point_def_label.place(relx=widgets_x_start, rely=0.5)

        single_point_select_label = tk.Label(self, text="Select Point:", font=GUI.STANDARD_FONT_SMALL)
        single_point_select_label.place(relx=widgets_x_start, rely=0.535)
        single_points = ['None']
        single_point_var = tk.StringVar()
        single_point_var.set('None')
        dropdown_single_point_select = tk.OptionMenu(self, single_point_var, *single_points)
        dropdown_single_point_select.config(font=GUI.STANDARD_FONT_SMALL, width=4, height=1)
        dropdown_single_point_select.place(relx=widgets_x_start + 0.075, rely=0.53)

        add_point_select_label = tk.Label(self, text="Add/Adjust Point:", font=GUI.STANDARD_FONT_SMALL)
        add_point_select_label.place(relx=widgets_x_start, rely=0.58)

        add_point_x_label = tk.Label(self, text="X:", font=GUI.STANDARD_FONT_SMALL)
        add_point_x_label.place(relx=widgets_x_start, rely=0.615)
        add_point_x_entry_val = tk.StringVar()
        add_point_x_entry_val.set('0')
        add_point_x_entry = tk.Entry(self, textvariable=add_point_x_entry_val, font=GUI.STANDARD_FONT_SMALL, width=6)
        add_point_x_entry.place(relx=widgets_x_start + 0.02, rely=0.617)

        add_point_y_label = tk.Label(self, text="Y:", font=GUI.STANDARD_FONT_SMALL)
        add_point_y_label.place(relx=widgets_x_start + 0.06, rely=0.615)
        add_point_y_entry_val = tk.StringVar()
        add_point_y_entry_val.set('0')
        add_point_y_entry = tk.Entry(self, textvariable=add_point_y_entry_val, font=GUI.STANDARD_FONT_SMALL, width=6)
        add_point_y_entry.place(relx=widgets_x_start + 0.08, rely=0.617)

        def add_point():
            ...
        add_poly_node_button = tk.Button(self, text="ADD/ADJUST", command=add_point,
                                 width=11, height=1, font=GUI.STANDARD_FONT_BUTTON_SMALL)
        add_poly_node_button.place(relx=widgets_x_start + 0.125, rely=0.613)
        ##################################################

        ##################################################
        # info field maybe
        ##################################################





        ##################################################
        # Add canvas for system visualization - DYNAMIC
        self.canvas = tk.Canvas(self, width=GUI.CANVAS_SIZE_X, height=GUI.CANVAS_SIZE_Y, bg=GUI.CANVAS_BG)
        self.canvas.place(relx=canvas_x + 0.0075, rely=canvas_y)
        GUI.add_canvas_static_elements(self.canvas)
        ##################################################

        ##################################################
        # Accept Geometry button - returns value for geometry input and destroys window
        button_clear = tk.Button(self, text="ACCEPT GEOMETRY", command=self.return_geometry,
                                 width=16, height=1, font=GUI.STANDARD_FONT_BUTTON_BIG_BOLD)
        button_clear.place(relx=0.025, rely=0.925)
        ##################################################

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
