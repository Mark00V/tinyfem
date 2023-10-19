import tkinter as tk
import tkinter.font as tkFont

# Main Window
MAIN_WINDOW_SIZE_X = 1200
MAIN_WINDOW_SIZE_Y = 800

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # FONTS
        self.STANDARD_FONT_1_BOLD = tkFont.Font(family="Arial", size=12, weight='bold')

        # Initialize the instance variable
        self.text_variable = None

        # Start Main Window
        self.main_window()

    def main_window(self):
        print("first", self.text_variable)
        self.title('TinyFEM')
        self.geometry(f"{MAIN_WINDOW_SIZE_X}x{MAIN_WINDOW_SIZE_Y}")

        # Create a Label to display the instance variable
        self.text_label = tk.Label(self, text="", font=self.STANDARD_FONT_1_BOLD)
        self.text_label.place(relx=0.4, rely=0.4)

        button_define_geometry = tk.Button(self, text="DEFINE GEOMETRY", command=self.define_geometry, width=20, height=1)
        button_define_geometry.place(relx=0.025, rely=0.05)

    def define_geometry(self):
        # Create an instance of the Geometry class, passing a callback function
        return_geometry = Geometry(self.receive_geometry)

    def receive_geometry(self, geometry):
        # Update the instance variable with the received value
        self.text_variable = str(geometry)
        # Update the Label with the new value
        self.text_label.config(text=self.text_variable)
        print("second", self.text_variable)

class Geometry(GUI, tk.Toplevel):
    def __init__(self, callback_geometry):
        super().__init__()

        # Callback geometry to return geometry values to guimain
        self.callback_geometry = callback_geometry

    def main_window(self):
        self.title('Define Geometry')
        self.geometry(f"{MAIN_WINDOW_SIZE_X}x{MAIN_WINDOW_SIZE_Y}")

        button_clear = tk.Button(self, text="Geometry", command=self.return_geometry,
                                 font=self.STANDARD_FONT_1_BOLD, width=10, height=1)
        button_clear.place(relx=0.025, rely=0.05)

    def return_geometry(self):
        value = 999
        self.callback_geometry(value)

if __name__ == '__main__':
    gui = GUI()
    gui.mainloop()
