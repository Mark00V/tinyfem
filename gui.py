import tkinter as tk
import tkinter.font as tkFont

#################################################
# Other
AUTHOR = 'Itsame Mario'
VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 0
#################################################

#################################################
# tk inter statics

# Main Window
MAIN_WINDOW_SIZE_X = 1200
MAIN_WINDOW_SIZE_Y = 800

# Geometry Window
GEOM_WINDOW_SIZE_X = 1200
GEOM_WINDOW_SIZE_Y = 800

# Standard Canvas Size
CANVAS_SIZE_X = 900
CANVAS_SIZE_Y = 700
#################################################

class GUI(tk.Tk):


    def __init__(self):
        super().__init__()

        # FONTS
        self.STANDARD_FONT_1_BOLD = tkFont.Font(family="Arial", size=12, weight='bold')

        # Start Main Window
        self.main_window()

        # main input and output variables
        self.geometry_input = None

    def main_window(self):
        """

        :return:
        """
        self.title('TinyFEM - MAIN WINDOW')
        self.geometry(f"{MAIN_WINDOW_SIZE_X}x{MAIN_WINDOW_SIZE_Y}")

        button_define_geometry = tk.Button(self, text="DEFINE GEOMETRY", command=self.define_geometry, width=20, height=1)
        button_define_geometry.place(relx=0.025, rely=0.05)

        self.text_label = tk.Label(self, text="Init", font=self.STANDARD_FONT_1_BOLD)
        self.text_label.place(relx=0.4, rely=0.4)

    def define_geometry(self):
        return_geometry = Geometry(self.receive_geometry)

    def receive_geometry(self, geometry):
        self.geometry_input = str(geometry)
        self.text_label.config(text=self.geometry_input)


class Geometry(GUI, tk.Toplevel):

    def __init__(self, callback_geometry):
        super().__init__()

        # Callback geometry to return geometry values to guimain
        self.callback_geometry = callback_geometry
        self.geometry_input = None

    def main_window(self):
        """

        :return:
        """
        self.title('TinyFEM - DEFINE GEOMETRY')
        self.geometry(f"{GEOM_WINDOW_SIZE_X}x{GEOM_WINDOW_SIZE_Y}")

        button_clear = tk.Button(self, text="Geometry", command=self.return_geometry,
                                 font=self.STANDARD_FONT_1_BOLD, width=10, height=1)
        button_clear.place(relx=0.025, rely=0.05)


    def return_geometry(self):
        value = 999
        self.callback_geometry(value)


if __name__ == '__main__':
    #gui = GUI()  # Todo - Develop: For testing main gui
    gui = Geometry(0)  # Todo - Develop: For testing Geometry gui
    gui.mainloop()