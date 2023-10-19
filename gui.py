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

#################################################

class GUI(tk.Tk):


    def __init__(self):
        super().__init__()


        # FONTS
        self.STANDARD_FONT_1_BOLD = tkFont.Font(family="Arial", size=12, weight='bold')
        self.main_window()




    def main_window(self):
        """

        :return:
        """
        self.title('TinyFEM')
        self.geometry(f"{MAIN_WINDOW_SIZE_X}x{MAIN_WINDOW_SIZE_Y}")

        button_define_geometry = tk.Button(self, text="DEFINE GEOMETRY", command=self.define_geometry, width=20, height=1)
        button_define_geometry.place(relx=0.025, rely=0.05)

    def define_geometry(self):
        return_geometry = Geometry()
        print(return_geometry)


class Geometry(GUI):

    def __init__(self):
        super().__init__()

    def main_window(self):
        """

        :return:
        """
        self.title('Define Geometry')
        self.geometry(f"{MAIN_WINDOW_SIZE_X}x{MAIN_WINDOW_SIZE_Y}")

        button_clear = tk.Button(self, text="Geometry", command=self.return_geometry,
                                 font=self.STANDARD_FONT_1_BOLD, width=10, height=1)
        button_clear.place(relx=0.025, rely=0.05)


    def return_geometry(self):
        value = 999
        return value


if __name__ == '__main__':
    gui = GUI()
    gui.mainloop()